from flask import Blueprint, render_template, session, redirect,abort
from data.models import Users,Ratings
from utils.helpers import level
from data.models import Users, Messages, db


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
        return redirect('/error')

    # Extract user details
    acc_name = user.username
    class_lv = level(int(user.class_level))
    member_since = str(user.created_at)[:4]
    rating = Ratings.get_rating(user.id)

    curr_user = session.get('username')
    can_rate = False

    if curr_user:
        # Check if both users have messaged each other
        messages_exist = (
            Messages.query.filter(
                (Messages.sender == curr_user) & (Messages.recipient == acc_name)
            ).count() > 0 and
            Messages.query.filter(
                (Messages.sender == acc_name) & (Messages.recipient == curr_user)
            ).count() > 0
        )
        can_rate = messages_exist
    # Render user page
    return render_template('user.html', acc_name=acc_name, class_lv=class_lv, member_since=member_since,rating=rating, can_rate=can_rate)


@user_bp.route('/delete',methods=["POST","GET"])
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


