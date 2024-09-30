import json
from flask import session, redirect, url_for, render_template, request, flash
from . import main
from .forms import LoginForm, SignupForm

# Helper function to load users from login.json
def load_users():
    with open('database.json') as f:
        users = json.load(f)
    return users['users']

def save_users(users):
    with open('database.json', 'w') as f:
        json.dump({'users': users}, f, indent=4)

@main.route('/errorlogin')
def errorloginfunc():
    return render_template("errorlogin.html")


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    """Cadastro de novo usuário."""
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data

        # Load users and check if user already exists
        users = load_users()
        if any(u['name'] == name for u in users):
            flash('Username already exists. Please choose a different one.')
        else:
            # Add new user
            users.append({'name': name, 'password': password})
            save_users(users)
            flash('Registration successful! You can now log in.')
            return redirect(url_for('.index'))
    
    return render_template('signup.html', form=form)


@main.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        room = form.room.data

        # Load users and verify credentials
        users = load_users()
        user = next((u for u in users if u['name'] == name and u['password'] == password), None)

        if user:
            session['name'] = name
            session['password'] = password
            session['room'] = room
            return redirect(url_for('.chat'))
        else:
            return redirect("/errorlogin")
        
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')

    return render_template('index.html', form=form)

@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in the session."""
    name = session.get('name', '')
    password = session.get('password', '')
    room = session.get('room', '')

    if not name or not room or not password:
        return redirect(url_for('.index'))

    # Verify that the user is still valid
    users = load_users()
    user = next((u for u in users if u['name'] == name and u['password'] == password), None)

    if not user:
        flash('Invalid session, please log in again.')
        return redirect(url_for('.index'))

    return render_template('chat.html', name=name, room=room)
