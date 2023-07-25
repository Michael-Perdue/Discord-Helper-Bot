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

    @ban.error
    async def ban_error(self,ctx,error):
        if isinstance(error, commands.MemberNotFound):
            log_message(ctx,"incorrect use of ban command user does not exist:\n")
            await ctx.message.delete()
            await ctx.send(ctx.message.author.mention + " Incorrect use of ban command user does not exist!")
        else:
            raise error

    @commands.command(name="kick")
    async def kick(self,ctx,member: discord.Member,*reason):
        reason = " ".join(reason)
        log_message(ctx,"kick command:\n   user being kicked: "+str(member)+"\n   reason: \'" + reason + "\'\n")
        await ctx.message.delete()
        await ctx.send(ctx.message.author.mention + " has kicked " + str(member.mention) + " for: " + reason)
        await member.kick(reason=reason)

    @kick.error
    async def kick_error(self,ctx,error):
        if isinstance(error, commands.MemberNotFound):
            log_message(ctx,"incorrect use of kick command user does not exist:\n")
            await ctx.message.delete()
            await ctx.send(ctx.message.author.mention + " Incorrect use of kick command user does not exist!")
        else:
            raise error
async def setup(bot):
    await bot.add_cog(Moderation(bot))