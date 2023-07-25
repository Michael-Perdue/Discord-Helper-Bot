import discord
from discord.ext import commands
import os

class Bot(commands.Bot):

    def __init__(self):
        """
        This function sets the bot up to have the right intents and command prefixes
        along with defining a hardcoded set of cogs/extension to use
        """
        super().__init__(
            intents=discord.Intents.all(),
            command_prefix="!"
        )
        self.init_extensions = ["messaging","clock","moderation"]

    async def setup_hook(self):
        """
        This function is called upon the start of the bot and loads the cogs/extensions
        which lets the bot use all the commands of those cogs
        """
        for extension in self.init_extensions:
            await self.load_extension(extension)

    async def on_ready(self):
        """
        This function is called once the bot has been setup and it prints to the terminal that
        the bots name and all the servers that it has connected to.
        """
        botID = str(self.user)
        print(botID + " is online\n")
        print(botID + " has connected to:")
        for server in self.guilds:      # loops through all the servers that the bot is already setup to use
            print(" " + str(server))
        print("")

    async def on_command_error(self, ctx , error):
        """
        This function defines how the bot should deal with errors. Currently, it raises all errors apart
        from errors which come from the user calling a command that doesn't exist and this is dealt
        by messaging the user error, so they are aware
        :param ctx: context of a message
        :param error: the error raised by the message
        :return: raises an error
        """
        if isinstance(error,commands.CommandNotFound):
            # sends the user a message stating the command does not exist and logs to the terminal that an error occurred
            await ctx.send(str(ctx.message.author.mention) + " Error no command is found with the name \'" + ctx.message.content.replace("!","") + "\'")
            log_message(ctx,"Error unknown command \'" + ctx.message.content.replace("!","") + "\'\n")
        else:
            raise error


bot = Bot()

def log_message(ctx, message):
    """
    Neatly formats a log message given the context of the message and any additional info you want to log
    then prints this message to the terminal
    :param ctx: the context of a message
    :param message: a string of any additional information you want to log
    """
    print(message + "   sent by: " + str(ctx.message.author) + "\n   on server: " + str(ctx.guild))

def main():
    while True:
        bot.run(os.environ['TOKEN'])

if __name__ == '__main__':
    main()




