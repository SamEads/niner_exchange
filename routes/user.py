from flask import Blueprint, render_template, session, redirect,abort,request,url_for
from data.models import Users,Ratings
from utils.helpers import level
from data.models import Users, db


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
    rate_flag = Ratings.allow_rating(session['username'],acc_name)

    # Render user page
    return render_template('user.html', acc_name=acc_name, class_lv=class_lv, member_since=member_since,rating=rating,rate_flag=rate_flag)


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

@user_bp.route('/users_lookup',methods=['GET',"POST"])
def search():
    if request.method == 'POST':

        session['usr_query'] = request.form.get('query') or session.get('usr_query')

        return redirect(url_for('user.search_usr', page_num=1))
   
    return render_template('list_users_search.html')
    
@user_bp.route('/user_search/<int:page_num>', methods=["GET","POST"])
def search_usr(page_num):

    query = session.get('usr_query') or request.args.get('query')
    session['usr_query'] = query

    if not query: 
        return abort(400)
    

    res = Users.query.filter(
        (Users.username.ilike(f"%{query}%")) |
        (Users.email.ilike(f"%{query}%"))
    ).paginate(per_page=9,page=page_num,error_out=True)

    for k in res: 
        k.class_level = level(k.class_level)
    return render_template('show_user.html',users=res,query=query)
    


    