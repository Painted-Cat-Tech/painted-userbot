#!/usr/bin/env python3
from pyrogram.errors import FloodWait
 
from pyrogram.types import ChatPermissions
 
import time
from time import sleep
import random
from pyrogram import Client, filters
app = Client(
    "my_account",
    plugins=dict(root="plugins")
    )


@app.on_message(filters.command("test", prefixes="%") & filters.me)
async def test(client, message):
    await message.edit_text("Works good")

@app.on_message(filters.command("help", prefixes="%") & filters.me)
async def help(client, message):
    import os
    try:
        moduleslen=len(os.listdir('plugins'))-1
    except ValueError:
        moduleslen=0
    except FileNotFoundError:
        moduleslen=0
    await message.edit_text(f"**Number of modules: {moduleslen}**\n**Available commands:** \n%restart - restart the userbot \n%insmod 'link to the module' 'module name' - install the module \n%test - check for operability \n%shutdown - shutdown the userbot \n%info - Userbot information" ,parse_mode="markdown")

@app.on_message(filters.command("restart", prefixes="%") & filters.me)
async def reboot(client, message):
    import os
    import sys
    await message.edit_text("Restarting")
    sleep(2.0)
    await message.edit_text("Restarted!")
    os.execl(sys.executable, sys.executable, *sys.argv)

@app.on_message(filters.command("shutdown", prefixes="%") & filters.me)
async def shutdown(client, message):
    import sys
    await message.edit_text("Turned off")
    print("Turned off from chat")
    sys.exit()


@app.on_message(filters.command("insmod", prefixes="%") & filters.me)
async def downloadmodule(client, message):
    args = message.text.split(" ")
    import os
    import requests
    import json
    if args[1] == "usage":
        await message.edit_text("Usage:\n%insmod {module url} {OPTIONAL:module name}\nModule class:core\nDescription:download and install modules. TODO: depedency resolving")
    elif len(args) > 3:
        await message.edit_text("Please, choose ONE module name.")
    elif len(args) < 2:
        await message.edit_text("I need link for download")
    else:
        if len(args) == 2:
            link = args[1].split("/")
            name = link[len(link)-1]
        else:
            name = args[2]+".py"
        try:
            os.chdir("plugins")
        except FileNotFoundError:
            os.mkdir("plugins")
            os.chdir("plugins")
        with open(f"{name}", "w") as modfile:
            r = requests.get(args[1])
            fc = r.content.decode("UTF-8")
            modfile.write(fc)
            await message.edit_text(f"Module {name} installed")
        os.chdir("../")
        try:
            settings = fc.split('\'\'\'')[1]
            js = json.loads(settings)
            try:
                os.chdir("configs")
                with open(name.replace(".py", ".json"), "w") as jsonfile:
                    json.dump(js, jsonfile)
                os.chdir("../")
            except FileNotFoundError:
                os.mkdir("configs")
                os.chdir("configs")
                with open(name.replace(".py", ".json"), "w") as jsonfile:
                    json.dump(js, jsonfile)
                os.chdir("../")
        except IndexError:
            pass

@app.on_message(filters.command("info", prefixes="%") & filters.me)
async def info(client, message):
    await message.edit_text(f"[Painted Userbot](https://github.com/Painted-Cat-Tech/painted-userbot)\nVersion:0.3-indev",parse_mode="markdown")
    
app.run()
