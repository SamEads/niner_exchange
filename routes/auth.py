from flask import Blueprint, request, session, redirect, abort, render_template, url_for
from flask_bcrypt import Bcrypt
from data.models import Users, db

# Create blueprint for authentication related routes
auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

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
        abort(404) # (Abort with 404 error if username or password is not provided)

    user = Users.query.filter_by(username=username).first()

    # Redirect if user does not exist
    if not user:
        return redirect('/')

    if bcrypt.check_password_hash(user.password_hash, password):
        session['username'] = user.username
        return redirect(url_for('user.user', username=user.username))

    return "<h1>DID NOT Work<h1>"

# Handle user registration
@auth_bp.post('/create')
def create():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username).first()
    sesh_usr = session.get('username')

    # Check if user already exists or if session username matches the provided username
    if user is not None or sesh_usr == username:
        return redirect('/login')

    # Check if username and password are provided
    if not username or not password:
        abort(400) # (Abort with 400 error if username or password is not provided)

    # Hash password & create new user
    hashed_password = bcrypt.generate_password_hash(password, 12).decode('utf-8')
    new_user = Users(username, hashed_password)

    session['username'] = username  # Set session username
    db.session.add(new_user)        # Add new user to database
    db.session.commit()             # Commit changes to database
    
    # Redirect
    return redirect(url_for('user.user', username=new_user.username))