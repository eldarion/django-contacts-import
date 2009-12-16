import sys

from django.conf import settings


DEFAULT_CONTACT_PERSISTANCE = getattr(settings, "DEFAULT_CONTACT_PERSISTANCE",
    "contacts_import.backends.persistance.ModelPersistance")


class BaseRunner(object):
    def __init__(self, importer, persistance=None, **credentials):
        if persistance is None:
            module, klass = DEFAULT_CONTACT_PERSISTANCE.rsplit(".", 1)
            __import__(module)
            persistance = getattr(sys.modules[module], klass)
        self.importer = importer
        self.persistance = persistance
        self.credentials = credentials
    
    def import_contacts(self):
        raise NotImplementedError("Implement this in a subclass")


class SynchronousRunner(BaseRunner):
    def import_contacts(self):
        return self.importer.apply(args=[self.credentials, self.persistance()])


class AsyncRunner(BaseRunner):
    def import_contacts(self):
        return self.importer.delay(self.credentials, self.persistance())
