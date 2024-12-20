from flask import Blueprint, render_template, session, redirect,abort,request, url_for, flash,jsonify
from ..data.models import Users,Ratings, Uploads,Friendship
from ..utils.helpers import level,db
from werkzeug.utils import secure_filename


user_bp = Blueprint('user', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_MIME_TYPES = {'image/png', 'image/jpeg', 'image/gif'}
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

        if not allowed_file(file):
            flash('Error: Invalid file type. Allowed types are png, jpg, jpeg, and gif.')
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

    # Extract user details
    acc_name = user.username
    class_lv = level(int(user.class_level))
    member_since = str(user.created_at)[:4]
    rating = Ratings.get_rating(user.id)
    rate_flag = Ratings.allow_rating(session['username'], acc_name)
    friend_flag = Friendship.check_relationship(session['user_id'],user.id)
    friends_list = Friendship.get_friends(user.id)
    user_image = Uploads.query.filter_by(user_id=user.id).order_by(Uploads.id.desc()).first()

    # Render user page
    return render_template('user.html', acc_name=acc_name, class_lv=class_lv, member_since=member_since, rating=rating,
                            rate_flag=rate_flag, user_image=user_image,friend_flag=friend_flag,friends_list=friends_list)

def allowed_file(file):
    file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    if file_ext not in ALLOWED_EXTENSIONS:
        return False

    if file.mimetype not in ALLOWED_MIME_TYPES:
        return False

    return True

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

@user_bp.route('/users_lookup',methods=['GET',"POST"])
def search():
    if request.method == 'POST':

        session['usr_query'] = session.get('usr_query')

        return redirect(url_for('user.search_usr', page_num=1))
   
    return render_template('list_users_search.html')
    
@user_bp.route('/user_search/<int:page_num>', methods=["GET","POST"])
def search_usr(page_num):

    query = request.args.get('query')
    
    if not query:
        query = session.get('usr_query')
    
    if not query:
        query_string = request.query_string.decode('utf-8')
        if '=' in query_string:
            query = query_string.split('=')[1]  

    res = Users.query.filter(
        (Users.username.ilike(f"%{query}%")) |
        (Users.email.ilike(f"%{query}%"))
    ).paginate(per_page=9,page=page_num,error_out=True)


    return render_template('show_user.html',users=res,query=query)
    

@user_bp.route('/friend_request', methods=["POST"])
def friend_request():

    data = request.get_json()
    name = data['otherId']

    friend_id = Users.get_id_by_username(name)
    user_id = session.get('user_id')

    f = Friendship.send_friend_request(user_id=user_id,friend_id=friend_id)

    if f:
        return jsonify(f.status)
    else:
        return jsonify("Success")    


@user_bp.route('/deny_friend',methods=['post'])
def deny():
    name = request.form.get("username")
    curr_id = session.get('user_id')

    name_id = Users.get_id_by_username(name)
    if not name_id:
        print("name_id is none")
        return abort(404)


    f = Friendship.decline_friend_request(curr_id,name_id)

    if f:
        return redirect(url_for('inbox.inbox'))
    else:
        print("friendship value is none")

        abort(404)
   
    

@user_bp.route('/accept_friend',methods=['post'])
def accept():
    
    name = request.form.get("username")
    curr_id = session.get('user_id')

    name_id = Users.get_id_by_username(name)
    
    if not name_id:
        print("name_id is none")
        return abort(404)


    f = Friendship.accept_friend_request(curr_id,name_id)

    if f:
        return redirect(url_for('inbox.inbox'))
    else:
        print("friendship value is none")
        abort(404)

    



    




    

