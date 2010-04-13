import sys


class BaseRunner(object):
    def __init__(self, importer, persistance=None, **credentials):
        from contacts_import.settings import DEFAULT_PERSISTANCE
        if persistance is None:
            persistance = DEFAULT_PERSISTANCE
        self.importer = importer
        self.persistance = persistance
        self.credentials = credentials
    
    def import_contacts(self):
        raise NotImplementedError("Implement this in a subclass")


class SynchronousResult(object):
    """
    Very simple result to mimic what is needed of Celery's result
    """
    
    def __init__(self, result):
        self.result = result
        self.status = "DONE"
    
    def ready(self):
        return True


class SynchronousRunner(BaseRunner):
    def import_contacts(self):
        return SynchronousResult(
            self.importer().run(self.credentials, self.persistance())
        )


class AsyncRunner(BaseRunner):
    def import_contacts(self):
        return self.importer.delay(self.credentials, self.persistance())
