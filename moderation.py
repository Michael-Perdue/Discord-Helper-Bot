import asyncio
import time

import discord
from discord.ext import commands
from main import log_message
class Moderation(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="ban")
    async def ban(self,ctx,member: discord.Member,*reason):
        reason = " ".join(reason)
        log_message(ctx,"ban command:\n   user being banned: "+str(member)+"\n   reason: \'" + reason + "\'\n")
        await ctx.message.delete()
        await ctx.send(ctx.message.author.mention + " has banned " + str(member.mention) + " for: " + reason)
        await member.ban(reason=reason)

    @commands.command(name="kick")
    async def kick(self,ctx,member: discord.Member,*reason):
        reason = " ".join(reason)
        log_message(ctx,"kick command:\n   user being kicked: "+str(member)+"\n   reason: \'" + reason + "\'\n")
        await ctx.message.delete()
        await ctx.send(ctx.message.author.mention + " has kicked " + str(member.mention) + " for: " + reason)
        await member.kick(reason=reason)

async def setup(bot):
    await bot.add_cog(Moderation(bot))