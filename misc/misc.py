import discord
from discord.ext import commands
from .utils import checks
from __main__ import send_cmd_help

import asyncio


class misc:
	"""Misc commands"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden=True)
	async def summon(self):
		await self.bot.say("Who dares summon me?")

	async def rename_orun(self):
		while self is self.bot.get_cog("misc"):
			orun_id = 202429404503212034
			user = await self.bot.get_user_info(orun_id)
			nickname = "Orun"
			try:
				await self.bot.change_nickname(user, nickname)
			except discord.Forbidden:
				print("I cannot do that, I lack the "
								"\"Manage Nicknames\" permission.")
			await asyncio.sleep(30)

def setup(bot):
	n = misc(bot)
	loop = asyncio.get_event_loop()
	loop.create_task(n.rename_orun())
	bot.add_cog(n)