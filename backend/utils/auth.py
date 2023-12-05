from functools import wraps
from flask import abort, session


def login_required(role: str):
    """
    check user wheher has logged in by session
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            username = session.get("username")
            user_role = session.get("role")

            if not username:
                return abort(403, "Not Logged In!")
            if user_role != role:
                return abort(403, "Wrong role!")

            return func(*args, **kwargs)

        return wrapper

    return decorator
