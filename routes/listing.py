from flask import Blueprint, request, session, redirect, abort, render_template, url_for
from flask_bcrypt import Bcrypt
from data.models import Users, db

# Create blueprint for authentication related routes
listing_bp = Blueprint('listing', __name__)
bcrypt = Bcrypt()

# Route to render listing page
@listing_bp.route('/listing')
def listing():
    return render_template('listing.html')
