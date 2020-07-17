from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from . import db
import datetime
from .models import Visitor, User

main = Blueprint('main', __name__)


@main.route('/')
def index():
    #control visitor with cookies
    cookie = request.cookies.get('isvisited')
    if cookie:
        #visit=True
        pass
    else:
        resp = make_response(render_template('index.html'))
        resp.set_cookie('isvisited', 'yess')
        return resp

    visitor_ip = request.remote_addr
    visited_time = datetime.datetime.now()
    visitors = Visitor.query.all()
    visited = Visitor.query.filter_by(ip=visitor_ip).first()
    visit = False
    if visited:
        difference = abs((visited_time - visited.last_visit).seconds)
        if difference > 60:
            visit = True
            visited.last_visit = visited_time
            db.session.commit()
    else:
        new_visitor = Visitor(ip=visitor_ip,last_visit=visited_time)
        db.session.add(new_visitor)
        db.session.commit()
    return render_template('index.html',visitors=visitors,visit=visit)

@main.route('/', methods=['POST'])
def index_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
