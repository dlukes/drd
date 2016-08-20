import os.path as osp

ROOT = osp.split(osp.dirname(__file__))[0]


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TEXT_FIELD_MAX_LEN = 80


class Production(Config):
    pass


class Dev(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "/".join(["sqlite:///", ROOT, "db", "dev.db"])


class Test(Config):
    TESTING = True
