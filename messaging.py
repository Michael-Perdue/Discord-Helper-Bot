import asyncio

import discord
from discord.ext import commands
from time import sleep
class Messaging(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    def log_message(self,ctx,message):
        print(message + "   sent by: " + str(ctx.message.author) + "\n   on server: " + str(ctx.guild))

    @commands.command(name="test")
    async def test(self,ctx):
        self.log_message(ctx,"Test command:\n")
        await ctx.send("Test")

    @commands.command(name="mirror")
    async def mirror(self,ctx,*args):
        message = " ".join(args)
        self.log_message(ctx,"Mirror command:\n   message: \'"+message+"\'\n")
        await ctx.send(message)

    @commands.command(name="spam")
    async def spam(self,ctx,*args):
        self.log_message(ctx,"Spam command:\n   mentioned: "+str(args[0])+"\n")
        for x in range(int(args[1])):
            await ctx.send(str(args[0]))
            await asyncio.sleep(0.2)

async def setup(bot):
    await bot.add_cog(Messaging(bot))