from django.conf.urls.defaults import *


urlpatterns = patterns("",
    url(r"^import_contacts/$", "contacts_import.views.import_contacts", name="import_contacts"),
    url(r"^authsub/login/$", "contacts_import.views.authsub_login", name="authsub_login"),
)