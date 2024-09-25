from app import app,db
from flask import request, jsonify,render_template,send_file,make_response
from app.model import Post,Like,Follow,Profile,Comment

from io import BytesIO
from flask_weasyprint import HTML, render_pdf

@app.route('/other/pdf/<int:id>.pdf', methods=['GET', 'POST'])
def pdf(id):
    post = Post.query.filter_by(auth_id=id).all()
    profile = Profile.query.filter_by(auth_id=id).one()
    html= render_template('pdf.html', post=post,pro_id=profile.id,username = profile.username,
                           description=profile.description ,Profile=profile)
    return render_pdf(HTML(string=html))
    # config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    # # pdf =  pdfkit.from_string(html, 'MyPDF.pdf', configuration=config)
    # pdf = pdfkit.from_string(html, False, configuration=config)
    # response = make_response(pdf)
    # response.headers["Content-Type"] = "application/pdf"
    # response.headers["Content-Disposition"] = "inline; filename=output.pdf"

    # return response

@app.route('/image/<int:image_id>')
def image(image_id):
    profile = Profile.query.filter_by(id=image_id).one()
    return send_file(BytesIO(profile.profile_img), mimetype='image')

@app.route('/image/post/<int:image_id>')
def image_post(image_id):
    post = Post.query.filter_by(id=image_id).one()
    return send_file(BytesIO(post.post_img), mimetype='image')


