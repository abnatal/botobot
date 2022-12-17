from functools import wraps

def token_required(fn):
    """ TODO JWT checking.
    """
    @wraps(fn)
    def decorated(*args, **kwargs):
        """ To be implemented. """
        return fn(*args, **kwargs)

    return decorated
