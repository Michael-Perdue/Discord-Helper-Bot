import asyncio
import time

import discord
from discord.ext import commands
from main import log_message
class Moderation(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    def moderation_channel(self,ctx):
        return discord.utils.get(ctx.guild.channels, name="moderation")


    @commands.command(name="ban")
    async def ban(self,ctx,member: discord.Member,*reason):
        reason = " ".join(reason)
        log_message(ctx,"ban command:\n   user being banned: "+str(member)+"\n   reason: \'" + reason + "\'\n")
        await ctx.message.delete()
        await self.moderation_channel(ctx).send(ctx.message.author.mention + " has banned " + str(member.mention) + " for: " + reason)
        await member.ban(reason=reason)


    @commands.command(name="kick")
    async def kick(self,ctx,member: discord.Member,*reason):
        reason = " ".join(reason)
        log_message(ctx,"kick command:\n   user being kicked: "+str(member)+"\n   reason: \'" + reason + "\'\n")
        await ctx.message.delete()
        await self.moderation_channel(ctx).send(ctx.message.author.mention + " has kicked " + str(member.mention) + " for: " + reason)
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
        # NOTE history is used over purge with a check lamda due to purge only being able to search the last 100 messages so if the user is not active the command wouldn't have worked
        all_messages = channel.history(limit=None)
        async for message in all_messages:
            if message.author.id == member.id:
                await message.delete()
                await asyncio.sleep(1)  # This has to be done due to throttle limiting of deletions

    @commands.command(name="delete")
    async def delete(self, ctx: commands.Context, member: discord.Member,*type):
        if len(type) != 0:
            if type[0] == "all":
                log_message(ctx, "delete all command:\n   user's messages being deleted: " + str(member) + "\n")
                channels = ctx.guild.text_channels
                for channel in channels:
                    await self.delete_all_messages(channel=channel, member=member)
                await self.moderation_channel(ctx).send(ctx.message.author.mention + " has deleted all of " + str(member.mention) + " messages from all channels")
            else:
                log_message(ctx, "delete all command used wrong:\n   user's messages being deleted: " + str(member) + "\n")
                await self.moderation_channel(ctx).send(ctx.message.author.mention + " incorrect use of delete command \'" + str(type) + "\' is not a valid argument")
        else:
            log_message(ctx,"delete command:\n   user's messages being deleted: "+str(member)+"\n")
            await self.delete_all_messages(ctx.channel,member)
            await self.moderation_channel(ctx).send(ctx.message.author.mention + " has deleted all of " + str(member.mention) + " messages from " + ctx.channel.mention)

    @commands.command(name="clear")
    async def clear(self,ctx: commands.Context,size: int):
        log_message(ctx,"clear command:\n   number of messages being deleted: "+str(size)+"\n")
        for x in range(1+int(size/100)):   # purge has a max limit of 100 so this determines how many times to run purge
            await ctx.channel.purge(limit=None)
        await self.moderation_channel(ctx).send(ctx.message.author.mention + " has deleted the last " + str(size) + " messages from " + ctx.channel.mention)

    @commands.command(name="banword")
    async def ban_word(self,ctx: commands.Context,word: str):
        lines = open("banned_words.txt", "r").readlines()
        lines = [str(line.replace("\n","") + " " + word + "\n") for line in lines if str(ctx.guild.id) in line]
        log_message(ctx,"ban word command:\n   word banned: "+word+"\n")
        file = open("banned_words.txt","w")
        file.writelines(lines)
        file.close()
        self.bot.banned_words[ctx.guild.id] = (self.bot.banned_words[ctx.guild.id] + [word])
        await ctx.message.delete()
        await self.moderation_channel(ctx).send(ctx.message.author.mention + " has banned the word: " + word)

    def read_banned_words(self):
        file = open("banned_words.txt","r")
        for x in file:
            print(x)
            split_line = list(x.replace("\n","").split(" "))
            self.banned_words[int(split_line[0])] = split_line[1:]
        file.close()

    def add_guilds(self):
        file = open("banned_words.txt","a")
        found_guilds = self.banned_words.keys()
        for guild in self.guilds:
            if guild.id not in found_guilds:
                file.write(str(guild.id) + "\n")
        file.close()

async def setup(bot):
    await bot.add_cog(Moderation(bot))