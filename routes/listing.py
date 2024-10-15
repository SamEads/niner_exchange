from flask import Blueprint, request, session, redirect, abort, render_template, url_for
from flask_bcrypt import Bcrypt
from data.models import Users, Listing, db

# Create blueprint for authentication related routes
listing_bp = Blueprint('listing', __name__)
bcrypt = Bcrypt()

# Route to render listing page
@listing_bp.route('/listing')
def listing():
    return render_template('listing.html')

@listing_bp.route('/listing', methods=['POST'])
def createListing():
    user_id = session.get('user_id')
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')

    if not title or not description or not price:
        return abort(400, description="Invalid data provided")
    if not user_id:
        return abort(400, description="You must be logged in to create a post")

    new_listing = Listing(
        user_id = user_id,
        title = title,
        description = description,
        price = float(price)
    )

    db.session.add(new_listing)
    db.session.commit()
    return redirect(url_for('listing.listing'))
