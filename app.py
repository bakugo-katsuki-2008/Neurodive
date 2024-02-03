from flask import Flask, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import bcrypt
from login import configure_login_routes
from register import configure_register_routes

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Neurodive'
app.secret_key = 'your_secret_key_here'

mysql = MySQL(app)

# Include login and register routes
configure_login_routes(app, mysql)
configure_register_routes(app, mysql)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/urgenthelp')
def urgenthelp():
    return render_template('urgenthelp.html')
@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM UserInformation WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template('dashboard.html', user=user)

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out successfully.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
