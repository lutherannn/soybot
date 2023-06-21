import discord
import os
import random
import aiohttp
import json
import datetime
import requests
import hastebin as hastebinapi
from discord.ext import commands, tasks
from dotenv import load_dotenv
from os.path import exists
from time import sleep
from math import floor
from modules import roll as mroll
from modules import roll20 as mroll20
from modules import wheel as mwheel
from modules import domath as mdomath
from modules import definition as mdefinition
from modules import urban as murban
from modules import quiz as cquiz
from modules import mquiz as mmquiz
from modules import rps as mrps
from modules import weather as mweather
from modules import metar as mmetar

# Set command prefix
client = commands.Bot(command_prefix="!")

# Load the .env contents
load_dotenv()

# 4chan style post rolling for roll threads


@client.command(
    name="roll", description="Rolls a 4chan like post number for roll thread images"
)
async def roll(ctx):
    await ctx.send(mroll.roll())


@client.command(name="roll20", description="Rolls a d20")
async def roll20(ctx):
    n = mroll20.roll20()
    await ctx.send("Nat 20!" if n == 20 else n)


# Spin the wheel, choose a random name from a new line delimited text file named names.txt
@client.command(name="wheel", description="The wheel of fate")
async def wheel(ctx):
    await ctx.send(mwheel.wheel())


@client.event
async def on_message(message):
    if message.content.lower().startswith("hey soybot"):
        try:
            with open("responses.txt", "r") as f:
                lines = f.readlines()
        except:
            print("File not found")
        await message.channel.send(random.choice(lines))

    if message.content.lower().startswith("cope") and not client.user.mentioned_in(
        message
    ):
        await message.channel.send(
            "https://c.tenor.com/fGAe4omlBhUAAAAS/cope-harder.gif"
        )

    if "cope" in message.content.lower() and client.user.mentioned_in(message):
        await message.channel.send("Let me cope, my wife's boyfriend bullied me today")

    if message.content.startswith("O-H"):
        await message.channel.send("I-O")

    if message.content.startswith("RAIDER"):
        await message.channel.send("POWER")

    if message.content.startswith("BILLS"):
        await message.channel.send("MAFIA")

    await client.process_commands(message)


@client.command(name="source", description="Sends the link of the source code")
async def source(ctx):
    await ctx.send("Source code: https://github.com/lutherannn/soybot")


# Does math


@client.command(name="domath", description="Performs math operations")
async def domath(ctx, *args):
    await ctx.send(mdomath.domath(*args))


# Gets definition of word from local dictionary


@client.command(name="definition", description="gets the definition of a word")
async def definition(ctx, arg1):
    await ctx.send(mdefinition.definition(arg1))


# Gets definition of word from urban dictionary


@client.command(
    name="urban", description="gets the definition of a word on urban dictionary"
)
async def urban(ctx, *, arg1):
    await ctx.send(murban.urban(arg1))


# Country/State capital & vice versa quiz


@client.command(
    name="quiz",
    description="Sends a country or city and you have to give the corresponding capital city or country",
)
async def quiz(ctx):
    qa = cquiz.quiz()
    await ctx.send(qa[0])
    sleep(10)
    await ctx.send(qa[1])


# Math quiz


@client.command(name="mquiz", description="Math quiz")
async def mquiz(ctx):
    qa = mmquiz.mquiz()
    await ctx.send(qa[0])
    sleep(10)
    await ctx.send(qa[1])


# Uploads message contents to hastebin


@client.command(name="hastebin", description="Sends text to hastebin")
async def hastebin(ctx, *, message):
    postData = hastebinapi.HasteBinApi(message)
    await ctx.send(f"<https://www.toptal.com/developers/hastebin/{postData.getKey()}>")


# Sends uptime of bot


@client.command(name="uptime", description="Sends the uptime of the bot")
async def uptime(ctx):
    global ts
    await ctx.send(f"Probably up since: {ts:%d.%m.%Y %H:%M:%S}")


# Picks random item from user sent list


@client.command(name="choose", description="Chooses a random item from the given list")
async def choose(ctx, *, options):
    r = [x for x in options.split(",")]
    await ctx.send(random.choice(r)) if len(r) > 1 else await ctx.send(
        "Choice requires more than one option."
    )


# Sends the weather of a given city
@client.command(name="weather", description="Prints the weather of the specified city")
async def weather(ctx, *, message):
    await ctx.send(mweather.weather(message))


# Plays a game of russian roulette
@client.command(name="soyroulette", description="Plays a game of russian roulette.")
async def soyroulette(ctx):
    await ctx.send("BANG!" if random.randrange(1, 7) == 7 else "Click.")


# Plays a game of rock paper scissors
@client.command(name="rps", description="Plays a game of rock paper scissors")
async def rps(ctx, userChoice):
    await ctx.send(mrps.rps(userChoice))


# Calls an emergency meeting
@client.command(name="em", description="Calls an emergency meeting")
async def em(ctx):
    await ctx.send("@everyone Emergency meeting")
    await ctx.send("https://tenor.com/bpitK.gif")


# Sends METAR of an airport
@client.command(name="metar", description="Returns the metar of a given airport")
async def metar(ctx, arg1):
    await ctx.send(mmetar.metar(arg1))


@client.command(
    name="jam", decription="Sends a random song from a list of spotify track links"
)
async def jam(ctx, *args):
    if (
        len(args) == 2
        and args[0].lower() == "load"
        and "https://open.spotify.com/track/" in args[1]
    ):
        with open("songs.txt", "a+") as f:
            f.write("\n" + str(args[1]))
            f.close()
    else:
        with open("songs.txt", "r") as f:
            # instead of checking for dupes when you load a song into the list, we'll just convert it to a set and back lmfao
            # this does mean the file can get pretty large, but fuck it
            cringe = set(f.readlines())
            cringe = list(cringe)
            await ctx.send(random.choice(cringe))

@client.command(name="iam", description="sets your role to a range of days for tracking days since your last... whatever you want", pass_context=True)
async def iam(ctx, arg1):
    member = ctx.message.author
    if arg1 == "1-7":
        role = discord.utils.get(member.guild.roles, name= "Day 1-7")
    if arg1 == "8-14":
        role = discord.utils.get(member.guild.roles, name = "Day 8-14")
    if arg1 == "15-21":
        role = discord.utils.get(member.guild.roles, name = "Day 15-21")
    if arg1 == "22-60":
        role = discord.utils.get(member.guild.roles, name = "Day 22-60")
    if arg1 == "61+":
        role = discord.utils.get(member.guild.roles, name = "61+")
    await member.add_roles(role)

@client.command(name="iamn", description="removes the role set from the iam command", pass_context = True)
async def iamn(ctx, arg1):
    member = ctx.message.author
    if arg1 == "1-7":
        role = discord.utils.get(member.guild.roles, name = "Day 1-7")
    if arg1 == "8-14":
        role = discord.utils.get(member.guild.roles, name = "Day 8-14")
    if arg1 == "15-21":
        role = discord.utils.get(member.guild.roles, name = "Day 15-21")
    if arg1 == "22-60":
        role = discord.utils.get(member.guild.roles, name = "Day 22-60")
    if arg1 == "61+":
        role = discord.utils.get(member.guild.roles, name = "Day 61+")
    await member.remove_roles(role)

@tasks.loop(minutes=60)
async def randomQuote():
    if os.path.exists(".quote"):
        chan = client.get_channel(int(os.getenv("QUOTE_CHAN")))
        chance = random.randrange(1, 4)
        if chance == 1:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://zenquotes.io/api/random") as response:
                    jData = json.loads(await response.text())
                quote = jData[0]["q"]
                await chan.send(quote)


# Starts pre-requirements such as time stamp and the random quote event if used


@client.event
async def on_ready():
    global ts
    print("connected")
    randomQuote.start()
    ts = datetime.datetime.now()


# Starts the bot
client.run(os.getenv("DISCORD_TOKEN"))
