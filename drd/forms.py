from . import app
from . import models as m

from flask_wtf import Form
from wtforms import (SelectField, StringField, SubmitField, TextAreaField,
                     IntegerField)
from wtforms.validators import InputRequired, Length
import sqlalchemy as sa

tfml = app.config["TEXT_FIELD_MAX_LEN"]
length_validator = Length(
    max=tfml, message="Maximální délka: {} znaků.".format(tfml))


def choices(model):
    try:
        return [(r.id, r.id) for r in model.query.all()]
    except sa.exc.OperationalError:
        return [("<empty>", "<empty>")]


# class AddUserForm(Form):

#     name = StringField("Jméno", validators=[
#         length_validator,
#         InputRequired(message="Chybí uživatelské jméno.")
#     ])
#     submit = SubmitField("Přidat uživatele")


class CreateCharacterForm(Form):

    name = StringField("Jméno", validators=[
        length_validator,
        InputRequired(message="Zvolte jméno postavy.")
    ])
    race = SelectField("Rasa", choices=choices(m.Race),
                       validators=[InputRequired("Zvolte rasu.")])
    cclass = SelectField("Povolání", choices=choices(m.CClass),
                         validators=[InputRequired("Zvolte povolání.")])
    note = TextAreaField("Poznámky")
    submit = SubmitField("Přidat postavu")


class EditAttributeForm(Form):

    value = IntegerField()
    submit = SubmitField("Potvrdit")
