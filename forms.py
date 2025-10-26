from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RegisterForm(FlaskForm):
    username = StringField('Nombre', validators=[DataRequired(), Length(3,80)])
    email = StringField('Correo', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(6,128)])
    password2 = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('El nombre de usuario ya existe.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('El email ya está en uso.')

class LoginForm(FlaskForm):
    email = StringField('Correo', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Contraseña actual', validators=[DataRequired()])
    new_password = PasswordField('Nueva contraseña', validators=[DataRequired(), Length(6,128)])
    new_password2 = PasswordField('Confirmar nueva contraseña', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Cambiar contraseña')
