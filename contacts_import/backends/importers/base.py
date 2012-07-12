from contacts_import.conf import settings


class Importer(object):
    
    form_class = None
    
    def get_authentication_url(self):
        raise NotImplementedError()
    
    def run(self, *args, **kwargs):
        """
        Called when we are ready to do the import of contacts. This method
        will call process which calls the importer's handle to generate
        contacts from the given arguments.
        """
        # @@@ async? (consider how args and kwargs should be serialized;
        # that may change things quite a bit)
        self.process((args, kwargs))
    
    def process(self, args):
        """
        Handles the processing of contacts import and passes data to the
        callback for site specific processing. This method may not run in the
        same process that handled the web request.
        """
        contacts = self.handle(*args[0], **args[1])
        settings.CONTACTS_IMPORT_CALLBACK(contacts)
    
    def handle(self, *args, **kwargs):
        """
        This method should be overridden by our children to do what is best
        for them.
        """
        raise NotImplementedError()
