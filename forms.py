from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField, SelectMultipleField, FileField
from wtforms.validators import DataRequired, length, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed


class RegisterForm(FlaskForm):
    email = EmailField('E-Pasts', validators=[DataRequired()])
    password1 = PasswordField('Ievadi Jauno Paroli', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Apstiprināt Jauno Paroli', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Reģistrēties')

class LoginForm(FlaskForm):
    email = EmailField('E-Pasts', validators=[DataRequired()])
    password = PasswordField('Ievadi Jauno Paroli', validators=[DataRequired()])
    submit = SubmitField('Ienākt')

class GraphForm(FlaskForm):
    data = FileField('Upload CSV', validators=[FileRequired(), FileAllowed(['csv'], 'CSV files only!')])
    title = StringField('Nosaukums', validators=[DataRequired()])
    submit = SubmitField('Generate Graph')