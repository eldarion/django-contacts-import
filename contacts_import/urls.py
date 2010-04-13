from django.conf.urls.defaults import *


urlpatterns = patterns("",
    url(r"^import_contacts/$", "contacts_import.views.import_contacts", name="import_contacts"),
    url(r"^authsub/login/$", "contacts_import.views.authsub_login", name="authsub_login"),
    url(r"^bbauth/login/$", "bbauth.views.login", {
        "redirect_to": "/contacts/import_contacts/",
    }, name="bbauth_login"),
    url(r"oauth/login/(?P<service>\w+)/", "contacts_import.views.oauth_login", name="oauth_login"),
    url(r"oauth/callback/(?P<service>\w+)/", "contacts_import.views.oauth_callback", name="oauth_callback"),
)