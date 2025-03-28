from flask import Blueprint, render_template, flash, redirect
from .forms import LoginForm, RegisterForm
from .models import User, Graph
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            new_user = User()
            new_user.email = email
            new_user.password = password2

            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Account Created Successfully, You can now Login')
                return redirect('/login')
            except Exception as e:
                print(e)
                flash('Account Not Created!!, Email already exists')

            form.email.data = ''
            form.password1.data = ''
            form.password2.data = ''

    return render_template('/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user:
            if user.verify_password(password=password):
                login_user(user)
                return redirect('/')
            else:
                flash('Incorrect Email or Password')

        else:
            flash('Account does not exist please Sign Up')

    return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    return redirect('/')

@auth.route('/account/<int:user_id>')
@login_required
def account(user_id):
    formatted_date = current_user.date_joined.strftime("%B %d, %Y at %I:%M %p")
    user = User.query.get(user_id)
    graphs = Graph.query.filter_by(user_id=current_user.id).all()
    return render_template('account.html', user=user, graphs=graphs, formatted_date=formatted_date)