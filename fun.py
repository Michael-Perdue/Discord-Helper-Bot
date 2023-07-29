import asyncio
import random
from discord.ext import commands
from main import log_message

class Fun(commands.Cog):

    def __init__(self,bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="coin")
    async def coin_flip(self,ctx: commands.Context,times: int) -> None:
        results = []
        for x in range(0,int(times)):
            results.append("Heads" if random.randrange(2) else "Tails")
        await ctx.send("The coin/s landed on **" + " ".join(results) + "**")
        log_message(ctx,"Coinflip command used:\n   times: "+str(times)+"\n")

    @commands.hybrid_command(name="roll")
    async def roll(self,ctx: commands.Context,amount: str,size: str) -> None:
        result = []
        for x in range(0,int(amount)):
            roll = random.randint(1,int(size))
            result.append(str(roll)+"/"+size)
        await ctx.send(" The dice landed on **" + " ".join(result) + "**")
        log_message(ctx,"roll command used:\n   amount of dice: " + amount + "\n   sides of dice: " + size + "\n")




async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))