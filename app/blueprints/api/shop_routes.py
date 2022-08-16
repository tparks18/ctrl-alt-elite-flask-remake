from . import bp as api
from app.blueprints.auth.auth import token_auth
from flask import request, make_response, g, abort
from .models import *
from helpers import require_admin

#Get all the categories

@api.get('/category')
#@token_auth.login_required()
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
    return make_response(f"category {cat.id} with the name of: {cat.name} has been deleted"), 200
    
#####################
###Item API Routes###
#####################

#get all items from shop
@api.get('/item')
#@token_auth.login_required()
def get_items():
    items = Item.query.all()
    items_dicts = [item.to_dict() for item in items]
    return make_response({"items":items_dicts},200)

#get an item by its id
@api.get('/item/<int:id>')
#@token_auth.login_required()
def get_item(id):
    item = Item.query.get(id)
    if not item:
        abort(404)
    return make_response({item.to_dict},200)

#get all items in a category(by cat id)
@api.get('/item/category/<int:id>')
#@token_auth.login_required()
def get_items_by_cat(id):
    cat = Category.query.get(id)
    if not cat:
        abort(404)
    all_items_in_cat = [item.to_dict() for item in cat.products]
    return make_response({"items":all_items_in_cat},200)

#post route to create a new item
@api.post('/item')
@token_auth.login_required()
@require_admin
def post_item():
    item_dict = request.get_json()

    if not all(key in item_dict for key in {"name", "desc", "price", "img", "category_id"}):
        abort(400)

    item = Item()
    item.from_dict(item_dict)
    item.save()
    return make_response(f"Item {item.name} was created with an id of {item.id}", 200)

#put route to edit an item
@api.put('/item/<int:id>')
@token_auth.login_required()
@require_admin
def put_item(id):
    item_dict = request.get_json().get("item")
    item = Item.query.get(id)
    if not item:
        abort(404)
    item.from_dict(item_dict)
    item.save()
    return make_response(f"Item {item.name} with ID {item.id} has been updated", 200)

#delete an item
@api.delete('/item/<int:id>')
@token_auth.login_required()
@require_admin
def delete_item(id):
    item_to_delete = Item.query.get(id)
    if not item_to_delete:
        abort(404)
    item_to_delete.delete()
    return make_response(f"Item with {id} has been deleted"), 200
    