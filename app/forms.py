from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class RegistroForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(), Length(min=3, max=64)
    ])
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(), Length(min=6)
    ])
    password2 = PasswordField('Repite la contraseña', validators=[
        DataRequired(), EqualTo('password', message='Las contraseñas no coinciden')
    ])
    role = SelectField('Soy...', choices=[
        ('producer', 'Productor'),
        ('artist', 'Artista')
    ])
    submit = SubmitField('Crear cuenta')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese nombre de usuario ya está en uso.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ese email ya está registrado.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Entrar')