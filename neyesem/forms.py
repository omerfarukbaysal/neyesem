from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import SelectField, SelectMultipleField, widgets,StringField,validators,FileField
from wtforms.validators import InputRequired,DataRequired
from .choices import cuisine_choices,ingredients_choices

class CheckBox(SelectMultipleField):
    widget=widgets.ListWidget(prefix_label=True)
    option_widget=widgets.CheckboxInput()
    validators = [DataRequired()]

class MealForm(FlaskForm):
    ingredients = CheckBox(label='Choose an option', choices=ingredients_choices,validators=[DataRequired()])
    cuisine = SelectField('Cuisine', choices=cuisine_choices,validators=[InputRequired()])

class MealCreateForm(FlaskForm):
    name = StringField(label='Enter your meal\'s Name', validators=[InputRequired()])
    ingredients = CheckBox(label='Choose an option', choices=ingredients_choices, validators=[DataRequired()])
    cuisine = SelectField('Cuisine', choices=cuisine_choices, validators=[InputRequired()])
    image = FileField(validators=[FileAllowed(['png', 'jpeg', 'jpg'], "wrong format!"), FileRequired('File was empty!')])