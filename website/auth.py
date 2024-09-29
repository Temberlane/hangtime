from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')  # Fixed spelling
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash("Email does not exist.", category='error')
    return render_template("login.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already is registered with an account', category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters. ", category='error')
        elif len(first_name) < 2:
            flash("First name must be greater than 1 characters", category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category='error')
        else:
            # Create the user
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method="pbkdf2:sha256"))
            db.session.add(new_user)
            db.session.commit()

            # Fetch the newly created user to log in
            user = User.query.filter_by(email=email).first()  # Fetch the user from the database

            if user:  # Ensure the user was created and fetched successfully
                login_user(user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('User creation failed. Please try again.', category='error')

    return render_template("sign_up.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/add-class',methods=['GET', 'POST'])
@login_required
def class_add():
    if request.method == 'POST':
        num_sections = int(request.form.get("sections"))
        valid = True
        for i in range(num_sections):
            first_day = datetime.strptime(request.form.get(f"{i}/fday"), '%Y-%m-%d').date()
            last_day = datetime.strptime(request.form.get(f"{i}/lday"), '%Y-%m-%d').date()
            if first_day.day != last_day.day:
                flash('Section start and end days must be on the same day of the week', category='error')
                valid = False
                break
        if valid:
            course = request.form.get("class")
            prof = request.form.get("prof")

            for i in range(num_sections):
                section_type = request.form.get(f"{i}/type")
                first_day = request.form.get(f"{i}/fday")
                last_day = request.form.get(f"{i}/lday")
                start_time = request.form.get(f"{i}/stime")
                end_time = request.form.get(f"{i}/etime")
                biweekly = request.form.get(f"{i}/biweekly") #'true' if yes, None if no
            return redirect(url_for('views.home'))


@auth.route('/schedule')
@login_required
def view_schedule():
    return render_template("adapted_schedule.html")
