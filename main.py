import discord
from discord.ext import commands
import requests
import datetime as dt



from apis import *

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9 / 5) + 32
    return celsius, fahrenheit

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print("Logged in as {bot.user.name}")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")

@bot.command()
async def weather(ctx, city):
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()

    temp_kelvin = response['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)

    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
    wind_speed = response['wind']['speed']
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']
    sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

  # Create a Discord embed
    embed = discord.Embed(title=f"Weather in {city}", color=discord.Color.blue())
    embed.add_field(name="Temperature", value=f"{temp_celsius:.2f}°C / {temp_fahrenheit:.2f}°F", inline=False)
    embed.add_field(name="Feels Like", value=f"{feels_like_celsius:.2f}°C / {feels_like_fahrenheit:.2f}°F", inline=False)
    embed.add_field(name="Humidity", value=f"{humidity}%", inline=False)
    embed.add_field(name="Wind Speed", value=f"{wind_speed} m/s", inline=False)
    embed.add_field(name="General Weather", value=description, inline=False)
    embed.add_field(name="Sunrise", value=sunrise_time.strftime('%Y-%m-%d %H:%M:%S') + " local time", inline=False)
    embed.add_field(name="Sunset", value=sunset_time.strftime('%Y-%m-%d %H:%M:%S') + " local time", inline=False)

    await ctx.send(embed=embed)



@bot.command()
async def react(ctx):
    await ctx.send("I'm feeling excited!")
    await ctx.message.add_reaction("🎉")

bot.run(TOKEN)