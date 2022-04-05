from . import bp as api
from app.blueprints.auth.auth import token_auth
from flask import request, make_response, g, abort
from .models import *
from helpers import require_admin

#Get all the categories

@api.get('/category')
@token_auth.login_required()
def get_category():
    cats = Category.query.all()
    cats_dicts = [cat.to_dict() for cat in cats]
    return make_response({"categories":cats_dicts},200)
    
#create a new category

@api.post('/category')
@token_auth.login_required()
@require_admin
def post_category():
    cat_name = request.get_json().get("name")
    cat = Category(name=cat_name)
    cat.name=cat_name
    cat.save()
    return make_response(f"category {cat.id} with name {cat.name} created", 200)

#change my category

@api.put('/category/<int:id>')
@token_auth.login_required()
@require_admin
def put_category(id):
    cat_name = request.get_json().get("name")
    cat = Category.query.get(id)
    if not cat:
        abort(404)
    cat.name=cat_name
    cat.save()
    return make_response(f"category {cat.id} has a new name: {cat.name}", 200)

#delete a category
@api.delete('/category/<int:id>')
@token_auth.login_required()
@require_admin
def delete_category(id):
    cat = Category.query.get(id)
    if not cat:
        abort(404)
    cat.delete()
    return make_response(f"category {cat.id} with the name of: {cat.name} has been deleted", 200)