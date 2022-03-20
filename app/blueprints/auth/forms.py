from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import Email, DataRequired, EqualTo, ValidationError
from app.models import User
import random
from jinja2 import Markup


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    #random numbers to generate a random icon
    r1=random.randint(1,1000)
    r2=random.randint(1001,2000)
    r3=random.randint(2001,3000)
    r4=random.randint(3001,4000)
    r1_img=Markup(f'<img src="https://avatars.dicebear.com/api/bottts/{r1}.svg" style="height:75px">')
    r2_img=Markup(f'<img src="https://avatars.dicebear.com/api/bottts/{r2}.svg" style="height:75px">')
    r3_img=Markup(f'<img src="https://avatars.dicebear.com/api/bottts/{r3}.svg" style="height:75px">')
    r4_img=Markup(f'<img src="https://avatars.dicebear.com/api/bottts/{r4}.svg" style="height:75px">')

    icon = RadioField('Avatar', choices=[(r1,r1_img),(r2,r2_img),(r3,r3_img),(r4,r4_img)], validators=[DataRequired()])

    #MUST BE LIKE THIS VALIDATE_FIELDNAME
    def validate_email(form, field):
        same_email_user = User.query.filter_by(email = field.data).first() #one instance of a user, first result, filter_by always gives a list unless you use first()

        if same_email_user:
            raise ValidationError('Email is Already In Use')

        

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Save Changes')

     #random numbers to generate a random icon
    r1=random.randint(1,1000)
    r2=random.randint(1001,2000)
    r3=random.randint(2001,3000)
    r4=random.randint(3001,4000)
    r1_img=Markup(f'<img src="https://avatars.dicebear.com/api/bottts/{r1}.svg" style="height:75px">')
    r2_img=Markup(f'<img src="https://avatars.dicebear.com/api/bottts/{r2}.svg" style="height:75px">')
    r3_img=Markup(f'<img src="https://avatars.dicebear.com/api/bottts/{r3}.svg" style="height:75px">')
    r4_img=Markup(f'<img src="https://avatars.dicebear.com/api/bottts/{r4}.svg" style="height:75px">')

    icon = RadioField('Avatar', choices=[(9000,"Don't Change"),(r1,r1_img),(r2,r2_img),(r3,r3_img),(r4,r4_img)], validators=[DataRequired()])
