from importlib import import_module

from python_facebook.sdk.exceptions.facebook_class_not_found_exception import ClassNotFoundException


def get_class(path):
    """
        Load a class and return it
    """
    try:
        mod_name, class_name = path.rsplit('.', 1)
        mod = import_module(mod_name)
    except ImportError, e:
        raise ClassNotFoundException(('Error importing class from path %s: "%s"' % (path, e)))
    try:
        class_ = getattr(mod, class_name)
    except AttributeError:
        raise ClassNotFoundException(('Module "%s" does not define a "%s" class' % (mod_name, class_name)))
    return class_
