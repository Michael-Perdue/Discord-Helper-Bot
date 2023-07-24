import asyncio
import time
from discord.ext import commands
from main import log_message
class Clock(commands.Cog):
    stopwatches = {}

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="countdown")
    async def countdown(self,ctx,arg):
        log_message(ctx,"Countdown command:\n   time: "+str(arg)+" seconds\n")
        for x in range(int(arg),0,-1):
            await ctx.send(x)
            await asyncio.sleep(1)

    @commands.command(name="timer")
    async def timer(self,ctx,arg):
        log_message(ctx,"Timer command:\n   time: "+str(arg)+" seconds\n")
        await asyncio.sleep(int(arg))
        await ctx.send(str(ctx.message.author.mention) + " " + str(arg) + "s timer finished")

    @commands.command(name="stopwatch")
    async def stopwatch(self,ctx,arg):
        if(arg == "start"):
            self.stopwatches[ctx.message.author] = time.time()
            log_message(ctx, "Stopwatch command started:\n")
            await ctx.send(str(ctx.message.author.mention) + " stopwatch started")
        elif(arg == "stop"):
            time_elapsed = time.time()-self.stopwatches[ctx.message.author]
            self.stopwatches.pop(ctx.message.author)
            await ctx.send(str(ctx.message.author.mention) + " stopwatch stopped\n   Total time elapsed: " + str(time_elapsed) + " seconds")
            log_message(ctx, "Stopwatch command stopped:\n   time elapsed: " + str(time_elapsed) + " seconds\n")
        else:
            await ctx.send(str(ctx.message.author.mention) + " incorrect use of stopwatch please either do !stopwatch start or !stopwatch stop")
            log_message(ctx, "Invalid use of stopwatch command:\n   argument given: " + str(arg) + "\n")


async def setup(bot):
    await bot.add_cog(Clock(bot))