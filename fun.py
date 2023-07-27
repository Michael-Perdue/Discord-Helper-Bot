import asyncio
import random
from discord.ext import commands
from main import log_message

class Fun(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="coin")
    async def coin_flip(self,ctx: commands.Context,*args):
        amount = 1
        if(len(args) != 0):
            amount = args[0]
        for x in range(0,int(amount)):
            flip = random.randrange(2)
            await ctx.send(ctx.message.author.mention + " The coin landed on **" + ("Heads" if flip else "Tails") + "**")
            await asyncio.sleep(1)
        log_message(ctx,"Coinflip command used:\n   times: "+str(amount)+"\n")

    @commands.command(name="roll")
    async def roll(self,ctx: commands.Context,*args):
        amount = args[0]
        size = args[1]
        result = []
        for x in range(0,int(amount)):
            roll = random.randint(1,int(size))
            result.append(str(roll)+"/"+size)
        await ctx.send(ctx.message.author.mention + " The dice landed on **" + " ".join(result) + "**")
        log_message(ctx,"roll command used:\n   amount of dice: " + amount + "\n   sides of dice: " + size + "\n")




async def setup(bot):
    await bot.add_cog(Fun(bot))