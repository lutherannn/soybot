import discord, os, random, aiohttp, json
from discord.ext import commands, tasks
from dotenv import load_dotenv

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
    names = []
    try:
        with open("names.txt", "r") as f:
            for line in f:
                names.append(line)
        await ctx.send(f"The wheel has chosen {random.choice(names)}")
    except:
        print("File not found")


@client.event
async def on_message(message):
    if message.content.lower().startswith("hey soybot"):
        try:
            with open("responses.txt", "r") as f:
                lines = f.readlines()
        except:
            print("File not found")
        await message.channel.send(random.choice(lines))


@client.command(name="source", description="Sends the link of the source code")
async def source(ctx):
    await ctx.send(f"Source code: https://github.com/lutherannn/soybot")


@client.command(
    name="archive",
    description="Saves local text file of the last message the person who called the command sent",
)
async def archive(ctx, arg1, arg2):
    if arg1 == "save" or arg1 == "s":
        return 0
    else:
        await ctx.send("Invalid command. Usage: !archive save <filename>")


@tasks.loop(minutes=30)
async def randomQuote(ctx):
    if random.randrange(1, 2) == 1:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://zenquotes.io/api/random") as response:
                jData = json.loads(await response.text())
                quote = jData[0]["q"]
                await ctx.send(quote)


load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
