import discord
from discord.ext import commands
from .utils import checks
from .utils.dataIO import dataIO
from .utils import chat_formatting as cf
from __main__ import send_cmd_help

import asyncio
import os
import os.path
import sys
import aiohttp
import copy
import glob
from typing import List
import subprocess
from threading import Thread
import shlex
import datetime

try:
	from Queue import Queue, Empty
except ImportError:
	from queue import Queue, Empty # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names

DEFAULT_HEADERS = {'User-Agent': "A GW2 Discord bot",
'Accept': 'application/json'}


class APIError(Exception):
	pass

class APIConnectionError(APIError):
	pass

class APIForbidden(APIError):
	pass

class APIBadRequest(APIError):
	pass

class ShinyAPIError(Exception):
	pass

class APIKeyError(APIError):
	pass

class APINotFound(APIError):
	pass


class misc:
	"""Misc commands"""

	def __init__(self, bot):
		self.bot = bot
		self.report_base = "data/reports"
		self.evtc_base = "data/reports"
		self.gandaracheck = True
		self.session = aiohttp.ClientSession(loop=self.bot.loop)

	def __unload(self):
		self.session.close()

	"""def enqueue_output(self, out, queue):
		for line in iter(out.readline, b''):
			queue.put(line)
		out.close()"""

	"""async def processevtc(self, command, file):
		This function runs a raid_heroes.exe to process a evtc file using a seperate thread so it isn't blocking
		subprocess.call([command, file])
		process = Popen(shlex.split(command), stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
		q = Queue()
		t = Thread(target=self.enqueue_output, args=(process.stdout, q))
		t.daemon = True
		t.start()
		boss = 'error'
		while True:
			try:
				output = q.get_nowait().decode()
			except Empty:
				if t.isAlive() == False and q.empty() == True:
					break
				else:
					pass
			else:
				if output:
					if len(output) > 1:
						try:
							await self.bot.say(output)
						except:
							pass
					if 'Samarog' in output:
						boss = '_sam'
					if 'Sabetha' in output:
						boss = '_sab'
					if 'Overseer' in output:
						boss = '_mo'
					if 'Deimos' in output:
						boss = '_dei'
					if 'Vale' in output:
						boss = '_vg'
					if 'Gorseval' in output:
						boss = '_gor'
					if 'Matthias' in output:
						boss = '_mat'
					if 'Construct' in output:
						boss = '_kc'
					if 'Xera' in output:
						boss = '_xer'
					if 'Cairn' in output:
						boss = '_cai'
		return boss"""

	@commands.command(hidden=True)
	async def summon(self):
		await self.bot.say("Who dares summon me?")

	"""@commands.command(pass_context=True)
	@checks.is_owner()
	async def logprocess(self, ctx, link: str=None):
		Process an arcdps .evtc file with raid heroes.
		Upload the file as a discord attachment.
		await self.bot.type()
		server = ctx.message.server
		channel = ctx.message.channel
		attach = ctx.message.attachments
		if len(attach) > 1 or (attach and link):
			await self.bot.say(
				cf.error("Please only add one evtc file at a time."))
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
		if fileextension != '.evtc':
			await self.bot.say("That's not a evtc file.")
			return
		splitfilename = os.path.splitext(filename)[0]
		splitfilename = splitfilename.replace('-','')
		if splitfilename.isalnum() != True:
			await self.bot.say("That's an invalid file name.")
			return
		filepath = os.path.join(self.evtc_base, filename)
		if os.path.splitext(filename)[0] in self._list_evtc():
			pass
		else:
			async with aiohttp.get(url) as new_evtc:
				f = open(filepath, "wb")
				f.write(await new_evtc.read())
				f.close()
		message = await self.bot.say("Processing...")
		file = '/home/ubuntu/Red-DiscordBot/data/reports/' + filename
		command = '/home/ubuntu/raid_heroes'
		await self.processevtc(command, file)
		await asyncio.sleep(180)
		os.remove(file)
		#linktofile = 'redballslair.uk/raidbossreports/reports/' + os.path.splitext(filename)[0] + boss + '.html'
		#await self.bot.say(linktofile)
		#await self.bot.send_file(channel, output)"""

	@commands.command(pass_context=True)
	@checks.is_owner()
	async def logupload(self, ctx, link: str=None):
		"""Adds a new raid heroes log report.
		Upload the file as a discord attachment."""
		await self.bot.type()
		message = ctx.message
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
		async with aiohttp.get(url) as new_report:
			f = open(filepath, "wb")
			f.write(await new_report.read())
			f.close()
		url = 'http://redballslair.uk/raidbossreports/reports/' + filename
		try:
			await self.bot.delete_message(message)
		except:
			pass
		await self.bot.say("Report added. URL: {0}".format(url))


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

	def _list_evtc(self) -> List[str]:
		return sorted(
			[os.path.splitext(s)[0] for s in os.listdir(os.path.join(
				self.evtc_base))],
				key=lambda s: s.lower())

	async def getworldid(self, world):
		if world is None:
			return None
		try:
			endpoint = "worlds?ids=all"
			results = await self.call_api(endpoint)
		except APIError:
			return None
		for w in results:
			if w["name"].lower() == world.lower():
				return w["id"]
		return None

	async def call_api(self, endpoint, headers=DEFAULT_HEADERS):
		apiserv = 'https://api.guildwars2.com/v2/'
		url = apiserv + endpoint
		"""try:
			result = await self.session.get(url, headers=headers)
		except:
			raise APIConnectionError("API appears to be down.")"""
		async with self.session.get(url, headers=headers) as r:
			if r.status != 200 and r.status != 206:
				if r.status == 400:
					raise APIBadRequest("No ongoing transactions")
				if r.status == 404:
					raise APINotFound("Not found")
				if r.status == 403:
					raise APIForbidden("Access denied")
				if r.status == 429:
					print (time.strftime('%a %H:%M:%S'), "Api call limit reached")
					raise APIConnectionError(
						"Requests limit has been achieved. Try again later.")
				else:
					raise APIConnectionError(str(r.status))
			results = await r.json()
		return results

	async def gandarafullcheck(self):
		while self is self.bot.get_cog("misc"):
			if self.gandaracheck == True:
				world = 'Gandara'
				wid = await self.getworldid(world)
				try:
					endpoint_ = "worlds?id={0}".format(wid)
					worldinfo = await self.call_api(endpoint_)
					worldname = worldinfo["name"]
					population = worldinfo["population"]
				except APIError as e:
					return
				if population != 'Full':
					userid = '73569608572870656'
					user = await self.bot.get_user_info(userid)
					await self.bot.send_message(user, "Gandara is currently not full!")
					await asyncio.sleep(300)
					self.gandaracheck = False
				else:
					await asyncio.sleep(300)
			else:
				await asyncio.sleep(1800)

	async def timetopof(self):
		while self is self.bot.get_cog("misc"):
			poflaunch = datetime.datetime(2017, 9, 22, 16) - datetime.datetime.utcnow()
			if poflaunch.total_seconds() < 0:
				await self.bot.change_presence(game=discord.Game(name="Path of Fire is out!"), status=discord.Status.online)
				await asyncio.sleep(3000)
			else:
				hours = poflaunch.total_seconds() / 3600
				minutes = (hours % 1) * 60
				time = "{:02d}h{:02d}m".format(int(hours), int(minutes))
				game = time  + ' until PoF!'
				await self.bot.change_presence(game=discord.Game(name=game),status=discord.Status.online)
				await asyncio.sleep(30)
		
def check_folders():
	folder = "data/reports/toprocess"
	if not os.path.exists(folder):
		print("Creating {} folder...".format(folder))
		os.makedirs(folder)

def setup(bot):
	n = misc(bot)
	check_folders()
	loop = asyncio.get_event_loop()
	loop.create_task(n.gandarafullcheck())
	loop.create_task(n.timetopof())
	bot.add_cog(n)