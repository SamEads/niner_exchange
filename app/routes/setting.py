from flask import Blueprint, render_template, session, redirect,abort, request, flash
from ..data.models import Users,Ratings
from ..data.models import Users
from ..utils.helpers import db


setting_bp = Blueprint('setting', __name__)

# Route to render home page
@setting_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    
    username = session.get('username')
    
    user = Users.query.filter_by(username=username).first()
    """
    if user is None:
        return abort(404)
    """
    if request.method == 'POST':
        new_email = request.form.get('email')
        #new_username = request.form.get('username')
        new_password = request.form.get('password')
        new_class_level = request.form.get('class-level')

        """
        if new_username != user.username and Users.query.filter_by(username=new_username).first():
            flash('Username already taken. Please choose a different one.', 'error')
            return redirect(request.url)
        """
        # Check for duplicate emails, excluding the current user's email
        if new_email != user.email and Users.query.filter_by(email=new_email).first():
            flash('Email already in use. Please choose a different one.', 'error')
            return redirect(request.url)

        user.email = new_email
        user.class_level = new_class_level

        """
        if new_username != user.username:
            user.username = new_username
        """
        if new_password:
            user.set_password(new_password)

        db.session.commit()
        return redirect('/settings')
    return render_template('setting.html', user=user)
