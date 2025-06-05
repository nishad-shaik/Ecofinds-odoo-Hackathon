from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, Message, User

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat(user_id):
    other_user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        content = request.form['content']
        message = Message(
            sender_id=current_user.id,
            receiver_id=user_id,
            content=content
        )
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('chat_bp.chat', user_id=user_id))

    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    return render_template('chat.html', messages=messages, other_user=other_user)
