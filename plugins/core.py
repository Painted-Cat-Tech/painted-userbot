from pyrogram import Client,  filters
@Client.on_message(filters.command("test", prefixes="%") & filters.me)
async def test(client, message):
    await message.edit_text("Works good")
@Client.on_message(filters.command("restart", prefixes="%") & filters.me)
async def reboot(client,message):
	await message.edit_text("Rebooting")
	os.execl(sys.executable, sys.executable, *sys.argv)
