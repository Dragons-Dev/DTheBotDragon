import asyncio
import logging
import time

import discord
from discord.ext import commands

import config
from DragonBot import DragonBot
from utils import db


class ModMailCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if isinstance(msg.channel, discord.DMChannel):
            if msg.author.bot:
                return
            modmail_channel = await db.get_setting("modmail channel", guild = config.GUILD)
            if not modmail_channel:
                em = discord.Embed(title = "Error", description = "The bot-owner has no Modmail Channel set up.", color = discord.Color.brand_red())
                await msg.channel.send(embed = em)
                return
            parent_channel = int(modmail_channel[0])
            channel: discord.TextChannel = self.client.get_channel(parent_channel)
            if msg.author.id != self.client.user.id:
                threads = channel.threads

                for thread in threads:

                    if str(f"{msg.author.id}") == str(f"{thread.name}"):

                        if thread.locked or thread.archived:
                            message = await channel.send(f"Creating thread for {msg.author.name}...")
                            thread = await message.create_thread(name = msg.author.id)

                            guild = self.client.get_guild(int(config.GUILD))
                            member = guild.get_member(msg.author.id)

                            joined_at = member.joined_at
                            joined_at.timestamp()
                            joined_at = (time.mktime(joined_at.timetuple()))

                            created_at = member.created_at
                            created_at.timestamp()
                            created_at = (time.mktime(created_at.timetuple()))

                            em = discord.Embed(title = f"Userinfo for {member.display_name}",
                                               color = discord.Color.magenta())
                            em.add_field(name = f"Name", value = f"{member.name}", inline = False)
                            em.add_field(name = f"ID", value = f"{member.id}", inline = False)
                            em.add_field(name = f"Creation Date", value = f"<t:{int(created_at)}:F>", inline = False)
                            em.add_field(name = f"Join Date", value = f"<t:{int(joined_at)}:F>")
                            em.add_field(name = f"Bot", value = f"{'Yes' if member.bot else 'No'}", inline = False)
                            em.set_thumbnail(url = member.display_avatar)

                            dm = discord.Embed(description = msg.content,
                                               color = discord.Color.yellow())
                            dm.set_author(name = member.name, icon_url = member.display_avatar)

                            await thread.send(embeds = [em, dm])

                            if len(msg.attachments) > 0:
                                picture_em = discord.Embed(color = discord.Color.yellow())
                                picture_em.set_author(name = msg.author, icon_url = msg.author.display_avatar)
                                await thread.send(embed = picture_em, files = msg.attachments)

                        if len(msg.attachments) == 0:
                            em = discord.Embed(description = msg.content, color = discord.Color.yellow())
                            em.set_author(name = msg.author, icon_url = msg.author.display_avatar)
                            em.set_footer(text = f"Unique ID for this user {msg.author.id}")
                            await thread.send(embed = em)
                            break
                        if len(msg.attachments) > 0:
                            for attachment in msg.attachments:
                                picture_em = discord.Embed(description = msg.content, color = discord.Color.yellow())
                                picture_em.set_author(name = msg.author, icon_url = msg.author.display_avatar)
                                picture_em.set_image(url = attachment.url)
                                picture_em.set_footer(text = f"Unique ID for this user {msg.author.id}")
                                await thread.send(embed = picture_em)
                            break
                else:
                    message = await channel.send(f"Creating thread for {msg.author.name}...")
                    thread = await message.create_thread(name = msg.author.id)

                    guild = self.client.get_guild(int(config.GUILD))
                    member = guild.get_member(msg.author.id)

                    joined_at = member.joined_at
                    joined_at.timestamp()
                    joined_at = (time.mktime(joined_at.timetuple()))

                    created_at = member.created_at
                    created_at.timestamp()
                    created_at = (time.mktime(created_at.timetuple()))

                    em = discord.Embed(title = f"Userinfo for {member.display_name}",
                                       color = discord.Color.magenta())
                    em.add_field(name = f"Name", value = f"{member.name}", inline = False)
                    em.add_field(name = f"ID", value = f"{member.id}", inline = False)
                    em.add_field(name = f"Creation Date", value = f"<t:{int(created_at)}:F>", inline = False)
                    em.add_field(name = f"Join Date", value = f"<t:{int(joined_at)}:F>")
                    em.add_field(name = f"Bot", value = f"{'Yes' if member.bot else 'No'}", inline = False)
                    em.set_thumbnail(url = member.display_avatar)

                    dm = discord.Embed(description = msg.content,
                                       color = discord.Color.yellow())
                    dm.set_author(name = member.name, icon_url = member.display_avatar)

                    await thread.send(embeds = [em, dm])

                    if len(msg.attachments) > 0:
                        picture_em = discord.Embed(description = msg.content, color = discord.Color.brand_green())
                        picture_em.set_author(name = msg.author, icon_url = msg.author.display_avatar)
                        picture_em.set_footer(text = f"Unique ID for this user {msg.author.id}")
                        await msg.channel.send(content = "The moderator is recieving the files", embed = picture_em)
                        await member.send(embed = picture_em, files = [attachment for attachment in msg.attachments])

        if msg.channel.type == discord.ChannelType.public_thread:
            if msg.author.id != self.client.user.id:
                guild = msg.channel.guild
                member = guild.get_member(int(msg.channel.name))
                await msg.delete()
                await asyncio.sleep(0.1)

                if len(msg.attachments) == 0:
                    em = discord.Embed(description = msg.content, color = discord.Color.brand_green())
                    em.set_author(name = msg.author, icon_url = msg.author.display_avatar)
                    em.set_footer(text = f"Unique ID for this user {msg.author.id}")
                    await msg.channel.send(embed = em)
                    await member.send(embed = em)

                if len(msg.attachments) > 0:
                    picture_em = discord.Embed(description = msg.content, color = discord.Color.brand_green())
                    picture_em.set_author(name = msg.author, icon_url = msg.author.display_avatar)
                    picture_em.set_footer(text = f"Unique ID for this user {msg.author.id}")
                    await msg.channel.send(content = "The user is recieving the files", embed = picture_em)
                    await member.send(embed = picture_em, files = [attachment for attachment in msg.attachments])


def setup(client: DragonBot):
    client.add_cog(ModMailCog(client))
