from flask import Blueprint, render_template, session, redirect, request, url_for
from data.models import Users, Ratings
from utils.helpers import level

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def home():
    return render_template('home.html')

# Route to handle search functionality
@user_bp.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query')
    return redirect(url_for('user.listings', query=search_query))

# Route to render listings page
@user_bp.route('/listings')
def listings():
    query = request.args.get('query')
    return render_template('listings.html', query=query)

@user_bp.route('/user/<username>')
def user(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        return redirect('/')

    acc_name = user.username
    class_lv = level(int(user.class_level))
    member_since = str(user.created_at)[:4]
    rating = Ratings.get_rating(user.id)

    return render_template('user.html', acc_name=acc_name, class_lv=class_lv, member_since=member_since, rating=rating)
