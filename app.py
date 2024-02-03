from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neurodive.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120),unique=True,nullable=False)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=True)  # Assuming date of birth is a date field
    password_hash = db.Column(db.String(120), nullable=False)

# Create tables (run this only once)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    current_user = session.get('user')
    return render_template('home.html', current_user=current_user)

@app.route('/urgenthelp')
def urgenthelp():
    return render_template('urgenthelp.html')

@app.route('/community')
def community():
    if 'user' not in session:
        flash('Please log in to access the community page.', 'error')
        return redirect(url_for('login'))
    current_user = session['user']
    return render_template('community.html', current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        # Check if the identifier is an email or a username
        user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            flash('Login successful', 'success')
            session['user'] = {'id': user.id, 'username': user.username}
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your email or username and password.', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        username = request.form['username']
        dob_str = request.form['dob']  # Get the date as a string
        password = request.form['password']
        # confirm_password = request.form['confirm_password']

        # Check if passwords match
        # if password != confirm_password:
        #     flash('Passwords do not match.', 'error')
        # else:
            # Check if username already exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                if User.query.filter_by(username=username).first() :
                    flash('Username already exists. Please choose a different username.', 'error')
                if User.query.filter_by(email=email).first():
                    flash('Email already exists.', 'error')

        else:
                # Convert the date string to a Python date object
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

                # Add the new user to the database with bcrypt hashing
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = User(email=email, name=name, username=username, dob=dob, password_hash=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful. You can now log in.', 'success')
                return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(port=8000, debug=True)
