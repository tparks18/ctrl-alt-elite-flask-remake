#make decorator
from functools import wraps
def require_admin(f):
    @wraps(f)
    def check_admin():
        if not g.current_user.is_admin:
            abort(403)
        else:
            return f()
    return check_admin

#makes @require_admin wrapper/decorator