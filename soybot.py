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
from udpy import UrbanClient
from time import sleep
from math import floor
from modules import roll as mroll
from modules import roll20 as mroll20
from modules import wheel as mwheel
from modules import domath as mdomath
from modules import definition as mdefinition

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
    if message.content.lower().startswith(
        "hey soybot"
    ) and not message.content.lower().startswith("hey soybot choose"):
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
async def urban(ctx, arg1):
    ud = UrbanClient()
    defs = ud.get_definition(arg1)
    await ctx.send(f"Definition of {defs[0]}")


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


# Country/State capital & vice versa quiz


@client.command(
    name="quiz",
    description="Sends a country or city and you have to give the corresponding capital city or country",
)
async def quiz(ctx):
    with open("questions.txt") as f:
        lines = f.readlines()
        question = random.choice(lines)
        if "country" in question:
            answer = lines[lines.index(question) + 1].replace("city ", "")
            question = question.replace("country ", "")
            await ctx.send(f"What is the capital of: {question}")
            sleep(10)
            await ctx.send(f"Answer: {answer}")
        if "city" in question:
            answer = lines[lines.index(question) - 1].replace("country ", "")
            question = question.replace("city ", "")
            await ctx.send(f"Which country/state has the capital city of: {question}")
            sleep(10)
            await ctx.send(f"Answer: {answer}")


# Math quiz


@client.command(name="mquiz", description="Math quiz")
async def mquiz(ctx):
    ops = ["+", "-", "*"]
    num1, num2 = random.randrange(1, 100), random.randrange(1, 100)
    operator = random.choice(ops)
    await ctx.send(f"What is: {num1} {operator} {num2}")
    if num1 == 69 or num2 == 69:
        await ctx.send("Funny sex number lmao")
    if operator == "+":
        answer = num1 + num2
    if operator == "-":
        answer = num1 - num2
    if operator == "*":
        answer = num1 * num2
    sleep(5)
    await ctx.send(f"Solution: {answer}")


# Uploads message contents to hastebin


@client.command(name="hastebin", description="Sends text to hastebin")
async def hastebin(ctx, *, message):
    postData = hastebinapi.HasteBinApi(message)
    await ctx.send(f"<https://www.toptal.com/developers/hastebin/{postData.getKey()}>")


# Sends uptime of bot


@client.command(name="uptime", description="Sends the uptime of the bot")
async def uptime(ctx):
    global ts
    await ctx.send(f"Probably up since: {ts}")


# Picks random item from user sent list


@client.command(name="choose", description="Chooses a random item from the given list")
async def choose(ctx, *, options):
    r = [x for x in options.split(",")]
    await ctx.send(random.choice(r)) if len(r) > 1 else await ctx.send(
        "Choice requires more than one option."
    )


# Sends the wearher of a given city
@client.command(name="weather", description="Prints the weather of the specified city")
async def weather(ctx, *, message):
    url = (
        "http://api.openweathermap.org/data/2.5/weather?appid="
        + os.getenv("TEST")
        + "&q="
        + message
    )
    resp = requests.get(url)
    cont = resp.json()

    if cont["cod"] != "404":
        weatherData = cont["main"]
        temp = weatherData["temp"]
        temp = floor((temp - 273.15) * 1.8 + 32)
        await ctx.send(f"Temperature in {message.title()}: {str(temp)}")
    else:
        await ctx.send("City not found, or openweathermap is down")


# Plays a game of russian roulette
@client.command(name="soyroulette", description="Plays a game of russian roulette.")
async def soyroulette(ctx):
    loc = random.randrange(0, 7)
    await ctx.send("BANG!" if loc == 6 else "Click.")
    await ctx.send(
        f"You were {abs(loc - 6)} clicks away from death." if loc != 6 else ""
    )


# Plays a game of rock paper scissors
@client.command(name="rps", description="Plays a game of rock paper scissors")
async def rps(ctx, userChoice):
    choices = ["Rock", "Paper", "Scissors"]
    validChoice = False
    userWin = False
    cpuWin = False
    tie = False
    userChoice = userChoice.title()
    if userChoice not in choices:
        await ctx.send("You did not enter a correct choice.")
    else:
        validChoice = True
    if validChoice:
        cpuChoice = random.choice(choices)
        if userChoice == choices[0] and cpuChoice == choices[2]:
            userWin = True
        if userChoice == choices[1] and cpuChoice == choices[0]:
            userWin = True
        if userChoice == choices[2] and cpuChoice == choices[1]:
            userWin = True
        if cpuChoice == choices[0] and userChoice == choices[2]:
            cpuWin = True
        if cpuChoice == choices[1] and userChoice == choices[0]:
            cpuWin = True
        if cpuChoice == choices[2] and userChoice == choices[1]:
            cpuWin = True
        if userChoice == cpuChoice:
            tie = True

        if cpuWin and not tie:
            await ctx.send(f"I chose {cpuChoice}, I win!")
        if userWin and not tie:
            await ctx.send(f"I chose {cpuChoice}, you win, incel.")
        if tie:
            await ctx.send(f"We both chose {cpuChoice}, we tied.")


# Calls an emergency meeting
@client.command(name="em", description="Calls an emergency meeting")
async def em(ctx):
    await ctx.send("@everyone Emergency meeting")
    await ctx.send("https://tenor.com/bpitK.gif")


# Sends METAR of an airport
@client.command(name="metar", description="Returns the metar of a given airport")
async def metar(ctx, arg1):
    chars = "[]'"
    metarKey = os.getenv("METAR_KEY")
    metarUrl = f"https://api.checkwx.com/metar/{str(arg1.upper())}?x-api-key={metarKey}"

    req = requests.get(metarUrl)

    try:
        req.raise_for_status()
        resp = json.loads(req.text)
    except requests.exceptions.HTTPError as e:
        print(e)

    result = str(resp["data"])

    for x in chars:
        result = result.replace(x, "")

    await ctx.send(result)


# Starts pre-requirements such as time stamp and the random quote event if used


@client.event
async def on_ready():
    global ts
    print("connected")
    randomQuote.start()
    ts = datetime.datetime.now()


# Starts the bot
client.run(os.getenv("DISCORD_TOKEN"))
