from flask_login import login_required, login_user, logout_user, current_user
from flask import Blueprint, request, redirect, url_for, render_template
from model import Message, User
from ext import db


apps = Blueprint("app_blueprint", __name__)


@apps.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return "Пользователь с таким именем уже существует.", 400
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('app_blueprint.home'))
    return render_template('register.html')


@apps.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('app_blueprint.home'))
        else:
            print("12")
    return render_template('login.html')


@apps.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app_blueprint.login'))


@apps.route('/')
@login_required
def home():
    users = User.query.all()
    print(current_user.username, "username")
    return render_template('users.html', users=users)


@apps.route('/chat/<int:recipient_id>')
@login_required
def chat(recipient_id):
    recipient = User.query.get_or_404(recipient_id)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.recipient_id == recipient.id)) |
        ((Message.sender_id == recipient.id) & (Message.recipient_id == current_user.id))
    ).all()
    return render_template('chat.html', recipient=recipient, messages=messages)





















