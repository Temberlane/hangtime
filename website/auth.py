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
        return render_template("login.html", user=current_user, form_data=request.form)
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
        return render_template("sign_up.html", user=current_user, form_data=request.form)

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
            start_time = datetime.strptime(request.form.get(f"{i}/stime"), '%H:%M').time()
            end_time = datetime.strptime(request.form.get(f"{i}/etime"), '%H:%M').time()

            if first_day.weekday() != last_day.weekday():
                m = 'Section start and end days must be on the same day of the week'
                valid = False
                break
            elif first_day > last_day:
                m = 'The first day must be before the last day'
                valid = False
                break
            elif start_time > end_time:
                m = 'The end time must be after the start time'
                valid = False
                break
            elif int(start_time.min.strftime("%M"))%30!=0 or int(end_time.min.strftime("%M"))%30!=0:
                m = 'Times must be inputted in 30 minute increments'
                valid = False
                break

        if valid:
            course = request.form.get("class")
            prof = request.form.get("prof")
            color = request.form.get("color") # gives hex code (as a str)
            flash("class successfully added", category='success')

            for i in range(num_sections):
                section_type = request.form.get(f"{i}/type")
                location = request.form.get(f"{i}/location") # may be none
                room = request.form.get(f"{i}/room") # may be none
                first_day = datetime.strptime(request.form.get(f"{i}/fday"), '%Y-%m-%d').date()
                last_day = datetime.strptime(request.form.get(f"{i}/lday"), '%Y-%m-%d').date()
                start_time = datetime.strptime(request.form.get(f"{i}/stime"), '%H:%M').time()
                end_time = datetime.strptime(request.form.get(f"{i}/etime"), '%H:%M').time()
                biweekly = request.form.get(f"{i}/biweekly") #'true' if yes, None if no
            return redirect(url_for('views.home'))
        else:
            flash(m, category='error')
            return render_template("add_class.html", user=current_user, form_data=request.form)
    return render_template("add_class.html", user=current_user)

@auth.route('/add-events',methods=['GET', 'POST'])
@login_required
def event_add():
    if request.method == 'POST':
        num_sections = int(request.form.get("sections"))
        valid = True
        for i in range(num_sections):
            start = datetime.strptime(request.form.get(f"{i}/start"), '%Y-%m-%dT%H:%M')
            end = datetime.strptime(request.form.get(f"{i}/end"), '%Y-%m-%dT%H:%M')
            if start > end:
                flash('Event must start before it ends', category='error')
                valid = False
                break
            elif int(start.min.strftime("%M"))%30!=0 or int(end.min.strftime("%M"))%30!=0:
                flash('Times must be inputted in 30 minute increments', category='error')
                valid = False
                break
        if valid:
            flash(f'event{"s" if num_sections>1 else ""} successfully added', category='success')
            for i in range(num_sections):
                color = request.form.get(f"{i}/color")
                location = request.form.get(f"{i}/location")
                start = datetime.strptime(request.form.get(f"{i}/start"), '%Y-%m-%dT%H:%M')
                end = datetime.strptime(request.form.get(f"{i}/end"), '%Y-%m-%dT%H:%M')
                repeats = request.form.get(f"{i}/repeats")
                notes = request.form.get(f"{i}/notes")
            return redirect(url_for('views.home'))
        else:

            return render_template("add_events.html", user=current_user, form_data=request.form)
    return render_template("add_events.html", user=current_user)


@auth.route('/schedule')
@login_required
def view_schedule():
    return render_template("adapted_schedule.html", user=current_user)
