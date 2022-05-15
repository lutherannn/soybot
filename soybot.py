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
            line = f.readlines()
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


@client.command(name="source", description="Sends the link of the source code")
async def source(ctx):
    await ctx.send(f"Source code: https://github.com/lutherannn/soybot")


@client.command(
    name="archive",
    description="Saves local text file of the last message the person who called the command sent",
)
async def archive(ctx, arg1):
    await ctx.send("Not yet implemented")


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


@tasks.loop(minutes=30)
async def randomQuote(ctx):
    chance = random.randrange(1, 2)
    if chance == 1:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://zenquotes.io/api/random") as response:
                jData = json.loads(await response.text())
                quote = jData[0]["q"]
                await ctx.send(quote)


load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
