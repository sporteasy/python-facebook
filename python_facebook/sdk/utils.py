from importlib import import_module

from python_facebook.sdk.exceptions.facebook_class_not_found_exception import ClassNotFoundException


def get_class(path):
    """
        Load a class and return it
    """
    try:
        mod_name, class_name = path.rsplit('.', 1)
        mod = import_module(mod_name)
    except ImportError as e:
        raise ClassNotFoundException(('Error importing class from path %s: "%s"' % (path, e)))
    try:
        class_ = getattr(mod, class_name)
    except AttributeError:
        raise ClassNotFoundException(('Module "%s" does not define a "%s" class' % (mod_name, class_name)))
    return class_


def constant_time_compare(val1, val2):
    """
    Returns True if the two strings are equal, False otherwise.

    The time taken is independent of the number of characters that match.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1, val2):
        result |= ord(x) ^ ord(y)
    return result == 0
