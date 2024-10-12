from flask import Blueprint, render_template, session, redirect
from data.models import Users,Ratings
from utils.helpers import level

user_bp = Blueprint('user', __name__)

# Route to render home page
@user_bp.route('/')
def home():
    return render_template('home.html')

# Route to render user page
@user_bp.route('/user/<username>')
def user(username):
    # Query user from database
    user = Users.query.filter_by(username=username).first()

    # If user does not exist, render home page
    if user is None:
        return redirect('/')

    # Extract user details
    acc_name = user.username
    class_lv = level(int(user.class_level))
    member_since = str(user.created_at)[:4]
    rating = Ratings.get_rating(user.id)

    # Render user page
    return render_template('user.html', acc_name=acc_name, class_lv=class_lv, member_since=member_since,rating=rating)