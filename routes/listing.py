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

    query = request.form.get('query')
    session["curr_query"] = query

    if not query:

        return abort(400,description ="Invalid query")
    

    res = Listing.query.filter(
        (Listing.title.ilike(f"%{query}%")) |
        (Listing.description.ilike(f"%{query}%"))
    ).limit(10) #can paginate later

    if not res:
        return None
    
    
    #json to display the search query
    return render_template('list_all_listings.html', listings=res)

# routes to show all listings displayed in a grid
@listing_bp.route('/listings')
def list_all_listings():
    if session.get('curr_query'):
        session.pop('curr_query')

    all_listings = Listing.query.all()
    return render_template('list_all_listings.html', listings=all_listings)




@listing_bp.route('/sort_listing',methods = ['POST'])
def sorted_listing() -> render_template:

    query = session.get('curr_query')
    critera = request.form.get('criteria')
    order = request.form.get('order','asc')

    if query:
        res = Listing.query.filter(
            (Listing.title.ilike(f"%{query}%")) |
            (Listing.description.ilike(f"%{query}%"))
            ).limit(10) #can paginate later
    else: 
        res = Listing.query.limit(10).all()

    
    sort_map = {
        'title': 'title',
        'price': 'price',
        'created_at': 'created_at',
    }
     
    col = sort_map.get(critera)
  
    if order =="asc":
        res = sorted(res, key=lambda x: getattr(x, str(col)))
    elif order == "desc":
        res = sorted(res, key=lambda x: getattr(x, str(col)), reverse=True)
    else:
        return -1
    

    return render_template('list_all_listings.html', listings = res)
     







