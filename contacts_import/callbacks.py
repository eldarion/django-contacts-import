from django.core.exceptions import ImproperlyConfigured


def dummy(contacts):
    raise ImproperlyConfigured("CONTACTS_IMPORT_CALLBACK is set to a dummy "
        "callback. You should define your own.")


def debug(contacts):
    print "imported:"
    for contact in contacts:
        print repr(contact)
    print "done"
