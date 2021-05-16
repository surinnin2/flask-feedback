from flask import Flask, request, render_template, redirect, flash, jsonify, session
from models import db, User, Feedback, connect_db
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserForm, FeedbackForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "passkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)

#######
#routes
#######

@app.route('/')
def get_homepage():
    """redirects to homepage"""
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """register"""

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        flash('Account Created!','success')
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Login"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['user_id'] = user.id
            flash('Logged in!', 'success')
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form=form)

@app.route('/logout', methods=['POST'])
def logout():

    session.pop('user_id')
    return redirect('/login')

@app.route('/users/<string:username>')
def users_page(username):
    """Users Page"""
    
    if 'user_id' in session:
        userID = session['user_id']
        user = User.query.get_or_404(f'{userID}')

        feedbacks = Feedback.query.filter(Feedback.username == user.username)

        return render_template('users_page.html', user=user, feedbacks=feedbacks)
    else:
        flash('You must be logged in to view this page!', 'danger')
        return redirect('/login')

@app.route('/users/<string:username>/delete', methods=['POST'])
def delete_user(username):
    """Delete User"""

    if 'user_id' in session:
        userID = session['user_id']
        user = User.query.get_or_404(f'{userID}')

        db.session.delete(user)
        db.session.commit()
        flash('User Deleted', 'info')
        session.pop('user_id')
        return redirect('/login')

    else:
        flash('You must be logged in to use this function!', 'danger')
        return redirect('/login')


@app.route('/users/<string:username>/feedback/add', methods=['GET', 'POST'])
def add_user_feedback(username):
    
    form = FeedbackForm()


    if request.method == 'GET':
        if 'user_id' in session:
            userID = session['user_id']
            user = User.query.get_or_404(f'{userID}')

            

            return render_template('add_feedback.html', form=form, user=user)
        else:
            flash('You must be logged in to view this page!', 'danger')
            return redirect('/login')

    elif request.method == 'POST':

        if form.validate_on_submit():

            title = form.title.data
            content = form.content.data
            username = username
            new_feedback = Feedback(title=title, content=content, username=username)

            db.session.add(new_feedback)
            db.session.commit()

            return redirect(f'/users/{username}')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def edit_feedback(feedback_id):

    if 'user_id' in session:
        userID = session['user_id']
        user = User.query.get_or_404(f'{userID}')

        feedback = Feedback.query.get_or_404(feedback_id)
        form = FeedbackForm(obj=feedback)

        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            flash(f'Feedback {feedback_id} updated!', 'info')
            return redirect(f'/users/{user.username}')


        return render_template('edit_feedback.html', form=form, user=user)
    else:
        flash('You must be logged in to view this page!', 'danger')
        return redirect('/login')

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):

    if 'user_id' in session:
        userID = session['user_id']
        user = User.query.get_or_404(f'{userID}')

        feedback = Feedback.query.get_or_404(feedback_id)
        db.session.delete(feedback)
        db.session.commit()

        flash(f'Feedback {feedback_id} deleted!', 'info')
        return redirect(f'/users/{user.username}')
    else:
        flash('You must be logged in to view this page!', 'danger')
        return redirect('/login')