from django.core.urlresolvers import reverse

from contacts_import.backends.importers.base import Importer


class GoogleImporter(Importer):
    
    name = "Gmail"
    oauth_service = "google"
    
    def get_authentication_url(self):
        return reverse("oauth_access_login", kwargs=dict(service=self.oauth_service))
