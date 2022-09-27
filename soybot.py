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

# Set command prefix
client = commands.Bot(command_prefix="!")

# Load the .env contents
load_dotenv()

# 4chan style post rolling for roll threads


@client.command(
    name="roll", description="Rolls a 4chan like post number for roll thread images"
)
async def roll(ctx):
    dubs, trips, quads = False, False, False
    nums = ""
    for _ in range(10):
        nums += str(random.randrange(0, 9))
    await ctx.send(nums)

    if nums[-1] == nums[-2]:
        dubs = True
    if nums[-1] == nums[-2] and nums[-1] == nums[-3]:
        trips = True
    if nums[-1] == nums[-2] and nums[-1] == nums[-3] and nums[-1] == nums[-4]:
        quads = True

    if dubs and trips:
        dubs = False
    if quads and trips:
        trips = False

    if dubs:
        await ctx.send("Dubs!")
    if trips:
        await ctx.send("Trips!")
    if quads:
        await ctx.send("Quads!")


# Spin the wheel, choose a random name from a new line delimited text file named names.txt
@client.command(name="wheel", description="The wheel of fate")
async def wheel(ctx):
    try:
        with open("names.txt", "r") as f:
            lines = f.readlines()
            f.close()
        await ctx.send(f"The wheel has chosen {random.choice(lines)}")
    except:
        print("File not found")


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


# Archives last message sent to local disc


@client.command(
    name="archive",
    description="Saves the last message sent, usage: !archive <filename>",
)
async def archive(ctx, arg1, arg2):
    chan = client.get_channel(int(os.getenv("QUOTE_CHAN")))
    lastMsg = await chan.history(limit=2).flatten()
    used = []
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith(".txt"):
            used.append(file)
    usedF = ", ".join(used)
    if arg1 == "load" or arg1 == "lo":
        try:
            with open(f"{arg2}.txt") as f:
                content = f.readlines()
                await ctx.send(" ".join(content))
                f.close()
        except FileNotFoundError:
            await ctx.send("Filename not found.")
            await ctx.send(f"Used filenames: {usedF}")
    if arg1 == "save" or arg1 == "s":
        if not exists(f"{arg2}.txt"):
            with open(f"{arg2}.txt", "w") as f:
                f.write(str(lastMsg[1].content))
                f.close()
                await ctx.send(f"File saved as: {arg2}.txt")
        else:
            await ctx.send("Filename already exists")
            await ctx.send(f"Used filenames: {usedF}")
    if arg1 == "list" or arg1 == "li":
        await ctx.send(f"Used filenames: {usedF}")
    else:
        await ctx.send(
            "Invalid usage. Correct usage: !archive <(s)ave>/<(lo)ad>/<(li)st> <filename>"
        )


# Does math


@client.command(name="domath", description="Performs math operations")
async def domath(ctx, *args):
    nums = list(args)
    nums.remove(nums[0])
    nums = [int(x) for x in nums]
    if args[0] == "add" or args[0] == "a":
        await ctx.send(sum(nums))
    if args[0] == "subtract" or args[0] == "s":
        await ctx.send(nums[0] - nums[1])
    if args[0] == "multiply" or args[0] == "m":
        for x in nums:
            r = 1
            for x in nums:
                r = r * x
        await ctx.send(r)
    if args[0] == "divide" or args[0] == "d":
        await ctx.send(nums[0] // nums[1])


# Gets definition of word from local dictionary


@client.command(name="definition", description="gets the definition of a word")
async def definition(ctx, arg1):
    f = open("dictionary.json")
    data = json.load(f)
    try:
        await ctx.send(f"Definition of {arg1}: {data[arg1.upper()]}")
    except KeyError:
        await ctx.send(f"{arg1} not found in dictionary")
    f.close()


# Gets definition of word from urban dictionary


@client.command(
    name="urban", description="gets the definition of a word on urban dictionary"
)
async def urban(ctx, arg1):
    ud = UrbanClient()
    defs = ud.get_definition(arg1)
    for d in defs:
        await ctx.send(f"Definition of word: {d}")


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
    r = [x for x in options.split()]
    await ctx.send(random.choice(r)) if len(r) > 1 else await ctx.send(
        "Choice requires more than one option."
    )


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


@client.command(name="soyroulette", description="Plays a game of russian roulette.")
async def soyroulette(ctx):
    await ctx.send("BANG!" if random.randrage(1, 6) == 6 else "Click.")


# Starts pre-requirements such as time stamp and the random quote event if used


@client.event
async def on_ready():
    global ts
    print("connected")
    randomQuote.start()
    ts = datetime.datetime.now()


# Starts the bot
client.run(os.getenv("DISCORD_TOKEN"))
