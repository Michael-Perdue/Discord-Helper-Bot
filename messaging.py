import discord
from discord.ext import commands
from time import sleep
class Messaging(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="test")
    async def test(self,ctx):
        await ctx.send("Test")

    @commands.command(name="mirror")
    async def mirror(self,ctx,arg):
        await ctx.send(str(arg))

    @commands.command(name="countdown")
    async def countdown(self,ctx,arg):
        for x in range(int(arg),0,-1):
            await ctx.send(x)
            sleep(1)

async def setup(bot):
    await bot.add_cog(Messaging(bot))