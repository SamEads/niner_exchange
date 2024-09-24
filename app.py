from flask import Flask, render_template,session,request,abort,redirect
from flask_bcrypt import Bcrypt
from data.models import *
import os,string,random



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_CON_STR') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Secure'
bcrypt = Bcrypt()

db.init_app(app)


@app.route('/end')
def hello_world():
    return render_template('index.html')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')


#will authenticate user if logging in. Not working rn.
@app.route('/auth', methods= ['POST', 'GET'])
def auth_user():
    username = request.form.get('username')
    password = request.form.get('password')

    if (not username and not password) or (username=='' and password ==''):
        abort(404)
    
    user = Users.query.filter_by(username=username).first()

    if not user:
        return redirect('/')
    
    if bcrypt.check_password_hash(user.password, password):
        session['username'] = user.username

        return redirect('/end')
    
    return f"<h1>DID NOT Work<h1>"



@app.post('/create')
def create():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username).first()

    session.clear() ## will remove after proper login auth is done

    sesh_usr = session.get('username') 
    
    if user is not None or sesh_usr is not None: # if the user is already in session or exist, ask them to login 
        return redirect('/login')

    if not username or not password:
        abort(400)


    #generate random email, will fix later
    email = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)) + '@' +''.join(random.choice(string.ascii_letters + string.digits) for _ in range(7))


    hashed_password = bcrypt.generate_password_hash(password,12).decode('utf-8')
    new_user = Users(username,email,hashed_password)


    session['username'] = username
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')
