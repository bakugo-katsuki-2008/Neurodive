from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
import bcrypt
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_mysqldb import MySQL
from flask import flash

def configure_login_routes(app, mysql):

    class LoginForm(FlaskForm):
        email_or_username = StringField("Email or Username", validators=[DataRequired()])
        password = PasswordField("Password", validators=[DataRequired()])
        submit = SubmitField("Login")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            email_or_username = form.email_or_username.data
            password = form.password.data

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM userinfo WHERE Email=%s OR Username=%s", (email_or_username, email_or_username))
            user = cursor.fetchone()
            cursor.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[5].encode('utf-8')):
                session['user_id'] = user[0]
                return redirect(url_for('dashboard'))
            else:
                flash("Login failed. Please check your email or username and password")
                return redirect(url_for('login'))

        return render_template('login.html', form=form)