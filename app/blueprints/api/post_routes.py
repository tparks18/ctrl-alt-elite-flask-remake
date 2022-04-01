from . import bp as api
from app.models import Post
from flask import request, make_response, g
from app.blueprints.auth.auth import token_auth

#return all the posts the user followers

@api.get('/posts')
@token_auth.login_required()
def get_posts():
    user = g.current_user
    posts = user.followed_posts()
    response_list=[]
    for post in posts:
        response_list.append(post.to_dict())
    return make_response({"posts":response_list}, 200)

#retun a single post from its id
@api.get('/posts/<int:id>')
@token_auth.login_required()
def get_single_post(id):
    user = g.current_user
    post = Post.query.get(id)

    if not post:
        abort(404)
    #check to make sure user has access to the post
    if not user.is_following(post.author) and not post.author.id == user.id:
        abort(403, description="no no no not in my house")
        # return make_response("no no no in my house", 403)

    return make_response(post.to_dict(), 200)

# {
# "body": "the post body"
#}

#create a new post
@api.post('/posts')
@token_auth.login_required()
def post_post():
    posted_data = request.get_json() #retrieves the payload
    u=g.current_user
    post = Post(**posted_data)
    post.save()
    u.posts.append(post)
    u.save()
    return make_response(f"Post id: {post.id} created",200)

#update posts
# {
# "body": "the post body"
# "id": 2
#}

#edit post
@api.put('/posts') #dirty easy way
@token_auth.login_required()
def put_post():
    posted_data = request.get_json()
    post = Post.query.get(posted_data['id'])
    if not post:
        abort(404)
    if not post.author.id == g.current_user.id:
        abort(403)
    post.edit(posted_data['body'])
    return make_response(f"Post id: {post.id} has been changed", 200)

#delete post
@api.delete('/posts/<int:id>')
@token_auth.login_required()
def delete_post(id):
    user = g.current_user
    post = Post.query.get(id)
    if not post:
        abort(404)
    #check to make sure user has access to the post
    if not post.author.id == user.id:
        abort(403, description="no no no not in my house")
        # return make_response("no no no in my house", 403)
    post.delete()
    return make_response(f"success! post with id: {id} was deleted", 200)