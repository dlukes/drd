#!/usr/bin/env python3

import os.path as osp
import csv

from drd.models import db
import drd.models as m

ROOT = osp.split(osp.dirname(__file__))[0]


def repopulate(model):
    model.query.delete()
    fname = model.__name__ + ".csv"
    with open(osp.join(ROOT, "data", fname), newline="") as fh:
        rdr = csv.DictReader(fh)
        for rec in rdr:
            db.session.add(model(**rec))


def main():
    db.create_all()
    for model in dir(m):
        model = getattr(m, model)
        if "data" in dir(model):
            repopulate(model)
    db.session.commit()


if __name__ == "__main__":
    main()
