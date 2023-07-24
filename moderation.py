import asyncio
import time

import discord
from discord.ext import commands
from main import log_message
class Moderation(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="ban")
    async def ban(self,ctx,member: discord.Member,reason):
        log_message(ctx,"ban command:\n   user being banned: "+str(member)+"\n   reason: \'" + str(reason) + "\'\n")
        await member.ban(reason=str(reason))

async def setup(bot):
    await bot.add_cog(Moderation(bot))