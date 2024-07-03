from functools import wraps
from flask import redirect, url_for
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def jwt_or_redirect():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            is_valid = verify_jwt_in_request(optional=True)
            if not is_valid or not get_jwt_identity():
                return redirect(url_for("router.auth.login_page"))
            else:
                return fn(*args, **kwargs)

        return decorator

    return wrapper
