import discord, os, random, aiohttp, json, urllib.parse, urllib.request
from discord.ext import commands, tasks
from dotenv import load_dotenv
from pastebin import PastebinAPI

client = commands.Bot(command_prefix="!")

# 4chan style post rolling for roll threads
@client.command(
    name="roll", description="Rolls a 4chan like post number for roll thread images"
)
async def roll(ctx):
    dubs, trips, quads = False, False, False
    nums = []
    for _ in range(10):
        nums.append(str(random.randrange(0, 9)))

    await ctx.send("".join(nums))

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

    if dubs and not trips and not quads:
        await ctx.send("Dubs!")
    if trips and not dubs and not quads:
        await ctx.send("Trips!")
    if quads and not dubs and not trips:
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


@client.command(name="soyball", description="The 8 ball, but soy")
async def soyball(ctx):
    responses = []
    try:
        with open("responses.txt", "r") as f:
            for line in f:
                responses.append(line)
        await ctx.send(random.choice(responses))
    except:
        print("File not found")


@client.command(name="source", description="Sends the link of the source code")
async def source(ctx):
    await ctx.send(f"Source code: https://github.com/lutherannn/soybot")


@tasks.loop(minutes=30)
async def randomQuote(ctx):
    if random.randrange(1, 2) == 1:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://zenquotes.io/api/random") as response:
                jData = json.loads(await response.text())
                quote = jData[0]["q"]
                await ctx.send(quote)


@client.command(
    name="pastebin",
    description="Uploads the selected text to pastebin, use code tags for formatting!",
)
async def pastebin(ctx, arg1):

    PASTEBIN_URL = "http://pastebin.com/api/api_post.php"
    pastebin_vars = dict(
        api_dev_key=os.getenv("PASTEBIN_TOKEN"),
        api_paste_code=arg1,
    )
    await ctx.send(
        urllib.request.urlopen(
            PASTEBIN_URL, urllib.parse.urlencode(pastebin_vars).encode("utf8")
        ).read()
    )


load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
