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

    subquery = db.session.query(
        Messages.id,
        Messages.sender,
        Messages.recipient,
        Messages.content,
        Messages.timestamp,
        func.row_number().over(
            partition_by=[
                func.least(Messages.sender, Messages.recipient),
                func.greatest(Messages.sender, Messages.recipient)
            ],
            order_by=Messages.timestamp.desc()
        ).label('rn')
    ).filter(
        or_(Messages.sender == user, Messages.recipient == user)
    ).subquery()

    latest_messages = db.session.query(Messages).join(
        subquery,
        Messages.id == subquery.c.id
    ).filter(
        subquery.c.rn == 1
    ).order_by(
        Messages.timestamp.desc()
    )

    return render_template('inbox.html', conversations=latest_messages)