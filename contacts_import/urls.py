from django.conf.urls.defaults import *

import contacts_import.tasks


urlpatterns = patterns("contacts_import.views",
    url(r"^import_contacts/$", "import_contacts", name="import_contacts"),
    url(r"^authsub/login/$", "authsub_login", name="authsub_login"),
)


urlpatterns += patterns("bbauth.views",
    url(r"^bbauth/login/$", "login", {
        "redirect_to": "/contacts/import_contacts/"
    }, name="bbauth_login"),
)
