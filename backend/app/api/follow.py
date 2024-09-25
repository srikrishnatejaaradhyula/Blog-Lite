from flask import request, jsonify
from app import app,db
from app.token import token_required
from app.model import Follow, Profile, Auth,Post
from datetime import datetime, timezone, timedelta


@app.route('/api/follow', methods=['POST'])
def follow():
    data = request.get_json()
    follower_id = data['followerId']
    followed_id = data['followedId']
    following = data['following']
    
    if following == 1:
        follow = Follow(follower_id=follower_id, followed_id=followed_id)
        db.session.add(follow)
    else:
        follow = Follow.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
        db.session.delete(follow)
    
    db.session.commit()
    
    return jsonify({'success': True})


@app.route('/api/all_users', methods=['GET'])
@token_required
def get_users():
    users = Profile.query.all()
    # user_data = []
    return jsonify([{'id': u.auth_id, 'name': u.username} for u in users ])


@app.route('/follow/<int:user_id>', methods=['GET'])
@token_required
def follow_count(user_id):
    followers = Follow.query.filter_by(followed_id=user_id).count()
    following = Follow.query.filter_by(follower_id=user_id).count()
    return jsonify({'followers': followers, 'following': following})


@app.route('/api/following', methods=['GET', 'POST'])
@token_required
def get_following():
    data = request.get_json()
    followerId = data['followerId']
    followedId = data['followedId']
    following = Follow.query.filter_by(follower_id=followerId, followed_id=followedId).first()
    if following is not None:
        return jsonify({'following': 1})
    else:
        return jsonify({'following': 0})
    

@app.route('/api/posts_data', methods=['GET'])
def get_posts():
    # Fetch data from Post model and convert it to JSON
    posts = Post.query.all()
    posts_data = []
    for post in posts:
        post_data = {
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'auth_id': post.auth_id,
            'created_at': post.created_at
        }
        posts_data.append(post_data)
    return jsonify(posts_data)
