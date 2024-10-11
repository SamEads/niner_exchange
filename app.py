from flask import Flask, render_template,session,request,abort,redirect,url_for
from flask_bcrypt import Bcrypt
from data.models import *
import os

app = Flask(__name__)
bcrypt = Bcrypt()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_CON_STR') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Secure'

db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

@app.route('/user/<username>')
def user(username):

    user = Users.query.filter_by(username=username).first()

    
    if user is None:
        return render_template('home.html')
    

    acc_name = user.username
    class_lv = level(int(user.class_level))
    member_since = str(user.created_at)[:4]

    #can later validadate if this is the users page or another users page will have to 

    return render_template('user.html',acc_name=acc_name,class_lv=class_lv,member_since=member_since)

#will authenticate user if logging in.
@app.route('/auth', methods= ['POST', 'GET'])
def auth_user():
    username = request.form.get('username')
    password = request.form.get('password')

    if (not username and not password) or (username=='' and password ==''):
        abort(404)
    
    user = Users.query.filter_by(username=username).first()

    if not user:
        return redirect('/')
    
    if bcrypt.check_password_hash(user.password_hash, password):
        session['username'] = user.username

        return redirect(url_for('user', username = user.username))
    
    return f"<h1>DID NOT Work<h1>"


#Create account with username and password
@app.post('/create')
def create():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username).first()

    sesh_usr = session.get('username') 
    
    if user is not None or sesh_usr == username: # if the user is already in session or exist, ask them to login 
        return redirect('/login')

    if not username or not password:
        abort(400)


    hashed_password = bcrypt.generate_password_hash(password,12).decode('utf-8')
    new_user = Users(username,hashed_password)


    session['username'] = username
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('user', username = new_user.username))




def level(arg: int) -> str:
    match arg: 
        case 1: 
          return  "1st"
        case 2: 
           return "2nd"
        case 3:
          return  "3rd"
        case 4:
          return  "4th"