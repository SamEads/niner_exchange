from flask import Blueprint, request, session, redirect, render_template, url_for, flash
from data.models import Users, Messages
from utils.helpers import db

# Create blueprint for messaging related routes
messaging_bp = Blueprint('messaging', __name__)

@messaging_bp.get('/messages/<recipient>')
def view_messages(recipient):
    # Session username
    sender = session.get('username')
    
    # If sender is not logged in, redirect to login page.
    if not sender:
        flash('You need to be logged in to view messages.')
        return redirect(url_for('auth.login'))
        
    # If sender is the same as recipient, redirect to home.
    if sender == recipient:
        return redirect('/')

    # If recipient does not exist, redirect to home.
    recipient_user = Users.query.filter_by(username=recipient).first()
    if not recipient_user:
        return redirect('/')

    # Get messages between sender and recipient
    messages = Messages.query.filter(
        (Messages.sender == sender) & (Messages.recipient == recipient) |
        (Messages.sender == recipient) & (Messages.recipient == sender)
    ).order_by(Messages.timestamp).all()

    return render_template('messaging.html', messages=messages, recipient=recipient)

# Route to handle sending a message
@messaging_bp.post('/send-message')
def send_message():
    # Session username
    sender = session.get('username')
    
    # Recipient username
    recipient_username = request.form.get('recipient')
    
    # Message content
    message_content = request.form.get('message')

    # Check if sender is logged in
    if not sender:
        flash('You need to be logged in to send a message.')
        return redirect(url_for('auth.login'))

    # Prevent sending message to self
    if sender == recipient_username:
        flash('You cannot send messages to yourself.')
        return redirect(url_for('messaging.view_messages', recipient=recipient_username))

    # Check if recipient exists
    recipient = Users.query.filter_by(username=recipient_username).first()
    if not recipient:
        flash('Recipient does not exist.')
        return redirect(url_for('messaging.view_messages', recipient=recipient_username))

    # Check message length
    if len(message_content) > 1000:
        flash('Message cannot exceed 1000 characters.')
        return redirect(url_for('messaging.view_messages', recipient=recipient_username))

    # Create and save the message
    new_message = Messages(sender=sender, recipient=recipient.username, content=message_content)
    db.session.add(new_message)
    db.session.commit()

    return redirect(url_for('messaging.view_messages', recipient=recipient_username))