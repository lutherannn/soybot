import discord, os, random
from discord.ext import commands
from dotenv import load_dotenv

client = commands.Bot(command_prefix="!")

# 4chan style post rolling for roll threads
@client.command()
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


load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
