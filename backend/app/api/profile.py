from flask import request, jsonify, send_file
from app import app,db
from app.token import token_required
from datetime import datetime, timezone
from app.model import Profile,Post,Like,Follow,Comment
from base64 import b64decode,b64encode
import io


    
@app.route("/api/create_profile", methods=["POST","GET"])
@token_required
def create_profile():
    data = request.get_json()
    username = data['username']
    description = data['description']
    user_id = data['user_id']
    img = b64decode(data['image'])

    if img  is None:
        return jsonify({"error": "Image is required"}), 400
    
    existing_profile = Profile.query.filter_by(auth_id=user_id).first()


    # check if user already exists
    if existing_profile is not None:
        return jsonify({"error": "Profile already created","id" :data['id']}), 401
    

    profile = Profile( username=username, profile_img= img ,auth_id=user_id, description=description, created_at=datetime.now(timezone.utc))
    db.session.add(profile)
    db.session.commit()
    return jsonify({"message": "Profile created successfully"}), 200


@app.route("/api/get_profile", methods=["GET","POST"])
@token_required
def get_profile():
    data = request.get_json()
    profile = Profile.query.filter_by(auth_id=data['user_id']).first()
    if profile is None:
        return jsonify({"error":"there is no profile"}), 401
    else:
        return jsonify({"username": profile.username, "description": profile.description }), 200


@app.route("/api/get_profile_img", methods=["GET","POST"])
@token_required
def get_profile_img():
    data = request.get_json()
    profile = Profile.query.filter_by(auth_id=data['id']).first()
    return send_file(
        io.BytesIO(profile.profile_img),
        mimetype='image/jpeg'
    )


@app.route("/api/update_profile", methods=["PUT"])
@token_required
def update_profile():
    data = request.get_json()
    existing_profile = Profile.query.filter_by(auth_id=data["user_id"]).first()
    if existing_profile:
        existing_profile.username = data["username"]
        existing_profile.description = data["description"]
        existing_profile.profile_img = b64decode(data['image'])
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 201
    else:
        return jsonify({"error": "Profile not found"}), 401
            
        
@app.route("/api/other_data", methods=["GET","POST"])
@token_required
def other_data():
    data = request.get_json()
    post = Post.query.filter_by(auth_id=data['user_id']).count()
    followers = Follow.query.filter_by(followed_id=data['user_id']).count()
    following = Follow.query.filter_by(follower_id=data['user_id']).count()
    return jsonify({"post": post, "followers": followers, "following": following}), 200
