from functools import wraps
from flask import request, redirect, url_for


def when_logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if request.cookies.get("LOGIN"):
            return f(*args, **kwargs)
        else:
            return redirect(url_for("router.auth.login_page"))

    return decorated_func
