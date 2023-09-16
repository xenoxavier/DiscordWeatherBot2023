import discord
from discord.ext import commands

from apis import *

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    print("Logged in as {bot.user.name}")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")


@bot.command()
async def react(ctx):
    await ctx.send("Im feeling excited!")
    await ctx.messsage.add_reaction(":tada:")

bot.run(TOKEN)