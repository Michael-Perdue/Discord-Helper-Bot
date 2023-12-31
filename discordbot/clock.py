import asyncio
import time
import discord
from typing import Optional
from discord.ext import commands
from main import log_message

class Clock(commands.Cog):
    stopwatches = {}

    def __init__(self,bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="countdown", description="Counts down from the number given.")
    async def countdown(self, ctx: commands.Context, start: int) -> None:
        """
        This function deals with a user sending a !countdown command, and a number the bot then
        will send back a message of the number after minusing one after every second to work like a countdown.
        Example command: '!countdown 3' and the bot will respond with a message saying '3' then '2' then '1' all
        with one second between and then send a message saying the countdown is done.
        :param ctx: the context of the message
        :param start: an int of the number you want the bot to countdown from
        """
        log_message(ctx,"Countdown command:\n   time: "+str(start)+" seconds\n")
        await ctx.send(start)
        for x in range(start-1,0,-1):
            await asyncio.sleep(1)
            await ctx.channel.send(x)
        await asyncio.sleep(1)
        await ctx.channel.send(ctx.author.mention + " countdown done")

    @commands.hybrid_command(name="timer", description="Informs you when the time is up.")
    async def timer(self,ctx: commands.Context,hours: Optional[int] = 0,minutes: Optional[int] = 0,seconds: Optional[int] = 0) -> None:
        """
        This function deals with a user sending a !timer command, and a time length, the bot then
        will sleep(non-blocking) until that number of seconds have gone by.
        It will then send a message mentioning the user saying the timer is up.
        Example command: '/timer 10' and the bot will wait 10 seconds before messaging saying @user timer finished.
        :param ctx: the context of the message
        :param hours: an int of the number of hours you want the timer to go off in
        :param minutes: an int of the number of minutes you want the timer to go off in
        :param seconds: an int of the number of seconds you want the timer to go off in
        """
        total_time = (hours*60*60)+(minutes*60)+seconds
        translated_time = time.strftime("%H hours %M minutes %S seconds",time.gmtime(total_time)).replace("00 hours ","").replace("00 minutes ","")
        await ctx.send("Timer started for " + translated_time,ephemeral=True)
        log_message(ctx,"Timer command:\n   time: "+ translated_time +"\n")
        await asyncio.sleep(total_time)
        await ctx.channel.send(str(ctx.message.author.mention) + " " + translated_time + " timer finished")

    @commands.hybrid_group(name="stopwatch", description="Simply a working stopwatch")
    async def stopwatch(self,ctx : commands.Context):
        """
        This function deals with a user sending a !stopwatch command, and has 3 options start, time and stop.
        Start will store the user and the time in a key value pair and stop will then retrieve the time and see
        how long has passed and return that to the user and time will retrieve the start time and how long has passed.
        Example command: '!stopwatch start' and '!stopwatch stop'
        :param ctx: the context of the message
        """

    @stopwatch.command(name="start",description="starts the stopwatch")
    async def stopwatch_start(self, ctx: commands.Context):
        self.stopwatches[ctx.message.author] = time.time()
        log_message(ctx, "Stopwatch command started:\n")
        await ctx.send("Stopwatch started")

    @stopwatch.command(name="stop",description="stops the stopwatch")
    async def stopwatch_stop(self, ctx: commands.Context):
        time_elapsed = time.time()-self.stopwatches[ctx.message.author]
        await ctx.send(embed=discord.Embed(title="Stopwatch",
                                           description=(ctx.message.author.mention + " You have stopped your stopwatch "),
                                           colour=discord.Colour.blue()
                                           ).add_field(name="Start time", value=str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.stopwatches[ctx.message.author]))), inline=True
                                           ).add_field(name="Stop time", value=str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))), inline=True
                                           ).add_field(name="Time elapsed", value="{:.2f}".format(time_elapsed) + " seconds", inline=False))
        self.stopwatches.pop(ctx.message.author)
        log_message(ctx, "Stopwatch command stopped:\n   time elapsed: " + str(time_elapsed) + " seconds\n")

    @stopwatch.command(name="time",description="gets the stopwatches time")
    async def stopwatch_time(self, ctx: commands.Context):
        time_elapsed = time.time()-self.stopwatches[ctx.message.author]
        await ctx.send(embed=discord.Embed(title="Stopwatch",
                                           description=(ctx.message.author.mention + " Information on your stopwatch "),
                                           colour=discord.Colour.blue()
                                           ).add_field(name="Start time", value=str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.stopwatches[ctx.message.author]))), inline=True
                                           ).add_field(name="Time elapsed", value="{:.2f}".format(time_elapsed) + " seconds", inline=False))
        log_message(ctx, "Stopwatch command time checked:\n   time elapsed: " + str(time_elapsed) + " seconds\n")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Clock(bot))