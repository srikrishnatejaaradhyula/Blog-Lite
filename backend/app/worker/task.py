from app import app,db,celery
from flask import request, jsonify,render_template,send_file,make_response
from app.model import Post,Like,Follow,Profile,Comment
from datetime import datetime, timezone
from base64 import b64decode

from celery.result import AsyncResult


@celery.task()
def create_post_task(title, caption, user_id, img):
    with app.app_context():
        # Perform the task logic
        img_data = b64decode(img)
        post = Post(auth_id=user_id, title=title, description=caption, post_img=img_data, created_at=datetime.now(timezone.utc))
        db.session.add(post)
        db.session.commit()
        print("*******************************")
        print('Task completed')
        print("*******************************")
        return True


@celery.task()
def add(x, y):
    return x + y

@app.route('/task', methods=['GET', 'POST'])
def add_task():
    a = add.apply_async(args=(25, 500))
    return jsonify({'status': 'ok', 'add': str(a.id)}) 