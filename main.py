# This is a sample Python script.
import discord
import os

bot = discord.Client(intents=discord.Intents.default())

@bot.event
async def on_ready():
    botID = str(bot.user)
    print(botID + " is online")
    print(botID + " has connected to:")
    for server in bot.guilds:
        print(" " + str(server))


if __name__ == '__main__':
    bot.run(os.environ['TOKEN'])

