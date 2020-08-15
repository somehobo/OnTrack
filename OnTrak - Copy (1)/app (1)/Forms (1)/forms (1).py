# This defines all of the forms that are use in the app. They are classes
# so each form is created as an object that can then be displayed on a template.

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, validators, TextAreaField, HiddenField

# This is the form for created and updated sections.  Sections are the name the app uses
# for 'classes' - like classes in school not in coding.
class SectionForm(FlaskForm):
    name = StringField("Name")
    subject = StringField("Subject")
    per = StringField("Per")
    desc = TextAreaField("Description")
    teacher = StringField("Teacher")
    submit = SubmitField("Submit")

# This is the form for creating and updating assignments.
class AssignmentForm(FlaskForm):
    name = StringField("Name")
    duedate = DateTimeField("Due Date", format='%m/%d/%Y')
    assigndate = DateTimeField("Date Assigned", format='%m/%d/%Y', validators=(validators.Optional(),))
    desc = TextAreaField("Description")
    submit = SubmitField("Submit")
