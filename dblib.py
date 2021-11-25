import json
'''
version 0.1. In development. UNSAVETY!. CAN BREAK USERBOT!

'''
db = str("rootdb.json")


def gettable(name: str) -> dict:
    global db
    try:
        with open(db, "r") as settingsfile:
            settings = json.load(settingsfile)
            return settings[name]
    except IndexError:
        return {"Error": "Module not found"}


def settable(name: str, data: dict) -> bool:
    global db
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
    try:
        settings[name] = data
    except IndexError:
        return False
    with open(db, "w") as settingsfile:
        json.dump(settings, settingsfile)
    return True


def setvalue(name: str, var: str, value) -> bool:
    global db
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
    try:
        settings[name] = value
    except IndexError:
        return False
    with open(db, "w") as settingsfile:
        json.dump(settings, settingsfile)
    return True


def getvalue(name: str, var: str):
    global db
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
    return settings[name][var]


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
    return True


def create(data: dict, file: str) -> bool:
    global db
    name = data["name"]
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
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
    return True


def getfnbyname(name):
    global db
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
    del settings[name]
    fn = None
    for mname in range(0, len(settings["root"]["modulelist"])):
        try:
            fn = settings["root"]["modulelist"][mname][name]
        except KeyError:
            pass
    return fn


def delete(name: str) -> str:
    global db
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
    del settings[name]
    for mname in range(0, len(settings["root"]["modulelist"])):
        try:
            fn = settings["root"]["modulelist"][mname][name]
            settings["root"]["modulelist"].pop(mname)
        except KeyError:
            pass
    with open(db, "w") as settingsfile:
        json.dump(settings, settingsfile)
    return fn
