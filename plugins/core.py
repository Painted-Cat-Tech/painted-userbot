from pyrogram import Client,  filters
import requests
import os
import sys
import pickle


@Client.on_message(filters.command("test", prefixes="%") & filters.me)
async def test(client, message):
    await message.edit_text("Works good")


@Client.on_message(filters.command("restart", prefixes="%") & filters.me)
async def reboot(client, message):
    await message.edit_text("Rebooting")
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.command("downmod", prefixes="%") & filters.me)
async def downloadmodule(client, message):
    args = message.text.split(" ")
    os.chdir("./plugins")
    if args[1] == "usage":
        await message.edit_text("Usage:\n%downmod {module url} {module name}\nModule class:core\nDescription:download and install modules. TODO: depedency resolving")
    elif len(args)<3:
        await message.edit_text("Too few arguments")
    elif len(args) > 3:
        await message.edit_text("Please, choose ONE module name.")
    else:
        with open(f"{args[2]}.py", "wb") as modfile:
            r = requests.get(args[1])
            pickle.dump(r.content, modfile)
            await message.edit_text(f"Module {args[2]}.py installed")
