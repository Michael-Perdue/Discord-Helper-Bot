import asyncio
import typing
import discord
from discord.ext import commands
from main import log_message

class Messaging(commands.Cog):

    def __init__(self,bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="hey",description="Returns a greeting")
    async def hey(self,ctx: commands.Context) -> None:
        """
        This function is simply for debugging to ensure the bot works
        when a user sends !hey the bot responds with a message saying 'Hello @user'.
        :param ctx: the context of the message
        """
        log_message(ctx,"Hello command:\n")
        await ctx.send("Hello " + ctx.author.mention)

    @commands.guild_only()
    @commands.hybrid_command(name="mirror",description="Resends whatever you send anonymously")
    async def mirror(self,ctx: commands.Context,message: str) -> None:
        """
        This function deals with a user sending a !mirror command, and it simply deletes their message
        and sends whatever they sent into the discord channel.
        Example command: '!mirror this is a test' results in the bot messaging back 'this is a test'.
        :param ctx: the context of the message.
        :param message: the string you want the bot to mirror.
        """
        log_message(ctx,"Mirror command:\n   message: \'"+message+"\'\n")
        await ctx.send("Message is being mirrored",delete_after=0,ephemeral=True)
        await ctx.channel.send(message)

    @commands.guild_only()
    @commands.hybrid_command(name="spam",description="Spam notifications to whatever role you want")
    async def spam(self,ctx: commands.Context,member: typing.Union[discord.Member,discord.Role],times: int) -> None:
        """
        This function deals with a user sending a !spam command, a mention of a user or group and a number.
        The bot will then mention the user or group the number of times it was told.
        Example command: '!spam @everyone 2' results in 2 messages by the bot of @everyone.
        :param ctx: the context of the message.
        :param member: the user or group you want to mention.
        :param times: the number of times you want the bot to mention them.
        """
        log_message(ctx,"Spam command:\n   mentioned: "+str(member)+"\n   amount: " + str(times) + "\n")
        await ctx.send("Spam is starting: ")
        for x in range(int(times)):
            await ctx.channel.send(str(member.mention))
            await asyncio.sleep(0.2)    # waits 0.2 seconds as otherwise the responses seem delayed

    @commands.guild_only()
    @commands.hybrid_command(name="forward",description="forwards your message anonymously")
    async def forward(self, ctx: commands.Context,member: typing.Union[discord.Member,discord.Role], message: str) -> None:
        """
        This function deals with a user sending a !forward command, and it simply sends whatever
        the users send to the person or group who they mention and the bot deletes their message, so it's anonymous.
        Example command: '!forward @user this is a test' results in the bot messaging back '@user this is a test'.
        :param ctx: the context of the message.
        :param member: the group or person the user wants to forward it to example @role.
        :param message: the string you want forwarded.
        """
        mention = member.mention
        if(member.name[0] == "@"):  # this must be done to allow @everyone and other roles starting with @ to work otherwise it sends out @@everyone
            mention = member.name
        await ctx.send("Message is being forwarded",ephemeral=True,delete_after=0)
        await ctx.channel.send(str(mention) + " " + message)
        await discord.utils.get(ctx.guild.channels, name="moderation").send(ctx.author.mention + " Has forwarded the message *\'" + message + "\'* to " + mention)
        log_message(ctx, "forward command:\n   message: \'" + message + "\'\n   forwarded to: "+str(member)+"\n")

    @forward.error
    async def forward_error(self,ctx,error):
        if isinstance(error, commands.MemberNotFound) or isinstance(error,commands.RoleNotFound) or isinstance(error,commands.BadUnionArgument):
            log_message(ctx,"incorrect use of forward command user or role doesn't exist:\n")
            await ctx.message.delete()
            await ctx.send(ctx.message.author.mention + " Incorrect use of forward command user or role does not exist!",ephemeral=True)
        else:
            raise error

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Messaging(bot))