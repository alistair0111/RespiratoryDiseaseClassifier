from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from projectapp.models import User
from flask_login import current_user







class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(),Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', 
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user= User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That Username Is Taken. Please Choose Different One!')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That Email Is Taken. Please Choose Different One!')




class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')                                    

class FileForm(FlaskForm):
    audio = FileField('Choose The Audio File In .WAV Format',
    						validators=[FileAllowed(['wav'])])
    submit = SubmitField('submit')

    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email =  StringField('Email',validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different username.')

    def validate_email(self,email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email is taken. Please sign-in with the same email or choose a diferent one.')

# class RequestResetForm(FlaskForm):
#     email =  StringField('Email',
#                             validators=[DataRequired(),Email()])
#     submit = SubmitField('Request Password Reset')
#     def validate_email(self,email):
#         email = User.query.filter_by(email=email.data).first()
#         if email is None:
#             raise ValidationError('There is no account with this email. You must register first!')



# class ResetPasswordForm(FlaskForm):
#     password = PasswordField('Password',
#                             validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password',
#                             validators=[DataRequired(),EqualTo('password')])
#     submit = SubmitField('Reset Password')
