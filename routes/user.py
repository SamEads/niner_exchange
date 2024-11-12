from flask import Blueprint, render_template, session, redirect, abort, request, flash
from werkzeug.utils import secure_filename

from data.models import Users, Ratings, Uploads
from utils.helpers import level
from data.models import Users, db

user_bp = Blueprint('user', __name__)


# Route to render home page
@user_bp.route('/')
def home():
    return render_template('home.html')


# Route to render user page
@user_bp.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    # Query user from database
    user = Users.query.filter_by(username=username).first()

    # If user does not exist, render home page
    if user is None:
        return redirect('/error')

    if request.method == 'POST':
        file = request.files.get('files')

        if not file:
            flash('Error: No image uploaded')
            return redirect(request.url)

        user_id = session.get('user_id')
        if not user_id:
            flash('Error: User must be logged in to upload')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        mimetype = file.mimetype

        new_image = Uploads(img=file.read(), filename=filename, mimetype=mimetype, user_id=user_id)
        db.session.add(new_image)
        db.session.commit()
        flash('Successfully changed profile picture!')

    # Extract user details
    acc_name = user.username
    class_lv = level(int(user.class_level))
    member_since = str(user.created_at)[:4]
    rating = Ratings.get_rating(user.id)
    rate_flag = Ratings.allow_rating(session['username'], acc_name)

    user_image = Uploads.query.filter_by(user_id=user.id).order_by(Uploads.id.desc()).first()

    # Render user page
    return render_template('user.html', acc_name=acc_name, class_lv=class_lv, member_since=member_since, rating=rating,
                           rate_flag=rate_flag, user_image=user_image)


@user_bp.route('/listing/<username>/image')
def get_user_image(username):
    user = Users.query.filter_by(username=username).first()

    if not user:
        abort(404, description="User not found")

    user_image = Uploads.query.filter_by(user_id=user.id).order_by(Uploads.id.desc()).first()
    if not user_image:
        return abort(404, description="Image not found")

    return (
        user_image.img,
        200,
        {'Content-Type': user_image.mimetype}
    )


@user_bp.route('/delete', methods=["POST", "GET"])
def kill_user():
    username = session.get('username')
    user = Users.query.filter_by(username=username).first()

    if user:
        db.session.delete(user)
        db.session.commit()
    else:
        return abort(400)

    session.clear()

    return redirect('/')
