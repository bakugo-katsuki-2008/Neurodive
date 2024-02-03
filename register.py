from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
import bcrypt
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_mysqldb import MySQL
from flask import redirect, url_for

def configure_register_routes(app, mysql):

    class RegisterForm(FlaskForm):
        name = StringField("Name", validators=[DataRequired()])
        email = StringField("Email", validators=[DataRequired(), Email()])
        username = StringField("Username", validators=[DataRequired()])
        dob = DateField("Date of Birth", validators=[DataRequired()])
        password = PasswordField("Password", validators=[DataRequired()])
        submit = SubmitField("Register")

        def validate_email(self, field):
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM userinfo WHERE Email=%s", (field.data,))
            user = cursor.fetchone()
            cursor.close()
            if user:
                raise ValidationError('Email Already Taken')

        def validate_username(self, field):
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM userinfo WHERE Username=%s", (field.data,))
            user = cursor.fetchone()
            cursor.close()
            if user:
                raise ValidationError('Username Already Taken')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            username = form.username.data
            dob = form.dob.data
            password = form.password.data

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # store data into database
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO userinfo (Name, Email, Username, DOB, Password) VALUES (%s, %s, %s, %s, %s)", (name, email, username, dob, hashed_password))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('login'))

        return render_template('register.html', form=form)