import asyncio
import typing
import discord
from discord.ext import commands
from main import log_message

class Messaging(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="test")
    async def test(self,ctx):
        """
        This function is simply for debugging to ensure the bot works
        when a user sends !test the bot responds with a message saying 'Test'.
        :param ctx: the context of the message
        """
        log_message(ctx,"Test command:\n")
        await ctx.send("Test")

    @commands.command(name="mirror")
    async def mirror(self,ctx,*args):
        """
        This function deals with a user sending a !mirror command and it simply sends whatever
        they send back to them.
        Example command: '!mirror this is a test' results in the bot messaging back 'this is a test'
        :param ctx: the context of the message
        :param args: the string the user sends with the command
        """
        message = " ".join(args)
        log_message(ctx,"Mirror command:\n   message: \'"+message+"\'\n")
        await ctx.send(message)

    @commands.command(name="spam")
    async def spam(self,ctx,*args):
        """
        This function deals with a user sending a !spam command, a mention of a user or group and a number.
        The bot will then mention the user or group the number of times it was told.
        Example command: '!spam @everyone 2' results in 2 messages by the bot of @everyone
        :param ctx: the context of the message
        :param args: the user or group you want to mention and the number of times you want the bot to mention them
        """
        log_message(ctx,"Spam command:\n   mentioned: "+str(args[0])+"\n   amount: " + str(args[1]) + "\n")
        for x in range(int(args[1])):
            await ctx.send(str(args[0]))
            await asyncio.sleep(0.2)    # waits 0.2 seconds as otherwise the responses seem delayed

    @commands.command(name="forward")
    async def forward(self, ctx,member: typing.Union[discord.Member,discord.Role], *message):
        """
        This function deals with a user sending a !forward command, and it simply sends whatever
        the users send to the person or group who they mention and the bot deletes their message, so it's anonymous.
        Example command: '!forward @user this is a test' results in the bot messaging back '@user this is a test'
        :param ctx: the context of the message
        :param member: the group or person the user wants to forward it to example @role
        :param message: the string the user sends with the command to be forwarded
        """
        mention = member.mention
        if(member.name[0] == "@"):  # this must be done to allow @everyone and other roles starting with @ to work otherwise it sends out @@everyon
            mention = member.name
        message = " ".join(message)
        await ctx.message.delete()
        await ctx.send(str(mention) + " " + message)
        log_message(ctx, "forward command:\n   message: \'" + message + "\'\n   forwarded to: "+str(member)+"\n")

    @forward.error
    async def forward_error(self,ctx,error):
        if isinstance(error, commands.MemberNotFound) or isinstance(error,commands.RoleNotFound) or isinstance(error,commands.BadUnionArgument):
            log_message(ctx,"incorrect use of forward command user or role doesn't exist:\n")
            await ctx.message.delete()
            await ctx.send(ctx.message.author.mention + " Incorrect use of forward command user or role does not exist!")
        else:
            raise error



async def setup(bot):
    await bot.add_cog(Messaging(bot))