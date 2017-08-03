import discord
from discord.ext import commands
from .utils import checks
from .utils.dataIO import dataIO
from .utils import chat_formatting as cf
from __main__ import send_cmd_help

import asyncio
import os
import os.path
import aiohttp
import copy
import glob
from typing import List


class misc:
	"""Misc commands"""

	def __init__(self, bot):
		self.bot = bot
		self.report_base = "data/reports"

	@commands.command(hidden=True)
	async def summon(self):
		await self.bot.say("Who dares summon me?")

	@commands.command(pass_context=True)
	@checks.is_owner()
	async def logupload(self, ctx, link: str=None):
		"""Adds a new raid heroes log report.
		Upload the file as a discord attachment."""
		await self.bot.type()
		server = ctx.message.server
		attach = ctx.message.attachments
		if len(attach) > 1 or (attach and link):
			await self.bot.say(
				cf.error("Please only add one report at a time."))
			return
		url = ""
		filename = ""
		if attach:
			a = attach[0]
			url = a["url"]
			filename = a["filename"]
		elif link:
			url = "".join(link)
			filename = os.path.basename(
				"_".join(url.split()).replace("%20", "_"))
		else:
			await self.bot.say(
				cf.error("You must provide a Discord attachment."))
			return
		fileextension = os.path.splitext(filename)[1]
		if fileextension != '.html':
			await self.bot.say("That's not a report.")
			return
		filepath = os.path.join(self.report_base, filename)
		if os.path.splitext(filename)[0] in self._list_reports():
			await self.bot.say(
				cf.error("A report with that filename already exists."
						 " Please change the filename and try again."))
			return
		async with aiohttp.get(url) as new_sound:
			f = open(filepath, "wb")
			f.write(await new_sound.read())
			f.close()
		await self.bot.say(
			cf.info("Report {} added.".format(os.path.splitext(filename)[0])))

	"""async def rename_orun(self, ):
		while self is self.bot.get_cog("misc"):
			server = await self.bot.get_server('294578270064869377')
			user = await self.bot.get_user_info('202429404503212034')
			nickname = "Orun"
			#print(user.nick)
			try:
				if user.nick != nickname:
					await self.bot.change_nickname(user, nickname)
					#print("Renamed Orun")
			except discord.Forbidden:
				print("I cannot do that, I lack the "
								"\"Manage Nicknames\" permission.")
			await asyncio.sleep(30)"""

	def _list_reports(self) -> List[str]:
		return sorted(
			[os.path.splitext(s)[0] for s in os.listdir(os.path.join(
				self.report_base))],
				key=lambda s: s.lower())

def check_folders():
	folder = "data/reports"
	if not os.path.exists(folder):
		print("Creating {} folder...".format(folder))
		os.makedirs(folder)
	files = glob.glob(folder + '/*')
	for f in files:
		try:
			os.remove(f)
		except PermissionError:
			print("Could not delete file '{}'. "
					"Check your file permissions.".format(f))

def setup(bot):
	n = misc(bot)
	check_folders()
	loop = asyncio.get_event_loop()
	#loop.create_task(n.rename_orun())
	bot.add_cog(n)