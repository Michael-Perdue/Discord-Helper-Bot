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
        """
        This function deals with a user sending a !countdown command, and a number the bot then
        will send back a message of the number after minusing one after every second to work like a countdown.
        Example command: '!countdown 3' and the bot will respond with a message saying '3' then '2' then '1' all
        with one second between.
        :param ctx: the context of the message
        :param arg: an int of the number you want the bot to countdown from
        """
        log_message(ctx,"Countdown command:\n   time: "+str(arg)+" seconds\n")
        for x in range(int(arg),0,-1):
            await ctx.send(x)
            await asyncio.sleep(1)

    @commands.command(name="timer")
    async def timer(self,ctx,arg):
        """
        This function deals with a user sending a !timer command, and a number the bot then
        will sleep(non-blocking) until that number of seconds have gone by.
        It will then send a message mentioning the user saying the timer is up.
        Example command: '!timer 10' and the bot will wait 10 seconds before messaging saying @user timer finished.
        :param ctx: the context of the message
        :param arg: an int of the number of seconds you want the bot to wait before it alerts you
        """
        log_message(ctx,"Timer command:\n   time: "+str(arg)+" seconds\n")
        await asyncio.sleep(int(arg))
        await ctx.send(str(ctx.message.author.mention) + " " + str(arg) + "s timer finished")

    @commands.command(name="stopwatch")
    async def stopwatch(self,ctx,arg):
        """
        This function deals with a user sending a !stopwatch command, and has 2 options start and stop.
        Start will store the user and the time in a key value pair and stop will then retrieve the time and see
        how long has passed and return that to the user.
        Example command: '!stopwatch start' and '!stopwatch stop'
        :param ctx: the context of the message
        :param arg: a string stating if you want to start the stopwatch or stop the stopwatch
        """
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