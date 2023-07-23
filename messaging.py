import asyncio

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
    async def mirror(self,ctx,*args):
        await ctx.send(" ".join(args))

    @commands.command(name="spam")
    async def spam(self,ctx,*args):
        for x in range(int(args[1])):
            await ctx.send(str(args[0]))
            await asyncio.sleep(0.2)

async def setup(bot):
    await bot.add_cog(Messaging(bot))