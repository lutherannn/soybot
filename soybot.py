import discord, os, random, aiohttp, json
from discord.ext import commands, tasks
from dotenv import load_dotenv
from os.path import exists
from udpy import UrbanClient
from time import sleep

client = commands.Bot(command_prefix="!")

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
        await ctx.send(f"The wheel has chosen {random.choice(lines)}")
    except:
        print("File not found")


@client.event
async def on_message(message, *args):
    if message.content.lower().startswith("hey soybot"):
        try:
            with open("responses.txt", "r") as f:
                lines = f.readlines()
        except:
            print("File not found")
        await message.channel.send(random.choice(lines))
    await client.process_commands(message)

    if message.content.lower().startswith("cope") and not client.user.mentioned_in(
        message
    ):
        await message.delete()
        await message.channel.send(
            "https://c.tenor.com/fGAe4omlBhUAAAAS/cope-harder.gif"
        )

    if "cope" in message.content.lower() and client.user.mentioned_in(message):
        await message.channel.send("Let me cope, my wife's boyfriend bullied me today")


@client.command(name="source", description="Sends the link of the source code")
async def source(ctx):
    await ctx.send(f"Source code: https://github.com/lutherannn/soybot")


@client.command(
    name="archive",
    description="Saves the last message sent, usage: !archive <filename>",
)
async def archive(ctx, arg1):
    chan = client.get_channel(949158145689800747)
    lastMsg = await chan.history(limit=2).flatten()
    if not exists(f"{arg1}.txt"):
        with open(f"{arg1}.txt", "w") as f:
            print(str(lastMsg[1].content))
            f.write(str(lastMsg[1].content))
            f.close()
    else:
        used = []
        await ctx.send("Filename already exists")
        cwd = os.getcwd()
        for file in os.listdir(cwd):
            if file.endswith(".txt"):
                used.append(file)
        usedF = ", ".join(used)
        await ctx.send(f"used filenames: {usedF}")


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


@client.command(name="definition", description="gets the definition of a word")
async def definition(ctx, arg1):
    f = open("dictionary.json")
    data = json.load(f)
    try:
        await ctx.send(f"Definition of {arg1}: {data[arg1.upper()]}")
    except KeyError:
        await ctx.send(f"{arg1} not found in dictionary")


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
    chan = client.get_channel(949158145689800747)
    if random.randrange(1, 4) == 1:
        print("Quote")
        async with aiohttp.ClientSession() as session:
            async with session.get("https://zenquotes.io/api/random") as response:
                jData = json.loads(await response.text())
                quote = jData[0]["q"]
                await chan.send(quote)

#@tasks.loop(minutes=30)
@client.command(name = "quiz", description = "Sends a country or city and you have to give the corresponding capital city or country")
async def quiz(ctx):
    with open("questions.txt") as f:
        lines = f.readlines()
        question = random.choice(lines)
        if '"country"' in question:
            answer = lines[lines.index(question) + 1].replace('"city": ', "")
            question = question.replace('"country": ', "")
            answer = answer.replace('"', "")
            answer = answer.replace(",", "")
            question = question.replace('"', "")
            question = question.replace(",", "")
            await ctx.send(f"What is the capital of: {question}")
            sleep(10)
            await ctx.send(f"Answer: {answer}")
        if '"city"' in question:
            answer = lines[lines.index(question) - 1].replace('"country": ', "")
            question = question.replace('"city": ', "")
            answer = answer.replace('"', "")
            answer = answer.replace(",", "")
            question = question.replace('"', "")
            question = question.replace(",", "")
            await ctx.send(f"Which country has the capital city of: {question}")
            sleep(10)
            await ctx.send(f"Answer: {answer}")


@client.event
async def on_ready():
    print("connected")
    randomQuote.start()


load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
