from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class GoalForm(FlaskForm):
  name = StringField('Goal Name', validators=[DataRequired(), Length(min=2, max=100)])
  description = TextAreaField('Description', validators=[Length(max=500)])
  submit = SubmitField('Add Goal')
