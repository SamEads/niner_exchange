from flask import Blueprint, request, session, redirect, abort, render_template, url_for
from flask_bcrypt import Bcrypt
from data.models import Users, Listing, db
from werkzeug.utils import secure_filename
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
    pic = request.files.get('pic')

    if not title or not description or not price:
        return abort(400, description="Invalid data provided")
    if not user_id or not Users.query.filter_by(id=user_id).first():
        return abort(400, description="You must be logged in to create a post")
    if not pic:
        return abort(400, description="No picture uploaded")  # Handle missing file

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype

    new_listing = Listing(
        user_id = user_id,
        title = title,
        description = description,
        price = float(price),
        img = pic.read(),
        name = filename,
        mimetype = mimetype
    )
    db.session.add(new_listing)
    db.session.commit()
    return redirect(url_for('listing.get_listing', listing_id=new_listing.id))

# routes to a completed listing
@listing_bp.route('/listing/<int:listing_id>')
def get_listing(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first()
    if listing is None:
        return abort(404, description="Listing not found")
    return render_template('view_listing.html', listing=listing)

# routes to the image
@listing_bp.route('/listing/<int:listing_id>/image')
def get_image(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first()
    return (
        listing.img,
        200,
        {'Content-Type': listing.mimetype}
    )

@listing_bp.route('/listings')
def list_all_listings():
    all_listings = Listing.query.all()

    return render_template('list_all_listings.html', listings=all_listings)
