# routes/inbox.py

from flask import Blueprint, render_template, session, redirect, url_for, flash
from data.models import Users, Messages, db
from sqlalchemy import func, or_, and_

# Create blueprint for inbox related routes
inbox_bp = Blueprint('inbox', __name__)

# Route to render the inbox page
@inbox_bp.get('/inbox')
def inbox():
    user = session.get('username')

    # Subquery to get the latest message timestamp for each conversation
    subquery = db.session.query(
        func.greatest(Messages.sender, Messages.recipient).label('user1'),
        func.least(Messages.sender, Messages.recipient).label('user2'),
        func.max(Messages.timestamp).label('latest_timestamp')
    ).filter(
        or_(Messages.sender == user, Messages.recipient == user)
    ).group_by(
        func.greatest(Messages.sender, Messages.recipient),
        func.least(Messages.sender, Messages.recipient)
    ).subquery()

    # Main query to get the latest messages
    latest_messages = db.session.query(Messages).join(
        subquery,
        and_(
            Messages.timestamp == subquery.c.latest_timestamp,
            or_(
                and_(Messages.sender == subquery.c.user1, Messages.recipient == subquery.c.user2),
                and_(Messages.sender == subquery.c.user2, Messages.recipient == subquery.c.user1)
            )
        )
    ).order_by(
        func.greatest(Messages.sender, Messages.recipient),
        func.least(Messages.sender, Messages.recipient),
        Messages.timestamp.desc()
    ).distinct(
        func.greatest(Messages.sender, Messages.recipient),
        func.least(Messages.sender, Messages.recipient)
    ).all()

    return render_template('inbox.html', conversations=latest_messages)