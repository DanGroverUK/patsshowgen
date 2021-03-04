from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, HiddenField


class EditForm(FlaskForm):
    f_title = TextAreaField("Title", render_kw={"rows": "1"})
    f_place = TextAreaField("Place", render_kw={"rows": "1"})
    f_char1 = TextAreaField("Character 1", render_kw={"rows": "1"})
    f_char2 = TextAreaField("Character 2", render_kw={"rows": "1"})
    f_char2_possession = TextAreaField("Character 2 Possession", render_kw={"rows": "1"})
    f_relationship = TextAreaField("Relationship", render_kw={"rows": "1"})
    f_shared_interest = TextAreaField("Shared Interest", render_kw={"rows": "1"})
    f_mission = TextAreaField("Mission", render_kw={"rows": "1"})
    f_firstname = TextAreaField("First Name", render_kw={"rows": "1"})
    f_surname = TextAreaField("Surname", render_kw={"rows": "1"})
    f_historic_element = TextAreaField("Historic Element", render_kw={"rows": "1"})
    f_historic_where = TextAreaField("Historic Where", render_kw={"rows": "1"})
    f_action = TextAreaField("Action", render_kw={"rows": "1"})
    f_final = TextAreaField("Final", render_kw={"rows": "1"})
    f_para = TextAreaField("Paragraph", render_kw={"rows": "1"})
    f_submit = SubmitField("Save", render_kw={"rows": "1"})
    f_sel = HiddenField("sel")
    