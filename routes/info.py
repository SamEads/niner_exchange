from flask import Blueprint, request, session, redirect, render_template,url_for,flash
from data.models import Users,Messages,Ratings,db


info_bp =  Blueprint('info', __name__)



@info_bp.route('/rate',methods=['GET','POST'])
def rate_usr():
    rating = int(request.form.get('rating'))
    user = (request.referrer).rsplit('/', 1)[-1] # Scrape owner of page from the url 
    curr_user = session.get('username')

    #both users must message each other for rating to post to db 
    messages_exist = (
    Messages.query.filter(
        (Messages.sender == curr_user) & (Messages.recipient == user)
    ).count() > 0 and 
    Messages.query.filter(
        (Messages.sender == user) & (Messages.recipient == curr_user)
    ).count() > 0
    )


    if messages_exist: 

        user_to_rate = Users.query.filter_by(username=user).first()
        curr_user_rating = Users.query.filter_by(username=curr_user).first()

        existing_rating = Ratings.query.filter_by(user_id=user_to_rate.id, rater_id = curr_user_rating.id).first()

        if existing_rating:
                existing_rating.rating = rating
                db.session.commit()
                return redirect(url_for('user.user',username=user_to_rate.username))


        if user_to_rate: 
            new_rating = Ratings(user_id=user_to_rate.id, rater_id=curr_user_rating.id, rating=rating)
            db.session.add(new_rating)
            db.session.commit()
        else: 
            return redirect(url_for('auth.error'))


    #if all cond fail, do nothing and rerender the page. 
    #not the most performant solution.
    return redirect(url_for('user.user',username=user))
