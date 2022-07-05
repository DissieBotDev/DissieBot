import discord
from discord.ext import commands, tasks, bridge, pages
from discord import Option
from discord.ui import Button, View
import datetime
import time
import json
from json import load
from pathlib import Path
import asyncio
import os
import sys
import logging
import re
import requests
import psutil

description = ""

intents = discord.Intents.default()
intents.members = True

with Path(os.path.dirname(__file__)+os.path.sep+'config.json').open() as f:
    config = load(f)

url = requests.get("https://raw.githubusercontent.com/DissieBotDev/DissieBot/main/.github/version.json")
text = url.text
githubversionjson = json.loads(text)

TOKEN = config["TOKEN"]
PREFIX = config["PREFIX"]
VERSION = config["VERSION"]
VERSIONSDATUM = config["VERSIONSDATUM"]
AUTOR = config["AUTOR"]
BOTNAME = config["BOTNAME"]
#SERVERNAME = config["SERVERNAME"]

SOURCE_CODE_VERSION = githubversionjson["SOURCE_CODE_VERSION"]

OWNERS = config["OWNERS"]

bot = discord.Bot(command_prefix=PREFIX, description=description, intents=intents, owner_ids=set(OWNERS), status=discord.Status.dnd, messages=True, members=True)

async def status():
    while True:
        await bot.change_presence(activity=discord.Game(name=f"/help | von {AUTOR}"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name=f"Version {VERSION} vom {VERSIONSDATUM}"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ViennaPlay.eu"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="AlexanderWagnerDev.at"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="dissie.alexanderwagnerdev.at"))
        await asyncio.sleep(10)

timestamp = datetime.datetime.now()
#timestamp = datetime.datetime.utcnow()+datetime.timedelta(hours=2)

@bot.event
async def on_ready():
    print('------')
    print(f'Pycord Version: {discord.__version__}')
    print(f'Python Version: {sys.version}')
    print(f'Bot Version: {VERSION}')
    print(f'Bot Versionsdatum: {VERSIONSDATUM}')
    print(f'Bot Autor: {AUTOR}')
    print('------')
    print(f'Bot gestartet: {datetime.datetime.now()}')
    print(f'Angemeldet als {bot.user} (ID: {bot.user.id})')
    print('------')
    bot.loop.create_task(status())
    channel = bot.get_channel(993122628543991830)
    embedstart = discord.Embed(title="Bot ist online", color=0x00ff00)
    embedstart.add_field(name="Bot wurde gestartet", value=" ⠀ ", inline=False)
    embedstart.timestamp = timestamp
    embedstart.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await channel.send(embed=embedstart)

start_time = time.time()
UPTIME = str(datetime.timedelta(seconds=int(round(time.time()-start_time))))

DATE = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
LOG_DATE = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")

bot_log = open(os.path.dirname(__file__)+os.path.sep+f'/logs/bot/bot-botv{VERSION}-{DATE}.log', encoding='utf-8', mode='w')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=os.path.dirname(__file__)+os.path.sep+f'/logs/bot/bot-botv{VERSION}-{DATE}.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#async def

async def allusers(user):
    users = await loadAllUsersData()

    if str(user.id) in users:
        return False
    else:
        users[str(user)] = {}
        users[str(user.id)] = {}
        users[str(user.id)]["roles"] = user.roles

    with open(os.path.dirname(__file__)+os.path.sep+'data/users.json', 'w') as f:
        json.dump(users, f)

    return True

async def loadAllUsersData():
    with open(os.path.dirname(__file__)+os.path.sep+'data/users.json', 'r') as f:
        users = json.load(f)
    return users

def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.slash_command(name ="hallo", aliases=["hello", "moin", "hi", "Hallo", "Hello", "Moin", "Hi"], description="Sagt hallo!")
async def hallo(ctx):
    #allusers(ctx.author)
    embedhello = discord.Embed(title="Hallo", color=0xffff00)
    embedhello.set_thumbnail(url="https://cdn.pixabay.com/photo/2016/10/26/13/09/bird-1771435_960_720.png")
    embedhello.add_field(name="Moin", value="Wie geht es dir?", inline=True)
    embedhello.timestamp = timestamp
    embedhello.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.respond(embed=embedhello)

@bot.slash_command(name="ping", aliases=["pong"], discription="Zeigt die Reaktionsdauer an")
async def ping(ctx):
    bot_latency = round(bot.latency * 1000)
    embedlade = discord.Embed(title="Lade", color=0xffff00)
    embedlade.add_field(name="Lade...", value=" ⠀ ", inline=True)
    embedlade.timestamp = timestamp
    embedlade.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.send(embed=embedlade, delete_after=0.5)
    async with ctx.typing():
        await asyncio.sleep(0.5)
    embedping = discord.Embed(title="Pong", color=0x00ff00)
    embedping.add_field(name=f'Mein Ping ist {bot_latency}ms  :ping_pong:', value='\u200b', inline=True)
    embedping.timestamp = timestamp
    embedping.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.respond(embed=embedping)

@bot.slash_command(name="userinfo", aliases=["ui", "UserInfo", "Userinfo", "UI", "Ui", "uI"], discription="Informationen über den User")
async def userinfo(ctx, user: Option(discord.User, description="User über den die Infos angezeigt werden soll", required=True)):
    embedlade = discord.Embed(title="Lade", color=0xffff00)
    embedlade.add_field(name="Lade...", value=" ⠀ ", inline=True)
    embedlade.timestamp = timestamp
    embedlade.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.send(embed=embedlade, delete_after=1)
    async with ctx.typing():
        await asyncio.sleep(1)
    embeduserinfo = discord.Embed(title="Userinfo", color=0x00ff00)
    embeduserinfo.add_field(name="Name", value=user.name, inline=False)
    embeduserinfo.set_thumbnail(url=user.avatar)
    embeduserinfo.add_field(name="Discord-ID", value=user.id, inline=False)
    embeduserinfo.add_field(name="Discord-Tag", value=user.discriminator, inline=False)
    embeduserinfo.add_field(name="Bot", value=user.bot, inline=False)
    #embeduserinfo.add_field(name="Status", value=user.status, inline=False)
    embeduserinfo.add_field(name="Rolle", value=user.roles, inline=False)
    embeduserinfo.add_field(name="Erstellt am", value=user.created_at, inline=False)
    embeduserinfo.timestamp = timestamp
    embeduserinfo.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.respond(embed=embeduserinfo)

@bot.slash_command(name="info", aliases=["i", "Info", "I"], discription="Informationen über den Bot")
async def info(ctx):
    invitebutton = Button(label="Invite", style=discord.ButtonStyle.primary, url="https://discord.com/api/oauth2/authorize?client_id=993118343861121104&permissions=1541826669815&scope=bot")
    view = View()
    view.add_item(invitebutton)
    embedinfo = discord.Embed(title="Informationen", color=0xff8000)
    embedinfo.add_field(name="Version:", value=f"{VERSION} vom {VERSIONSDATUM}\n", inline=False)
    embedinfo.add_field(name="Autor:", value=f"{AUTOR} \n", inline=False)
    embedinfo.timestamp = timestamp
    embedinfo.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.respond(embed=embedinfo, view=view)

@bot.slash_command(name="source", aliases=[], discription="Source Code des Bots")
async def source(ctx):
    embedsource = discord.Embed(title="Source Code", color=0x00ff00)
    embedsource.add_field(name="Code:", value=f"https://github.com/DissieBotDev/DissieBot", inline=False)
    embedsource.add_field(name="Source Code Version:", value=f"{SOURCE_CODE_VERSION} \n", inline=False)
    embedsource.timestamp = timestamp
    embedsource.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.respond(embed=embedsource)

@bot.slash_command(name="print", aliases=["p", "Print", "P"], discription="Printent den übergebenen Wert aus")
async def print(ctx, text: Option(str, description="Text to print", required=True)):
    await ctx.respond(text)

@bot.slash_command(name="embedprint", aliases=["EmbedPrint"], discription="Printent den übergebenen Wert in einen Embed aus")
async def embedprint(ctx, color: Option(str, description="Hex-Code der Farbe", required=True), title: Option(str, description="Titel", required=True), text: Option(str, description="Text", required=True)):
    embedprint = discord.Embed(title=title, color=color)
    embedprint.add_field(name=text, value=" ⠀ ", inline=False)
    embedprint.timestamp = timestamp
    embedprint.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.respond(embed=embedprint)

@bot.slash_command(name="uptime", aliases=["ut", "Uptime", "UT"], discription="Zeigt die Uptime an")
async def uptime(ctx):
    current_time = time.time()
    difference = int(round(current_time - start_time))
    UPTIME = str(datetime.timedelta(seconds=difference))
    embeduptime = discord.Embed(title="Uptime", color=0x00ff00)
    embeduptime.add_field(name="Uptime:", value=f"{UPTIME}", inline=False)
    embeduptime.timestamp = timestamp
    embeduptime.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.respond(embed=embeduptime)

@bot.slash_command(name="clear", aliases=["delete", "purge", "c"], discription="Löscht Nachrichten")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int=None):
    if amount == None:
        await ctx.channel.purge(limit=1000)
    else:
        try:
            int(amount)
        except:
            await ctx.respond('Bitte gebe eine gültige Ganzzahl an.')
        else:
            await ctx.channel.purge(limit=amount)
    embedclear = discord.Embed(title="Clear", color=0x00ff00)
    if amount == 1:
        embedclear.add_field(name=f"{amount} Nachricht gelöscht!", value=" ⠀ ", inline=False)
    else:
        embedclear.add_field(name=f"Ich habe {amount} Nachrichten gelöscht!", value=" ⠀ ", inline=False)
        embedclear.timestamp = timestamp
        embedclear.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.respond(embed=embedclear, delete_after=5)

@bot.slash_command(name="restart", aliases=["r", "R"], discription="Bot neustarten")
@commands.is_owner()
async def restart(ctx):
    embedrestart = discord.Embed(title="Neustart", color=0xff0000)
    embedrestart.add_field(name="Bot startet neu...", value="Ich bin gleich wieder erreichbar!", inline=True)
    embedrestart.timestamp = timestamp
    embedrestart.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.respond(embed=embedrestart)
    await bot.change_presence(status=discord.Status.dnd)
    restart_bot()

@bot.slash_command(name="ban", discription="Ein Mitglied bannen")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User=None, reason=None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("Du kannst dich nicht selber bannen")
        return
    if reason == None:
        reason = "Dafür, dass du dich nicht an die Regeln gehalten hast!"
    message = f"Du wurdest von {ctx.guild.name} wegen {reason} gebannt."
    await member.send(message)
    await ctx.guild.ban(member, reason=reason)
    await ctx.channel.respond(f"{member} wurde gebannt!")

@bot.slash_command(name="kick", discription="Ein Mitglied kicken")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.User=None, reason: Option(str, description="Grund", required=True)=None):
    if member == None or member == ctx.message.author:
        await ctx.channel.respond("Du kannst dich nicht selber kicken")
        return
    if reason == None:
        reason = "Dafür, dass du dich nicht an die Regeln gehalten hast!"
    message = f"Du wurdest von {ctx.guild.name} wegen {reason} gekickt."
    await member.send(message)
    await ctx.guild.kick(member, reason=reason)
    await ctx.channel.respond(f"{member} wurde gekickt!")

@bot.slash_command(name ="stats", aliases=[], description="Zeigt die Statistiken an")
async def stats(ctx):
    embedlade = discord.Embed(title="Lade", color=0xffff00)
    embedlade.add_field(name="Lade...", value=" ⠀ ", inline=True)
    embedlade.timestamp = timestamp
    embedlade.set_footer(text=f'{BOTNAME} von {AUTOR}',
                         icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.send(embed=embedlade, delete_after=1)
    cpuussage = psutil.cpu_percent(1)
    ramusage = psutil.virtual_memory().percent
    ramused = psutil.virtual_memory().used >> 20
    ramtotal = psutil.virtual_memory().total >> 20
    cpucores = psutil.cpu_count()
    async with ctx.typing():
        await asyncio.sleep(1)
    embedstats = discord.Embed(title="Statistiken", color=0xffff00)
    embedstats.add_field(name="CPU", value=f'{cpuussage}%', inline=False)
    embedstats.add_field(name="RAM", value=f'{ramusage}%', inline=False)
    embedstats.add_field(name="RAM in Used", value=f'{ramused}/{ramtotal} MB', inline=False)
    embedstats.add_field(name="CPU Cores", value=f'{cpucores}', inline=False)
    embedstats.timestamp = timestamp
    embedstats.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.respond(embed=embedstats)

@bot.slash_command(name="helpmod", aliases=["hilfemod", "Hilfemod", "hmod", "Hmod", "HM", "hm"], discription="Zeigt alle Befehle für Moderator und höher an")
@commands.has_permissions(kick_members=True)
async def helpmod(ctx):
    embedhelpmod = discord.Embed(title="Hilfe für Moderatoren", color=0xffff00)
    embedhelpmod.add_field(name="Clear", value=f"Befehl: `{PREFIX}clear` \n Löscht Nachrichten (gesendetet Nachricht wird mitgezählt) \n", inline=True)
    embedhelpmod.add_field(name="Kicken", value=f"Befehl: `{PREFIX}kick Mitglied Grund` \n Kickt ein Mitglied \n", inline=True)
    embedhelpmod.add_field(name="Ban", value=f"Befehl: `{PREFIX}ban Mitglied Grund` \n Bannt ein Mitglied \n", inline=True)
    embedhelpmod.add_field(name="Restart", value=f"Befehl: `{PREFIX}restart` \n Startet den Bot neu \n", inline=True)
    embedhelpmod.add_field(name="Hilfe", value=f"Befehl: `{PREFIX}helpmod` \n Zeigt diese Hilfe an \n", inline=True)
    embedhelpmod.timestamp = timestamp
    embedhelpmod.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.respond(embed=embedhelpmod)

@bot.slash_command(name="help", aliases=["hilfe", "Hilfe", "h", "H"], discription="Zeigt alle Befehle an")
async def help(ctx):
    embedhelp = discord.Embed(title="Hilfe", color=0xffff00)
    embedhelp.add_field(name="Hallo", value=f"Befehl: `/hello` \n Sagt Hallo! \n", inline=True)
    embedhelp.add_field(name="Ping", value=f"Befehl: `/ping` \n Zeigt die Reaktionsdauer an \n", inline=True)
    embedhelp.add_field(name="Info", value=f"Befehl: `/info` \n Zeigt Informationen über den Bot an \n", inline=True)
    embedhelp.add_field(name="Print", value=f"Befehl: `/print` \n Printent den übergebenen Wert aus \n", inline=True)
    embedhelp.add_field(name="Embed", value=f"Befehl: `/embed` \n Erstellt einen Embed \n", inline=True)
    embedhelp.add_field(name="Stats", value=f"Befehl: `/stats` \n Zeigt die Statistiken an \n", inline=True)
    embedhelp.add_field(name="Uptime", value=f"Befehl: `/uptime` \n Zeigt die Uptime an \n", inline=True)
    embedhelp.add_field(name="Source Code", value=f"Befehl: `/source` \n Source Code des Bots \n", inline=True)
    embedhelp.add_field(name="Hilfe", value=f"Befehl: `/help` \n Zeigt diese Hilfe an \n", inline=True)
    embedhelp.timestamp = timestamp
    embedhelp.set_footer(text=f'{BOTNAME} von {AUTOR}', icon_url="https://cdn.discordapp.com/attachments/993148355586830416/993488513070796850/Dissie_-_Logo_-_Transparent.png")
    await ctx.respond(embed=embedhelp)

bot.run(TOKEN)