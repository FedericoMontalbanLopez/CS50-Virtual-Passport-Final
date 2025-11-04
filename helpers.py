from functools import wraps
from flask import redirect, render_template, session, flash

def apology(message, code=400):
    """Render message as an apology to user and use flash for display."""
    
    # Use flash to display the error message on the next page load
    flash(f"Error {code}: {message}", "danger")
    
    # For HTTP errors (like 403 or 400), we redirect to a safe page (like login or home)
    if code == 403:
        return redirect("/login")
    
    if code == 400:
        return redirect("/register")
    
    else:
        # Default behavior: redirect to the homepage or return a simple template
        return render_template("/"), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


