import discord
from discord import Message
from discord.ext import commands
from pathlib import Path
import os
import re


class Bot(commands.Bot):
    banned_words = {}
    def __init__(self):
        """
        This function sets the bot up to have the right intents and command prefixes
        along with defining a hardcoded set of cogs/extension to use
        """
        super().__init__(
            intents=discord.Intents.all(),
            command_prefix="!",
            allowed_mentions=discord.AllowedMentions(everyone=True,roles=True,replied_user=True,users=True)
        )
        self.init_extensions = ["messaging","clock","moderation","fun"]


    async def setup_hook(self):
        """
        This function is called upon the start of the bot and loads the cogs/extensions
        which lets the bot use all the commands of those cogs
        """
        for extension in self.init_extensions:
            await self.load_extension(extension)

    def read_banned_words(self):
        if not Path("./banned_words.txt").is_file():
            #creates a new file through opening it on write
            open("banned_words.txt", "a").close()
        file = open("banned_words.txt","r")
        for x in file: # reads each line in the file
            split_line = list(x.replace("\n","").split(" ")) # splits the line into a list
            self.banned_words[int(split_line[0])] = split_line[1:]
        file.close()

    def add_guilds(self):
        file = open("banned_words.txt","a")
        found_guilds = self.banned_words.keys()
        for guild in self.guilds:
            if guild.id not in found_guilds:
                file.write(str(guild.id) + "\n")
                self.banned_words[guild.id] = []
        file.close()

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
        self.read_banned_words()
        self.add_guilds()
        print("Banned word list: " + str(self.banned_words))

    async def on_guild_join(self,guild):
        self.add_guilds()
        channel_found = False
        for channel in guild.text_channels:
            if channel.name == "moderation":
                channel_found = True
                break
        if channel_found == False:
            await guild.create_text_channel(name="moderation")
        print("Bot has been added to server: "+ str(guild))

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

    async def on_message(self, message: Message):
        if(message.author.id != self.user.id and "!unbanword" not in message.content):
            check_word = [word for word in self.banned_words[message.guild.id] if(re.search(("(^|\s)"+word+"($|\s)"),message.content))]
            if bool(check_word):
                await message.delete()
                await discord.utils.get(message.guild.channels, name="moderation").send(message.author.mention + " just tried to use banned word/s \'" + "\' \'".join(check_word) + "\' in channel: " + message.channel.mention )
            else:
                await self.process_commands(message)
        else:
            await self.process_commands(message)


bot = Bot()

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context) -> None:
    synced = await ctx.bot.tree.sync()
    await ctx.send("Synced "+str(len(synced))+" commands")
    log_message(ctx,"SYNC command used:\n   commands synced: " + str(len(synced)) + "\n")

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




