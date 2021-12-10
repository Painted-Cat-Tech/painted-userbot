import json
'''
version 0.2
In development. UNSAVETY!. CAN BREAK USERBOT!
Codes:
0:ok
1:already exists
2:var does not exists
3:table does not exists
'''
db = str("rootdb.json")


def gettable(name: str):
    global db
    try:
        with open(db, "r") as settingsfile:
            settings = json.load(settingsfile)
            return settings[name]
    except IndexError:
        return 3


def settable(name: str, data: dict) -> int:
    global db
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
    try:
        settings[name] = data
    except IndexError:
        return 3
    with open(db, "w") as settingsfile:
        json.dump(settings, settingsfile)
    return 0


def setvalue(name: str, var: str, value) -> int:
    global db
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
    if name in settings[name]:
        try:
            settings[name] = value
        except KeyError:
            return 2
        with open(db, "w") as settingsfile:
            json.dump(settings, settingsfile)
        return 0


def getvalue(name: str, var: str):
    global db
    try:
        with open(db, "r") as settingsfile:
            settings = json.load(settingsfile)
            return settings[name][var]
    except IndexError:
        return 2


def getlang() -> str:
    global db
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
    return settings["root"]["lang"]


def setlang(lang: str) -> bool:
    global db
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
    settings["root"]["lang"] = lang
    return 0


def create(data: dict, file: str) -> int:
    global db
    try:
        name = data["name"]
    except KeyError:
        return 2
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
    unique=True
    for mname in settings["root"]["modulelist"]:
        try:
            mname[name]
            unique=False
        except KeyError:
            pass
    if unique==False:
        return 1
    elif unique==True:
        settings[name] = data
        settings["root"]["modulelist"].append({name: file})
        try:
            settings[name]["description"] = data["description"]
        except KeyError:
            settings[name]["description"] = "Description not provided"
        try:
            settings[name]["help"] = data["help"]
        except KeyError:
            settings[name]["help"] = "Help page not provided"
        with open(db, "w") as settingsfile:
            json.dump(settings, settingsfile)
        return 0


def getfnbyname(name: str):
    global db
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
    del settings[name]
    for mname in range(0, len(settings["root"]["modulelist"])):
        try:
            fn = settings["root"]["modulelist"][mname][name]
        except KeyError:
            return 2
    return fn


def delete(name: str) -> str:
    global db
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
    try:
        del settings[name]
    except KeyError:
        return 3
    for mname in range(0, len(settings["root"]["modulelist"])):
        try:
            fn = settings["root"]["modulelist"][mname][name]
            settings["root"]["modulelist"].pop(mname)
        except KeyError:
            return 3
    with open(db, "w") as settingsfile:
        json.dump(settings, settingsfile)
    return fn
