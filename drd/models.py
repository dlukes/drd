from . import app
from . import rules as r

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
tfml = app.config["TEXT_FIELD_MAX_LEN"]


class Race(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    data = True

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<Race {!r}>".format(self.id)


class CClass(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    data = True
    __tablename__ = "cclass"

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<Character class {!r}>".format(self.id)


class Size(db.Model):
    id = db.Column(db.String(2), primary_key=True)
    data = True

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<Size {!r}>".format(self.id)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(tfml), unique=True)

#     def __init__(self, name):
#         self.name = name

#     def __repr__(self):
#         return "<User {!r}>".format(self.name)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # user = db.relationship("User", backref=db.backref("characters", lazy="dynamic"))
    name = db.Column(db.String(tfml))
    race = db.Column(db.String, db.ForeignKey("race.id"))
    race_id = db.relationship("Race")
    cclass = db.Column(db.String, db.ForeignKey("cclass.id"))
    cclass_id = db.relationship("CClass")
    size = db.Column(db.String, db.ForeignKey("size.id"))
    size_id = db.relationship("Size")
    mana = db.Column(db.Integer)
    mana_max = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    hp_max = db.Column(db.Integer)
    xp = db.Column(db.Integer)
    copper = db.Column(db.Integer)
    silver = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    lvl = db.Column(db.Integer)
    sil = db.Column(db.Integer)
    odl = db.Column(db.Integer)
    obr = db.Column(db.Integer)
    int = db.Column(db.Integer)
    chr = db.Column(db.Integer)
    note = db.Column(db.Text)

    def __init__(self, name, race, cclass, note):
        self.name = name
        self.race = race
        self.cclass = cclass
        self.note = note

    def __repr__(self):
        return "<Character {!r}>".format(self.name)


class Obj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    name = db.Column(db.String(tfml))
    weight = db.Column(db.Integer)
    __mapper_args__ = dict(polymorphic_on="type")


class Char2Obj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    char = db.Column(db.Integer, db.ForeignKey("character.id"))
    obj = db.Column(db.Integer, db.ForeignKey("obj.id"))
    equipped = db.Column(db.Boolean)


class Generic(Obj):
    __mapper_args__ = dict(polymorphic_identity="generic")


class Armor(Obj):
    oc = db.Column(db.Integer)
    __mapper_args__ = dict(polymorphic_identity="armor")


class Shield(Obj):
    __mapper_args__ = dict(polymorphic_identity="shield")


class Melee(Obj):
    sz = db.Column(db.Integer)
    utoc = db.Column(db.Integer)
    delka = db.Column(db.Integer)
    __mapper_args__ = dict(polymorphic_identity="melee")


class Ranged(Obj):
    k = db.Column(db.Integer)
    s = db.Column(db.Integer)
    d = db.Column(db.Integer)
    __mapper_args__ = dict(polymorphic_identity="ranged")


def unwrap(form):
    return {k: v.data for k, v in form.__dict__.items()
            if hasattr(v, "data") and k not in ["submit", "csrf_token"]}


# def add_user(form):
#     db.session.add(User(form.name.data))
#     db.session.commit()


def create_character(form):
    c = Character(**unwrap(form))
    r.generate_statistics(c)
    db.session.add(c)
    db.session.commit()
