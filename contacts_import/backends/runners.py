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
    
    def __init__(self, importer, *args):
        self.importer = importer
        self.args = args
        self.status = "DONE"
    
    def run(self):
        self.result = self.importer().run(*self.args)
    
    def ready(self):
        return True


class SynchronousRunner(BaseRunner):
    def import_contacts(self):
        result = SynchronousResult(self.importer, self.credentials, self.persistance())
        result.run()
        return result


class AsyncRunner(BaseRunner):
    def import_contacts(self):
        return self.importer.delay(self.credentials, self.persistance())
