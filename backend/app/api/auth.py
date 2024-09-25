from flask import request,jsonify
from app import app,db
from app.token import token_required
import jwt
from datetime import datetime,timedelta
from app.model import Auth,Profile


@app.route("/api/login", methods=["POST","GET"])
def login():
    data = request.get_json()
    auth = Auth.query.filter_by(email=data["email"]).first()

    if auth is None:
        return jsonify({"error": "Email is incorrect"}), 400
    
    elif auth.password != data["password"]:
        return jsonify({"error": "Password is incorrect"}), 400

    token = jwt.encode({'id' : auth.id, 
                        'exp' : datetime.utcnow() + timedelta(hours=5)}, 
                        app.config['SECRET_KEY'], "HS256")
    
    profile = Profile.query.filter_by(auth_id=auth.id).first()
    if profile is None:
        return jsonify({'token' : token}), 201
    else:
        return jsonify({'token' : token}), 200




@app.route("/api/register", methods=["POST","GET"])
def register():
    data = request.get_json()
    existing_user = Auth.query.filter_by(email=data['email']).first()

    # check if user already exists
    if existing_user:
        return jsonify({"error": "Email already in use"}), 400
    
    # create new user
    user = Auth(name=data["name"], email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


# this route for testing only
@app.route("/fun", methods=["GET"])
def fun():
    return jsonify({"message": "You are fun!"}), 200

@app.route("/api/test", methods=["GET"])
@token_required
def test(current_user):
    return  jsonify({"user": current_user.id}), 200
    