import discord
from discord.ext import commands
from .utils import checks
from __main__ import send_cmd_help


class misc:
	"""Misc commands"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def summon(self, ctx, key):
		"""Adds your key and associates it with your discord account"""
		await self.bot.say("Who dares summon me?")

def setup(bot):
		n = misc(bot)
		bot.add_cog(n)