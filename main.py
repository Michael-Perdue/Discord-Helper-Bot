# This is a sample Python script.
import asyncio

import discord
from discord.ext import commands
import os

#bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.all(),
            command_prefix="!"
        )
        self.initial_extensions = ["messaging"]

    async def setup_hook(self):
        for extension in self.initial_extensions:
            await self.load_extension(extension)

    async def on_ready(self):
        botID = str(self.user)
        print(botID + " is online")
        print(botID + " has connected to:")
        for server in self.guilds:
            print(" " + str(server))


bot = Bot()

async def load_extensions():
    await bot.load_extension('messaging')

def main():
    while True:
        bot.run(os.environ['TOKEN'])

if __name__ == '__main__':
    main()




