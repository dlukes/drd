from . import app
from .forms import CreateCharacterForm, EditAttributeForm
from . import models as m
from . import rules as r

from flask import g, render_template, redirect, url_for, flash


def prep_table(model):
    header = list(c.name for c in model.__table__.c)
    rows = [[getattr(r, c) for c in header] for r in model.query.all()]
    return header, rows


def get_char(id):
    return m.Character.query.filter_by(id=id).one()


@app.context_processor
def utilities():
    bonus = r.bonus

    def signed(num):
        return "+" + str(num) if num >= 0 else str(num)

    return locals()


@app.route("/")
def index():
    # users = m.User.query.all()
    characters = m.Character.query.all()
    return render_template("index.html", **locals())


# @app.route("/new/user", methods=["GET", "POST"])
# def add_user():
#     form = AddUserForm()
#     if form.validate_on_submit():
#         m.add_user(form)
#         return redirect(url_for("index"))
#     return render_template("form.html", form=form)


@app.route("/char/new", methods=["GET", "POST"])
def create_character():
    form = CreateCharacterForm()
    if form.validate_on_submit():
        m.create_character(form)
        return redirect(url_for("index"))
    return render_template("form.html", form=form)


@app.route("/char/id/<int:id>")
def char(id):
    char = get_char(id)
    g.charname = char.name
    der = r.derived(char)
    return render_template("sheet.html", char=char, der=der)


@app.route("/char/<method>/<int:char_id>/<attr>", methods=["GET", "POST"])
def edit(method, char_id, attr):
    char = get_char(char_id)
    g.charname = char.name
    form = EditAttributeForm()
    if form.validate_on_submit():
        if method == "set":
            new_val = form.value.data
        elif method == "inc":
            new_val = getattr(char, attr) + form.value.data
        elif method == "dec":
            new_val = getattr(char, attr) - form.value.data
        else:
            raise RuntimeError("Unsupported field edit method: {!r}".format(method))
        setattr(char, attr, new_val)
        m.db.session.commit()
        flash("✓", "success")
        return redirect(url_for("char", id=char_id))
    if method == "set":
        label = "Nová hodnota"
        form.value.default = getattr(char, attr)
    elif method == "inc":
        label = "Přidat"
    elif method == "dec":
        label = "Ubrat"
    else:
        raise RuntimeError("Unsupported field edit method: {!r}".format(method))
    form.value.label.text = label
    form.process()
    return render_template("form.html", form=form)


@app.route("/dump/<model>")
def dump(model):
    header, rows = prep_table(getattr(m, model))
    return render_template("table.html", **locals())
