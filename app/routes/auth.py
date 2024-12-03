from flask import Blueprint, request, flash, session, redirect, abort, render_template, url_for
from data.models import Users
from utils.helpers import db,bcrypt

# Create blueprint for authentication related routes
auth_bp = Blueprint('auth', __name__)

# Route to render login page
@auth_bp.route('/login')
def login():
    return render_template('login.html')


# Route to render registration page
@auth_bp.route('/registration')
def registration():
    return render_template('registration.html')

# Route to logout user
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Handle user authentication
@auth_bp.route('/auth', methods=['POST', 'GET'])
def auth_user():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if username and password are provided
    if (not username and not password) or (username == '' and password == ''):
        flash("Username and password are required.", "error")  # Flash message
        return redirect('/login')
    user = Users.query.filter_by(username=username).first()

    # Redirect if user does not exist
    if not user:
        flash("Invalid username or password. Please try again")  # Flash message
        return redirect('/login')

    if bcrypt.check_password_hash(user.password_hash, password):
        session['username'] = user.username
        session['user_id'] = user.id     # needs user.id to create listings
        return redirect(url_for('user.user', username=user.username))

    flash("Invalid username or password. Please try again")  # Flash message
    return redirect('/login')

# Handle user registration
@auth_bp.post('/create')
def create():
    username = request.form.get('username')
    password = request.form.get('password')
    class_level = request.form.get('class_level')

    user = Users.query.filter_by(username=username).first()
    sesh_usr = session.get('username')
    # Check if user already exists or if session username matches the provided username
    if user is not None or sesh_usr == username:
        flash("Your account already exist. Please log in.", "error")  # Flash message
        return redirect('/login')

    # Check if username and password are provided
    if not username or not password:
        abort(400) # (Abort with 400 error if username or password is not provided)

    # Hash password & create new user
    hashed_password = bcrypt.generate_password_hash(password, 12).decode('utf-8')
    new_user = Users(username, hashed_password, class_level)

    session['username'] = username  # Set session username
    db.session.add(new_user)        # Add new user to database
    db.session.commit()             # Commit changes to database

    # Redirect
    return redirect(url_for('user.user',username = new_user.username))



@auth_bp.route("/error")
def error():
    return render_template('error.html')
    