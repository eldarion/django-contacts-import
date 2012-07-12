from django.core.urlresolvers import reverse

from contacts_import.backends.importers.base import Importer


class YahooImporter(Importer):
    
    name = "Yahoo! Mail"
    oauth_service = "yahoo"
    
    def get_authentication_url(self):
        return reverse("oauth_access_login", kwargs=dict(service=self.oauth_service))
