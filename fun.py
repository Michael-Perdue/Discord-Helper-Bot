import random
from discord.ext import commands
from main import log_message


class Fun(commands.Cog):

    def __init__(self,bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="coin",description="Flips a coin.")
    async def coin_flip(self,ctx: commands.Context,times: int) -> None:
        results = []
        for x in range(0,int(times)):
            results.append("Heads" if random.randrange(2) else "Tails")
        await ctx.send("The coin/s landed on **" + " ".join(results) + "**")
        log_message(ctx,"Coin flip command used:\n   times: "+str(times)+"\n")

    @commands.hybrid_command(name="roll",description="Rolls a set of dice.")
    async def roll(self,ctx: commands.Context,amount: str,size: str) -> None:
        result = []
        for x in range(0,int(amount)):
            roll = random.randint(1,int(size))
            result.append(str(roll)+"/"+size)
        await ctx.send(" The dice landed on **" + " ".join(result) + "**")
        log_message(ctx,"roll command used:\n   amount of dice: " + amount + "\n   sides of dice: " + size + "\n")

    @commands.hybrid_command(name="8ball",description="get the eightball to answer your question")
    async def eight_ball(self,ctx: commands.Context,question: str) -> None:
        eightball_results = ["It is certain","Reply hazy try again","Don’t count on it", "It is decidedly so", "Ask again later",
                             "My reply is no","Without a doubt","Better not tell you now","My sources say no","Yes definitely",
                             "Cannot predict now","Outlook not so good","You may rely on it","Concentrate and ask again","Very doubtful",
                             "As I see it, yes","Most likely","Outlook good","Yes","Signs point to yes"	]
        await ctx.send(" The eight ball responds with **" + eightball_results[random.randint(0,len(eightball_results)-1)] + "** to the question *" +question +"*")
        log_message(ctx,"eightball command used:\n")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))