from flask import Blueprint, url_for, render_template, flash, request
from flask import redirect, session, g

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjungle
from werkzeug.security import generate_password_hash, check_password_hash

from forms import UserCreateForm, UserLoginForm

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = db.user.find_one({'username':form.username.data})

        if user is None:
            new_user = {'username':form.username.data, 
                        'password':generate_password_hash(form.password1.data),
                        'email':form.email.data}
            db.user.insert_one(new_user)
            return redirect(url_for('root.root'))
        else:
            flash('이미 존재하는 사용자입니다.')
            
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        
        error = None
        user = db.user.find_one({'username':form.username.data})

        if user is None:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user['password'], form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        
        if error is None:
            session.clear()
            session['user_id'] = user['username']
            return redirect(url_for('root.root'))
        flash(error)

    return render_template('auth/login.html', form=form)
    

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('root.root'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.user.find_one({'username':user_id})
        

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
