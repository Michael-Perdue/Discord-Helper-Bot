import discord
from discord.ext import commands
import os


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.all(),
            command_prefix="!"
        )
        self.init_extensions = ["messaging","clock","moderation"]

    async def setup_hook(self):
        for extension in self.init_extensions:
            await self.load_extension(extension)

    async def on_ready(self):
        botID = str(self.user)
        print(botID + " is online\n")
        print(botID + " has connected to:")
        for server in self.guilds:
            print(" " + str(server))
        print("")

    async def on_command_error(self, ctx , error):
        if isinstance(error,commands.CommandNotFound):
            await ctx.send(str(ctx.message.author.mention) + " Error no command is found with the name \'" + ctx.message.content.replace("!","") + "\'")
            log_message(ctx,"Error unknown command \'" + ctx.message.content.replace("!","") + "\'\n")
        else:
            raise error


bot = Bot()

def log_message(ctx, message):
    print(message + "   sent by: " + str(ctx.message.author) + "\n   on server: " + str(ctx.guild))

def main():
    while True:
        bot.run(os.environ['TOKEN'])

if __name__ == '__main__':
    main()




