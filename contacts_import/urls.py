from django.conf.urls.defaults import *

import contacts_import.tasks


urlpatterns = patterns("",
    url(r"^import_contacts/$", "contacts_import.views.import_contacts", name="import_contacts"),
    url(r"^authsub/login/$", "contacts_import.views.authsub_login", name="authsub_login"),
    url(r"^bbauth/login/$", "bbauth.views.login", {
        "redirect_to": "/contacts/import_contacts/",
    }, name="bbauth_login"),
)