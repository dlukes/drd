from math import ceil
from random import randint

races = {
    "hobit": {"size": "A",
              "mech": 5,
              "sil": {"range": "3-8", "corr": -5},
              "obr": {"range": "11-16", "corr": 2},
              "odl": {"range": "8-13", "corr": 0},
              "int": {"range": "10-15", "corr": -2},
              "chr": {"range": "8-18", "corr": 3}},
    "kudůk": {"size": "A",
              "mech": 5,
              "sil": {"range": "5-10", "corr": -3},
              "obr": {"range": "10-15", "corr": 1},
              "odl": {"range": "10-15", "corr": 1},
              "int": {"range": "9-14", "corr": -2},
              "chr": {"range": "7-12", "corr": 0}},
    "trpaslík": {"size": "A",
                 "obj": 5,
                 "sil": {"range": "7-12", "corr": 1},
                 "obr": {"range": "7-12", "corr": -2},
                 "odl": {"range": "12-17", "corr": 3},
                 "int": {"range": "8-13", "corr": -3},
                 "chr": {"range": "7-12", "corr": -2}},
    "elf": {"size": "B",
            "mech": 5,
            "sil": {"range": "6-11", "corr": 0},
            "obr": {"range": "10-15", "corr": 1},
            "odl": {"range": "6-11", "corr": -4},
            "int": {"range": "12-17", "corr": 2},
            "chr": {"range": "8-18", "corr": 2}},
    "člověk": {"size": "B",
               "sil": {"range": "6-16", "corr": 0},
               "obr": {"range": "9-14", "corr": 0},
               "odl": {"range": "9-14", "corr": 0},
               "int": {"range": "10-15", "corr": 0},
               "chr": {"range": "2-17", "corr": 0}},
    "barbar": {"size": "B",
               "obj": 5,
               "sil": {"range": "10-15", "corr": 1},
               "obr": {"range": "8-13", "corr": -1},
               "odl": {"range": "11-16", "corr": 1},
               "int": {"range": "6-11", "corr": 0},
               "chr": {"range": "1-16", "corr": -2}},
    "kroll": {"size": "C",
              "obj": 5,
              "sil": {"range": "11-16", "corr": 3},
              "obr": {"range": "5-10", "corr": -4},
              "odl": {"range": "13-18", "corr": 3},
              "int": {"range": "2-7", "corr": -6},
              "chr": {"range": "1-11", "corr": -5}},
}

classes = {
    "válečník": {"sil": "13-18",
                 "odl": "13-18",
                 "hp": 10},
    "hraničář": {"sil": "11-16",
                 "int": "12-17",
                 "hp": 8},
    "alchymista": {"obr": "13-18",
                   "odl": "12-17",
                   "hp": 7},
    "kouzelník": {"int": "14-19",
                  "chr": "13-18",
                  "hp": 6},
    "zloděj": {"obr": "14-19",
               "chr": "12-17",
               "hp": 6}
}


def bonus(v):
    v = v - 1 if v > 11 else v
    return -5 + v // 2


def correct_range(range, corr):
    return "-".join(str(int(num) + corr) for num in range.split("-"))


def range2roll(die):
    min, max = (int(num) for num in die.split("-"))
    rolls = (max - min) // 5
    bonus = min - rolls
    return "{}d6+{}".format(rolls, bonus)


def roll(die):
    if "-" in die:
        die = range2roll(die)
    if "+" in die:
        die, bonus = die.split("+")
        rolls, sides = (int(num) for num in die.split("d"))
    return sum(randint(1, sides) for _ in range(rolls)) + int(bonus)


def generate_statistics(model):
    model.size = races[model.race]["size"]
    for attr in ["sil", "odl", "obr", "int", "chr"]:
        if attr in classes[model.cclass]:
            die = correct_range(classes[model.cclass][attr],
                                races[model.race][attr]["corr"])
        else:
            die = races[model.race][attr]["range"]
        setattr(model, attr, roll(die))
    model.hp_max = classes[model.cclass]["hp"] + bonus(model.odl)
    model.hp = model.hp_max
    model.mana = model.mana_max = 0
    model.size = races[model.race]["size"]
    model.xp = 0
    model.lvl = 1
    model.copper = 0
    model.silver = 0
    model.gold = 0


def derived(model):
    perc = dict(
        obj=dict(rand=max(bonus(model.int), 0), search=model.int + races[model.race].get("obj", 0)),
        mech=dict(rand=max(bonus(model.int), 0), search=ceil(model.int / 2) + races[model.race].get("mech", 0))
    )
    return locals()
