from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, SelectField, FileField 
from wtforms.validators import DataRequired, length
from flask_wtf.file import FileField, FileRequired, FileAllowed

color_choices = [
    ('random', 'Random'),
    ('red', 'Red'),
    ('green', 'Green'),
    ('blue', 'Blue'),
    ('yellow', 'Yellow'),
    ('orange', 'Orange'),
    ('pink', 'Pink'),
    ('purple', 'Purple'),
    ('brown', 'Brown'),
    ('gray', 'Gray'),
    ('black', 'Black'),
    ('lightblue', 'Light Blue'),
    ('lightgreen', 'Light Green'),
    ('lightyellow', 'Light Yellow'),
    ('lightgray', 'Light Gray'),
    ('darkred', 'Dark Red'),
    ('darkblue', 'Dark Blue'),
    ('darkgreen', 'Dark Green'),
    ('darkgray', 'Dark Gray'),
    ('cyan', 'Cyan'),
    ('magenta', 'Magenta'),
    ('lime', 'Lime'),
    ('indigo', 'Indigo'),
    ('violet', 'Violet'),
    ('beige', 'Beige'),
    ('ivory', 'Ivory'),
    ('teal', 'Teal'),
    ('navy', 'Navy'),
    ('maroon', 'Maroon')
]
graph_type_choices = [
    ('random', 'Random Graph'),
    ('bar', 'Bar Graph'),
    ('barh', 'Horizontal Bar Graph'),
    ('histogram', 'Histogram'),
    ('scatter', 'Scatter Plot'),
    ('heatmap', 'Heatmap')
]
class RegisterForm(FlaskForm):
    email = EmailField('E-Mail', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = EmailField('E-Mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class GraphForm(FlaskForm):
    file_upload = FileField('Upload CSV', validators=[FileRequired(), FileAllowed(['csv'], 'CSV files only!')])
    color = SelectField('Select color', choices=color_choices, default='random', validators=[DataRequired()])
    graph_type = SelectField('Select Type', choices=graph_type_choices, default='random', validators=[DataRequired()])
    submit = SubmitField('Generate Graph')