from flask import request, jsonify, send_file
from app import app,db
from app.token import token_required
from datetime import datetime, timezone
from app.model import Post,Like,Follow,Profile,Comment
from base64 import b64decode, b64encode
import io
from app.worker.task import create_post_task
import pickle


@app.route('/api/like', methods=['POST'])
@token_required
def like():
    data = request.get_json()
    post_id = data['postId']
    user_id = data['userId']
    liked = data['liked']
    
    if liked:
        like = Like(post_id=post_id, auth_id=user_id)
        db.session.add(like)
    else:
        like = Like.query.filter_by(post_id=post_id, auth_id=user_id).first()
        db.session.delete(like)
    
    db.session.commit()
    
    return jsonify({'success': True}),200

@app.route('/api/like_count', methods=['GET','POST'])
@token_required
def like_count():
    data = request.get_json()
    count = Like.query.filter_by(post_id=data["postId"]).all()
    return jsonify({'count': str(len(count)), 'like': count[0].id})

@app.route('/api/liked', methods=['POST'])
@token_required
def liked():
    data = request.get_json()
    post_id = data['postId']
    user_id = data['userId']
    
    liked = Like.query.filter_by(post_id=post_id, auth_id=user_id).one()
    if liked is not None:
        return jsonify({'liked': 1})
    else:
        return jsonify({'liked': 0})
    

@app.route('/api/comment', methods=['GET','POST'])
@token_required
def comment():
    data = request.get_json()
    post_id = data['post_id']
    user_id = data['user_id']
    comment = data['comment']

    comment = Comment(post_id=post_id, auth_id=user_id, comment=comment,created_at=datetime.now(timezone.utc))
    db.session.add(comment)
    db.session.commit()
    return jsonify({'success': True}),200

@app.route('/api/get_comments', methods=['GET','POST'])
@token_required
def get_comments():
    data = request.get_json()
    post_id = data['post_id']
    comments = Comment.query.filter_by(post_id=post_id).all()
    comments_data = []
    for c in comments:
        user = Profile.query.filter_by(auth_id=c.auth_id).first()
        if user:
            comments_data.append({
                'id': c.id,
                'comment': c.comment,
                'user_id': c.auth_id,
                'username': user.username  # Add the username from Profile table
            })
    return jsonify(comments_data)


@app.route('/api/get_post_comment_data', methods=['GET','POST'])
@token_required
def get_post_comment_data():
    data = request.get_json()
    post_id = data['post_id']
    post = Post.query.filter_by(id=post_id).first()
    profile = Profile.query.filter_by(auth_id=post.auth_id).first()
    return jsonify({'id': profile.auth_id, 'username': profile.username, 'title': post.title, 'description': post.description, 'created_at': (datetime.utcnow() - post.created_at).days  })



@app.route('/api/delete_post', methods=['GET','POST'])
@token_required
def delete_post():
    data = request.get_json()
    post = Post.query.filter_by(id=data['post_id']).first()
    db.session.delete(post)
    db.session.commit()
    return jsonify({'success': True}),200   

@app.route('/api/update_post', methods=['GET','POST'])
@token_required
def update_post():
    data = request.get_json()
    post = Post.query.filter_by(id=data['post_id']).first()
    post.title = data['title']
    post.description = data['caption']
    db.session.commit()
    return jsonify({'success': True}),200


@app.route('/api/create_post', methods=['POST'])
@token_required
def create_post():
    data = request.get_json()
    title = data['title']
    caption = data['caption']
    user_id = data['user_id']
    img = b64decode(data['image'])
    img_base64 = b64encode(img).decode()  
    
    if img is None:
        return jsonify({"error": "Image is required"}), 400
    
    
    a = create_post_task.apply_async(args=(title, caption, user_id, img_base64))

    # post = Post(auth_id=user_id,title= title, description=caption, post_img=img,created_at=datetime.now(timezone.utc))
    # db.session.add(post)
    # db.session.commit()
    
    if a:
        return jsonify({'success': True}),200
    else:
        return jsonify({'success': False}),400
    

@app.route('/api/posts', methods=['GET','POST'])
@token_required
def get_post():
    data = request.get_json()
    user_id = data['user_id']
    follow = Follow.query.filter_by(follower_id=user_id).all()
    posts = Post.query.filter(Post.auth_id.in_([f.followed_id for f in follow])).all()
    current_time = datetime.utcnow()

    post_data = []
    for p in posts:
        user = Profile.query.filter_by(auth_id=p.auth_id).first()

        post_data.append({
            'id': p.id, 
            'title': p.title, 
            'description': p.description,
            'created_at': (current_time - p.created_at).days, 
            'user_id': p.auth_id,
            'user_name': user.username,
            'user_profile_id': user.id
        })
    return jsonify(sorted(post_data, key=lambda x: x['created_at']))


    # return jsonify(sorted([{'id': p.id, 'title': p.title, 'description': p.description,
    #                      'created_at': (current_time - p.created_at).days, 'user_id': p.auth_id} for p in posts], 
    #                      key=lambda x: x['created_at']))


@app.route('/api/post_img', methods=['GET','POST'])
@token_required
def get_post_img():
    data = request.get_json()
    post = Post.query.filter_by(id=data['post_id']).first()
    return send_file(
        io.BytesIO(post.post_img),
        mimetype='image/jpeg'
    )

@app.route('/api/profile_posts',methods=['GET','POST'])
@token_required
def get_profile_post():
    data = request.get_json()
    posts = Post.query.filter_by( auth_id =data['user_id']).all()
    current_time = datetime.utcnow()
    return jsonify([{'id': p.id, 'title': p.title, 'description': p.description,'created_at':(current_time - p.created_at).days,'user_id' : p.auth_id} for p in posts ])
    