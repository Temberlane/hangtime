from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", boolean=True)

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash("Email must be greater than 3 characters. ", catagory='error')
        elif len(firstName) < 2:
            flash("First name must be greater than 1 characters", catagory='error')
        elif password1 != password2:
            flash("Passwords don\'t match.", catagory='error')
        elif len(password1 < 7):
            flash("Password must be atleast 7 characters.", catagory='error')
        else:
            flash('Account created!', catagory='success')
            # add user to database
    return render_template("sign_up.html")

@auth.route('/add-schedule')
def schedule_add():
    return render_template("input_schedule.html")