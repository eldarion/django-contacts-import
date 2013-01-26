import functools

from django.conf import settings

from appconf import AppConf

from contacts_import.utils import load_path_attr


class ContactsImportAppConf(AppConf):
    
    IMPORTERS = {
        "gmail": "contacts_import.backends.importers.google.GoogleImporter",
        "yahoo": "contacts_import.backends.importers.yahoo.YahooImporter",
        "vcard": "contacts_import.backends.importers.vcard.vCardImporter",
        "csv": "contacts_import.backends.importers.csv.CSVImporter",
    }
    CALLBACK = "contacts_import.callbacks.dummy"
    
    class Meta:
        prefix = "contacts_import"
    
    def configure_importers(self, value):
        return {k: functools.partial(load_path_attr, v) for k, v in value.iteritems()}
    
    def configure_callback(self, value):
        return load_path_attr(value)
