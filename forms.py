from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField

class EditForm(FlaskForm):
    f_title = TextAreaField("Title")
    f_place = TextAreaField("Place")
    f_char1 = TextAreaField("Character 1")
    f_char2 = TextAreaField("Character 2")
    f_char2_possession = TextAreaField("Character 2 Possession")
    f_relationship = TextAreaField("Relationship")
    f_shared_interest = TextAreaField("Shared Interest")
    f_mission = TextAreaField("Mission")
    f_firstname = TextAreaField("First Name")
    f_surname = TextAreaField("Surname")
    f_historic_element = TextAreaField("Historic Element")
    f_historic_where = TextAreaField("Historic Where")
    f_action = TextAreaField("Action")
    f_final = TextAreaField("Final")
    f_submit = SubmitField("Save")