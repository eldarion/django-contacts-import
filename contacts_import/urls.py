from django.conf.urls import patterns, url, include

from contacts_import.views import (
    ImportBeginView, ImportServiceView
)


urlpatterns = patterns("",
    url(r"^$", ImportBeginView.as_view(), name="contacts_import"),
    url(r"^(?P<service>\w+)/$", ImportServiceView.as_view(), name="contacts_import_service"),
)
