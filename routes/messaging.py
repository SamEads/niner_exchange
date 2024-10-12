from flask import Blueprint, request, session, redirect, render_template, url_for, flash
from data.models import Users, Messages, db

# Create blueprint for messaging related routes
messaging_bp = Blueprint('messaging', __name__)

# Route to render the messaging page
@messaging_bp.route('/messages/<recipient>', methods=['GET'])
def view_messages(recipient):
    sender = session.get('username')
    if not sender:
        flash('You need to be logged in to view messages.')
        return redirect(url_for('auth.login'))

    messages = Messages.query.filter(
        (Messages.sender == sender) & (Messages.recipient == recipient) |
        (Messages.sender == recipient) & (Messages.recipient == sender)
    ).order_by(Messages.timestamp).all()

    return render_template('messaging.html', messages=messages, recipient=recipient)

# Route to handle sending a message
@messaging_bp.route('/send-message', methods=['POST'])
def send_message():
    sender = session.get('username')
    recipient_username = request.form.get('recipient')
    message_content = request.form.get('message')

    # Check if sender is logged in
    if not sender:
        flash('You need to be logged in to send a message.')
        return redirect(url_for('auth.login'))

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

    flash('Message sent successfully!')
    return redirect(url_for('messaging.view_messages', recipient=recipient_username))

'''
# Route to handle editing a message
@messaging_bp.route('/edit-message/<int:message_id>', methods=['POST'])
def edit_message(message_id):
    sender = session.get('username')
    if not sender:
        flash('You need to be logged in to edit messages.')
        return redirect(url_for('auth.login'))

    message = Messages.query.get(message_id)
    if not message or message.sender != sender:
        flash('You can only edit your own messages.')
        return redirect(url_for('messaging.view_messages', recipient=message.recipient))

    new_content = request.form.get('message')
    if len(new_content) > 1000:
        flash('Message cannot exceed 1000 characters.')
        return redirect(url_for('messaging.view_messages', recipient=message.recipient))

    message.content = new_content
    message.edited = True
    db.session.commit()

    flash('Message edited successfully!')
    return redirect(url_for('messaging.view_messages', recipient=message.recipient))
'''