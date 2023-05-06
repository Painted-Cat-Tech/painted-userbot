#!/usr/bin/env python3
import os, sys
import asyncio
import requests
import dblib

from pyrogram import Client, filters
from pyrogram.types import Message

app = Client(
    "my_account",
    plugins=dict(root="plugins")
)

def command(cmd: str, prefix: str = "%", only_me: bool = True) -> filters.Filter:
    command = filters.command(cmd, prefixes=prefix) 
    me = filters.me if only_me else True
    return command & me


@app.on_message(command("test"))
async def test(_, message: Message):
    await message.edit_text("Works good")


@app.on_message(command("help"))
async def help(_, message: Message):
    try:
        moduleslen = len(os.listdir('plugins'))-1
    except (ValueError, FileNotFoundError):
        moduleslen = 0

    await message.edit_text(
        f"**Number of modules: {moduleslen}**\n"
        "**Available commands:** \n"
        "%restart - restart the userbot \n"
        "%insmod (link to the module) (module name) - install the module \n"
        "%delmod (module name) - uninstall the module \n"
        "%modinfo (module name) - print module info \n"
        "%modlist - print modules list \n"
        "%test - check for operability \n"
        "%shutdown - shutdown the userbot \n"
        "%info - Userbot information", parse_mode="markdown"
    )


@app.on_message(command("restart"))
async def reboot(_, message: Message):
    await message.edit_text("Restarting")
    asyncio.sleep(2.0)
    await message.edit_text("Restarted!")
    os.execl(sys.executable, sys.executable, *sys.argv)


@app.on_message(command("shutdown"))
async def shutdown(_, message: Message):
    await message.edit_text("Turned off")
    print("Turned off from chat")
    sys.exit()


@app.on_message(command("insmod"))
async def insmodv2(_, message: Message):
    args = message.text.replace("%insmod ", "").split(" ")

    if args[0] == "usage":
        return await message.edit_text(
            "Usage:\n"
            "%insmod {module url}\n"
            "Module class:core\n"
            "Description:download and install modules.\n"
            "TODO: depedency resolving\n" # why did you place your todo inside this message? *_* (felix)
            "BETA!!!!!"
        )

    elif len(args) < 1:
        return await message.edit_text("I need link for download")

    elif len(args) > 2:
        return await message.edit_text("Please, choose ONE module name.")

    if len(args) == 1:
        link = args[0].split("/")
        filename = link[len(link)-1]
    else:
        filename = f"{args[1]}.py"

    try:
        os.chdir("plugins")
    except FileNotFoundError:
        os.mkdir("plugins")
        os.chdir("plugins")

    with open(filename, "w") as file:
        responce = requests.get(args[0]) # requests is not async #todo: use something async instead
        fc = responce.content.decode("UTF-8")
        if (
            "json.load" in fc 
            or "json.dump" in fc 
            or "json.loads" in fc 
            or "json.dumps" in fc
        ):
            await message.edit_text("""This module can try to access root table with very impotant info. Are you sure? (y/n) (redact me)""")

            while True:
                selection = message.text
                if selection in ["Y", "y"]:
                    break
                elif selection in ["N", "n"]:
                    await message.edit_text("Installation has been canceled by user")
                    return os.remove(f"{filename}.py")
                    

        file.write(fc)

    os.chdir("../")
    sys.path.append('plugins')

    module = __import__(filename.replace('.py', ''))
    moddata = module.datadef()
    moddata["link"] = args[0]

    code = dblib.create(moddata, filename)
    sys.path.remove('plugins')

    if code == 0:
        await message.edit_text(f"Module {moddata['name']} installed")
    elif code == 1:
        await message.edit_text(f"Module {moddata['name']} already installed")


@app.on_message(filters.command("delmod", prefixes="%") & filters.me)
async def delmod(_, message: Message):
    args = message.text.replace("%delmod ", "")
    import dblib

    if args == "usage":
        await message.edit_text("""Usage:\n
%delmod {module name}\n
Module class:core\nDescription:uninstall module.\n
BETA!!!!!""")
    else:
        fn = dblib.delete(args)
        if fn == 3:
            await message.edit_text(f"Module {args} is not installed")
        else:
            os.remove(f"plugins/{fn}")
            await message.edit_text(f"Module {args} has been uninstalled")


@app.on_message(filters.command("modinfo", prefixes="%") & filters.me)
async def modinfo(_, message: Message):
    args = message.text.replace("%modinfo ", "")
    import dblib
    if args == "usage":
        await message.edit_text("""Usage:\n
        %modinfo {module name}\n
        Module class:core\nDescription:print module info\n
        BETA!!!!!""")
    else:
        data = dblib.gettable(args)
        if data == 3:
            await message.edit_text(f"Module {args} is not installed")
        else:
            desc = data["description"]
            help = data["help"]
            await message.edit_text(f"""Module info:\n
Module name:{args}\n
Module description:{desc}\n
Module commands help:{help}""")


@app.on_message(filters.command("modlist", prefixes="%") & filters.me)
async def modlist(_, message: Message):
    import json
    args = message.text.replace("%modlist ", "")
    if args == "usage":
        await message.edit_text("""Usage:\n
%modlist\n
Module class:core\nDescription:print list of modules\n
        BETA!!!!!""")
    msgtext = "Module list:\n"
    db = "rootdb.json"
    with open(db, "r") as settingsfile:
        settings = json.load(settingsfile)
    if len(settings["root"]["modulelist"]) == 1:
        msgtext += f'{list(settings["root"]["modulelist"][0])[0]}'
    else:
        for i in list(settings["root"]["modulelist"]):
            msgtext += f"{list(i.keys())[0]}\n"
    await message.edit_text(msgtext)


@app.on_message(filters.command("info", prefixes="%") & filters.me)
async def info(_, message: Message):
    await message.edit_text("[Painted Userbot](https://github.com/Painted-Cat-Tech/painted-userbot)\nVersion:0.3-indev)", parse_mode="markdown")

print("Userbot ready to work") 
app.run()
