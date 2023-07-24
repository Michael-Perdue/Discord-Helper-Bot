import asyncio
from discord.ext import commands
from main import log_message
class Messaging(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="test")
    async def test(self,ctx):
        log_message(ctx,"Test command:\n")
        await ctx.send("Test")

    @commands.command(name="mirror")
    async def mirror(self,ctx,*args):
        message = " ".join(args)
        log_message(ctx,"Mirror command:\n   message: \'"+message+"\'\n")
        await ctx.send(message)

    @commands.command(name="spam")
    async def spam(self,ctx,*args):
        log_message(ctx,"Spam command:\n   mentioned: "+str(args[0])+"\n   amount: " + str(args[1]) + "\n")
        for x in range(int(args[1])):
            await ctx.send(str(args[0]))
            await asyncio.sleep(0.2)

async def setup(bot):
    await bot.add_cog(Messaging(bot))