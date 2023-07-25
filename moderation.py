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

    @kick.error
    @ban.error
    async def ban_kick_error(self,ctx,error):
        if isinstance(error, commands.MemberNotFound):
            log_message(ctx,"incorrect use of "+ctx.command.name+" command user does not exist:\n")
            await ctx.message.delete()
            await ctx.send(ctx.message.author.mention + " Incorrect use of "+ctx.command.name+ " command user does not exist!")
        else:
            raise error

    async def delete_all_messages(self,channel,member):
        all_messages = channel.history(limit=None)
        async for message in all_messages:
            if message.author.id == member.id:
                await message.delete()
                await asyncio.sleep(1)  # This has to be done due to throttle limiting of deletions

    @commands.command(name="delete")
    async def delete(self,ctx: commands.Context,member: discord.Member):
        log_message(ctx,"delete command:\n   user's messages being deleted: "+str(member)+"\n")
        # NOTE history is used over purge with a check lamda due to purge only being able to search the last 100 messages so if the user is not active the command wouldn't have worked
        await self.delete_all_messages(ctx.channel,member)
        await ctx.send(ctx.message.author.mention + " has deleted all of " + str(member.mention) + " messages from this channel")

    @commands.command(name="deleteall")
    async def delete_all(self,ctx: commands.Context,member: discord.Member):
        log_message(ctx,"deleteAll command:\n   user's messages being deleted: "+str(member)+"\n")
        channels = ctx.guild.text_channels
        for channel in channels:
            await self.delete_all_messages(channel=channel,member=member)
        # NOTE history is used over purge with a check lamda due to purge only being able to search the last 100 messages so if the user is not active the command wouldn't have worked
        await ctx.send(ctx.message.author.mention + " has deleted all of " + str(member.mention) + " messages")

    @commands.command(name="clear")
    async def clear(self,ctx: commands.Context,size: int):
        log_message(ctx,"clear command:\n   number of messages being deleted: "+str(size)+"\n")
        for x in range(1+int(size/100)):   # purge has a max limit of 100 so this determines how many times to run purge
            await ctx.channel.purge(limit=None)
        await ctx.send(ctx.message.author.mention + " has deleted the last " + str(size) + " messages from this channel")


async def setup(bot):
    await bot.add_cog(Moderation(bot))