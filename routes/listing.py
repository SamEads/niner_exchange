from flask import Blueprint, request, session, redirect, abort, render_template, url_for,jsonify,Response
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
    owner = listing.get_name(listing.user_id)
    if listing is None:
        return abort(404, description="Listing not found")
    return render_template('view_listing.html', listing=listing,owner=owner)

# routes to the image
@listing_bp.route('/listing/<int:listing_id>/image')
def get_image(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first()
    return (
        listing.img,
        200,
        {'Content-Type': listing.mimetype}
    )


@listing_bp.route("/search",methods=["POST","GET"])
def list_query():

    query = request.form.get('query') or session.get('curr_query')
    session["curr_query"] = query

    if not query:
        return abort(400,description ="Invalid query")
    
    page = request.args.get('page', 1, type=int)
    per_page = 8 

    res = Listing.query.filter(
        (Listing.title.ilike(f"%{query}%")) |
        (Listing.description.ilike(f"%{query}%"))
    ).paginate(page=page, per_page=per_page, error_out=False)

    if not res.items:
        return render_template('list_all_listings.html', listings=res, message="No listings found.")
    
    
    #json to display the search query
    return render_template('list_all_listings.html', listings=res)

# routes to show all listings displayed in a grid
@listing_bp.route('/listings')
def list_all_listings():
    if session.get('curr_query'):
        session.pop('curr_query')

    page = request.args.get('page', 1, type=int)
    per_page = 8  # Number of listings per page
    paginated_listings = Listing.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('list_all_listings.html', listings=paginated_listings)




@listing_bp.route('/sort_listing', methods=['POST'])
def sorted_listing():
    query = session.get('curr_query')
    criteria = request.form.get('criteria', 'title')
    order = request.form.get('order', 'asc')
    page = request.form.get('page', 1, type=int)
    per_page = 8  # Number of listings per page

    if query:
        res = Listing.query.filter(
            (Listing.title.ilike(f"%{query}%")) |
            (Listing.description.ilike(f"%{query}%"))
        )
    else:
        res = Listing.query

    sort_map = {
        'title': Listing.title,
        'price': Listing.price,
        'created_at': Listing.created_at,
    }

    col = sort_map.get(criteria, Listing.title)

    if order == "asc":
        res = res.order_by(col.asc())
    elif order == "desc":
        res = res.order_by(col.desc())

    paginated_listings = res.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('list_all_listings.html', listings=paginated_listings)
