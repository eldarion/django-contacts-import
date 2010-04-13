from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
try:
    from django.utils.importlib import import_module
except ImportError:
    from importlib import import_module


def map_to_class(setting, default):
    path = getattr(settings, setting, default)
    i = path.rfind(".")
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured("Error importing %s: '%s'" % (module, e))
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured("Module '%s' does not define a '%s'" % (module, attr))
    return attr


DEFAULT_PERSISTANCE = map_to_class(
    "CONTACTS_IMPORT_DEFAULT_PERSISTANCE",
    "contacts_import.backends.persistance.ModelPersistance"
)
RUNNER = map_to_class(
    "CONTACTS_IMPORT_RUNNER",
    "contacts_import.backends.runners.SynchronousRunner"
)