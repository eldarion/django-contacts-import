from django.conf import settings
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from django.contrib.auth.decorators import login_required

from gdata.contacts.service import ContactsService

from contacts_import.forms import VcardImportForm
from contacts_import.backends.importers import GoogleImporter, YahooImporter
from contacts_import.models import Contact
from contacts_import.settings import RUNNER, CALLBACK


GOOGLE_CONTACTS_URI = "http://www.google.com/m8/feeds/"


def _import_success(request, results):
    if results.ready():
        if results.status == "DONE":
            request.user.message_set.create(
                message = _("%(total)s people with email found, %(imported)s "
                    "contacts imported.") % results.result
            )
        elif results.status == "FAILURE":
            request.user.message_set.create(
                message = _("There was an error importing your contacts.")
            )
    else:
        request.user.message_set.create(
            message = _("We're still importing your "
                "contacts.  We'll let you know when they're ready, it "
                "shouldn't take too long.")
        )
        request.session["import_contacts_task_id"] = results.task_id
    return HttpResponseRedirect(request.path)


@login_required
def import_contacts(request, template_name="contacts_import/import_contacts.html"):
    runner_class = RUNNER
    callback = CALLBACK
    
    contacts = request.user.contacts.all()
    try:
        page_num = int(request.GET.get("page", 1))
    except ValueError:
        page_num = 1
    page = Paginator(contacts, 50).page(page_num)
    
    if request.method == "POST":
        action = request.POST["action"]
        
        if action == "upload_vcard":
            form = VcardImportForm(request.POST)
            
            if form.is_valid():
                results = form.save(request.user, runner_class=runner_class)
                return _import_success(request, results)
        elif action == "import-contacts":
            selected_post = set(request.POST.getlist("selected-contacts"))
            selected_session = request.session.get("selected-contacts", set())
            on_page = set([str(o.pk) for o in page.object_list])
            selected = (
                (selected_session - (on_page - selected_post)).union(selected_post)
            )
            request.session["selected-contacts"] = selected
            
            if "next" in request.POST:
                return HttpResponseRedirect("%s?page=%s" % (request.path, page_num+1))
            elif "prev" in request.POST:
                return HttpResponseRedirect("%s?page=%s" % (request.path, page_num-1))
            elif "finish" in request.POST:
                if not selected:
                    Contact.objects.filter(user=request.user).delete()
                    return HttpResponseRedirect(reverse("import_contacts"))
                return callback(request, selected)
        else:
            form = VcardImportForm()
            
            if action == "import_yahoo":
                bbauth_token = request.session.pop("bbauth_token", None)
                if bbauth_token:
                    runner = runner_class(YahooImporter,
                        user = request.user,
                        bbauth_token = bbauth_token
                    )
                    results = runner.import_contacts()
                    return _import_success(request, results)
            
            elif action == "import_google":
                authsub_token = request.session.pop("authsub_token", None)
                if authsub_token:
                    runner = runner_class(GoogleImporter,
                        user = request.user,
                        authsub_token = authsub_token
                    )
                    results = runner.import_contacts()
                    return _import_success(request,  results)
    else:
        form = VcardImportForm()
    
    ctx = {
        "form": form,
        "bbauth_token": request.session.get("bbauth_token"),
        "authsub_token": request.session.get("authsub_token"),
        "page": page,
        "task_id": request.session.pop("import_contacts_task_id", None),
    }
    
    return render_to_response(template_name, RequestContext(request, ctx))


def _authsub_url(next):
    contacts_service = ContactsService()
    return contacts_service.GenerateAuthSubURL(next, GOOGLE_CONTACTS_URI, False, True)


def authsub_login(request, redirect_to=None):
    if redirect_to is None:
        redirect_to = reverse("import_contacts")
    if "token" in request.GET:
        request.session["authsub_token"] = request.GET["token"]
        return HttpResponseRedirect(redirect_to)
    return HttpResponseRedirect(_authsub_url(request.build_absolute_uri()))


def oauth_login(request, service):
    consumer = oAuthConsumer(service)
    token = consumer.unauthorized_token()
    request.session["%s_unauth_token" % service] = token.to_string()
    return HttpResponseRedirect(consumer.authorization_url(token))


def oauth_callback(request, service):
    ctx = RequestContext(request)
    consumer = oAuthConsumer(service)
    unauth_token = request.session.get("%s_unauth_token" % service, None)
    if unauth_token is None:
        ctx.update({"error": "token_missing"})
    else:
        auth_token = consumer.check_token(unauth_token, request.GET)
        if auth_token:
            request.session["%s_token" % service] = str(auth_token)
            return HttpResponseRedirect(reverse("import_contacts"))
        else:
            ctx.update({"error": "token_mismatch"})
    return render_to_response("oauth_error.html", ctx)
