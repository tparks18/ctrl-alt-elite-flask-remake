from . import bp as api
from app.models import User
from app.blueprints.auth.auth import basic_auth, token_auth
from flask import request, make_response, g, abort
from helpers import require_admin

@api.get('/token')
@basic_auth.login_required()
def get_token():
    user = g.current_user
    token = user.get_token()
    return make_response({"token":token}, 200)

@api.put('/admin/<int:id>')
@token_auth.login_required()
@require_admin
def make_admin(id):
    #Is the requester an admin?
    #taken care of by require_admin decorator
    #Check the user id exists
    u = User.query.get(id)
    if not u:
        abort(404)
    #make admin
    u.is_admin=True
    u.save()
    return make_response(f'{u.first_name} {u.last_name} is now an Admin', 200)

###NEW
@api.get('/login')
@basic_auth.login_required()
def get_login():
    user = g.current_user
    token = user.get_token()
    return make_response({"token":token, **user.to_dict()}, 200)