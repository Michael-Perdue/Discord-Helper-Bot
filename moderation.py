import asyncio
import time
import re
from typing import Optional

import discord
from discord.ext import commands
from main import log_message
class Moderation(commands.Cog):

    def __init__(self,bot: commands.Bot) -> None:
        self.bot = bot

    def moderation_channel(self,ctx):
        """
        This function gets and returns the moderation channel of a server,
        given the context of a message from the server.
        :param ctx: the context of the message
        :return: a discord.TextChannel that represents the moderation channel
        """
        return discord.utils.get(ctx.guild.channels, name="moderation")


    @commands.command(name="ban")
    async def ban(self,ctx,member: discord.Member,*reason):
        """

        :param ctx: the context of the message
        :param member: the member you want to ban
        :param reason: the reason why you want to ban the member
        """
        reason = " ".join(reason)
        log_message(ctx,"ban command:\n   user being banned: "+str(member)+"\n   reason: \'" + reason + "\'\n")
        await ctx.message.delete()
        await self.moderation_channel(ctx).send(ctx.message.author.mention + " has banned " + str(member.mention) + " for: " + reason)
        await member.ban(reason=reason)


    @commands.command(name="kick")
    async def kick(self,ctx,member: discord.Member,*reason):
        """

        :param ctx: the context of the message
        :param member: the member you want to kick
        :param reason: the reason why you want to kick the member
        """
        reason = " ".join(reason)
        log_message(ctx,"kick command:\n   user being kicked: "+str(member)+"\n   reason: \'" + reason + "\'\n")
        await ctx.message.delete()
        await self.moderation_channel(ctx).send(ctx.message.author.mention + " has kicked " + str(member.mention) + " for: " + reason)
        await member.kick(reason=reason)

    @kick.error
    @ban.error
    async def ban_kick_error(self,ctx,error):
        """

        :param ctx: the context of the message
        :param error: the error that occured in the ban or kick function
        """
        if isinstance(error, commands.MemberNotFound):
            log_message(ctx,"incorrect use of "+ctx.command.name+" command user does not exist:\n")
            await ctx.message.delete()
            await ctx.send(ctx.message.author.mention + " Incorrect use of "+ctx.command.name+ " command user does not exist!")
        else:
            raise error

    async def delete_all_messages(self,channel,member,amount: Optional[int] = -1):
        """

        :param channel: the channel you want to delete messages from
        :param member: the user whose messages you want to delete
        :param amount: the number of messages you want to delete by default its -1 meaning all messages
        """
        # NOTE history is used over purge with a check lamda due to purge only being able to search the last 100 messages so if the user is not active the command wouldn't have worked
        all_messages = channel.history(limit=None)
        count = 0
        async for message in all_messages:
            if message.author.id == member.id:
                count+=1
                await message.delete()
                if count >= amount != -1:
                    return
                await asyncio.sleep(1)  # This has to be done due to throttle limiting of deletions

    @commands.has_permissions(administrator=True)
    @commands.hybrid_command(name="delete",description="Deletes all of a specific users messages from this channel or all channels")
    async def delete_messages(self, ctx: commands.Context, member: discord.Member,amount: Optional[int]=-1,all_channels: Optional[bool]=False) -> None:
        """

        :param ctx: the context of the message
        :param member: the user whose messages you want to delete
        :param amount: by default all messages are deleted if set to a number, then only that number of messages are deleted
        :param all_channels: by default is false if set to true then all users messages from all channels are deleted
        """
        await ctx.send("Deletion commencing",ephemeral=True,delete_after=10)
        if all_channels:
            log_message(ctx, "delete all command:\n   user's messages being deleted: " + str(member) + "\n")
            channels = ctx.guild.text_channels
            for channel in channels:
                await self.delete_all_messages(channel=channel, member=member)
            await self.moderation_channel(ctx).send(ctx.message.author.mention + " has deleted all of " + str(member.mention) + " messages from all channels")
        else:
            log_message(ctx,"delete command:\n   user's messages being deleted: "+str(member)+"\n")
            await self.delete_all_messages(channel=ctx.channel,member=member,amount=amount)
            await self.moderation_channel(ctx).send(ctx.message.author.mention + " has deleted " + (str(amount) if amount != -1 else "all") + " of " + str(member.mention) + " messages from " + ctx.channel.mention)
        await ctx.send("Deletion complete",ephemeral=True)

    @commands.has_permissions(administrator=True)
    @commands.hybrid_command(name="clear",description="Deletes all of the last x messages from this channel with x being the amount you set")
    async def clear(self,ctx: commands.Context,amount: int) -> None:
        """

        :param ctx: the context of the message
        :param amount: the amount of messages you want to delete
        """
        log_message(ctx,"clear command:\n   number of messages being deleted: "+str(amount)+"\n")
        total = amount
        await ctx.send("Clearing commencing", ephemeral=True,delete_after=10)
        for x in range(1+int(amount/100)):   # purge has a max limit of 100 so this determines how many times to run purge
            if total<100:
                await ctx.channel.purge(limit=total)
            else:
                await ctx.channel.purge(limit=None)
                total = total-100
        await ctx.send("Clearing complete", ephemeral=True)
        await self.moderation_channel(ctx).send(ctx.message.author.mention + " has deleted the last " + str(amount) + " messages from " + ctx.channel.mention)

    @commands.has_permissions(administrator=True)
    @commands.hybrid_command(name="banword",description="Bans a word, so makes it so any new message with that word gets deleted and reported to mod channel")
    async def ban_word(self,ctx: commands.Context,word: str) -> None:
        """

        :param ctx: the context of the message
        :param word: the word you want banned
        """
        lines = open("banned_words.txt", "r").readlines()
        lines = [str(line.replace("\n","") + " " + word + "\n") if str(ctx.guild.id) in line else line for line in lines]
        log_message(ctx,"ban word command:\n   word banned: "+word+"\n")
        file = open("banned_words.txt","w")
        file.writelines(lines)
        file.close()
        self.bot.banned_words[ctx.guild.id] = (self.bot.banned_words[ctx.guild.id] + [word])
        await ctx.send("\'" + word + "\' Has now been banned",ephemeral=True)
        await self.moderation_channel(ctx).send(ctx.message.author.mention + " has banned the word: " + word)

    @commands.has_permissions(administrator=True)
    @commands.hybrid_command(name="unbanword",description="Unbans a word which was previously banned")
    async def unban_word(self,ctx: commands.Context,word: str) -> None:
        """

        :param ctx: the context of the message
        :param word: the word you want unbanned
        """
        lines = open("banned_words.txt", "r").readlines()
        lines = [(str(ctx.guild.id) + " " + str(re.sub(("(^|\s)"+word+"($|\s)"),"",line.partition(" ")[2])))if str(ctx.guild.id) in line else line for line in lines]
        log_message(ctx,"unban word command:\n   word unbanned: "+word+"\n")
        file = open("banned_words.txt","w")
        file.writelines(lines)
        file.close()
        self.bot.banned_words[ctx.guild.id] = [word1 for word1 in self.bot.banned_words[ctx.guild.id] if word1 != word]
        await ctx.send("\'" + word + "\' Has now been unbanned",ephemeral=True)
        await self.moderation_channel(ctx).send(ctx.message.author.mention + " has unbanned the word: " + word)


    @commands.hybrid_command(name="banwords",description="Gives a list of all banned words")
    async def list_ban_words(self,ctx: commands.Context) -> None:
        """

        :param ctx: the context of the message
        """
        banned_words = self.bot.banned_words[ctx.guild.id]
        await ctx.send(content=ctx.message.author.mention,embed=discord.Embed(title="Banned words",
                                                                              description="Using any of these words will lead to your message being delete and you possibly being kicked or banned.",
                                                                              colour=discord.Colour.red()
                                                                              ).add_field(name="The list of banned words are :",value="\n".join(banned_words),inline=True).set_thumbnail(url="https://raw.githubusercontent.com/Michael-Perdue/Discord-bot/master/ban.png"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
