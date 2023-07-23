import discord
from discord.ext import commands
from time import sleep
class Clock(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="countdown")
    async def countdown(self,ctx,arg):
        for x in range(int(arg),0,-1):
            await ctx.send(x)
            sleep(1)

    @commands.command(name="timer")
    async def timer(self,ctx,arg):
        sleep(int(arg))
        await ctx.send(str(ctx.message.author.mention) + " " + str(arg) + "s timer finished")


async def setup(bot):
    await bot.add_cog(Clock(bot))