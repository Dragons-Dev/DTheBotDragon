import datetime
import logging
import time

import discord
from discord.ext import commands

from DragonBot import DragonBot
from utils import db


class UserCog(commands.Cog):
    def __init__(self, client):
        self.client: DragonBot = client

    @commands.slash_command(name="userinfo", description="get information about a user")
    async def userinfo(
        self,
        ctx: discord.ApplicationContext,
        user: discord.Option(
            input_type=discord.SlashCommandOptionType.user,
            description="mention a user to get information about him",
        ),
    ):
        user = user.strip("<@!>")
        user = ctx.guild.get_member(int(user))
        em = discord.Embed(
            title=f"{user.name}#{user.discriminator}", color=discord.Color.purple()
        )
        em.set_thumbnail(url=user.display_avatar.url)
        em.add_field(name=f"User ID", value=f"{user.id}")
        em.add_field(
            name=f"Accout created",
            value=f"{user.created_at.strftime('%d.%m.%Y %H:%M')}\n<t:{int(time.mktime(user.created_at.timetuple()))}:R>",
        )
        em.add_field(
            name=f"Joined at",
            value=f"{user.joined_at.strftime('%d.%m.%Y %H:%M')}\n<t:{int(time.mktime(user.joined_at.timetuple()))}:R>",
        )

        team_id = await db.get_setting(setting="team role", guild=str(ctx.guild_id))
        if team_id is None:
            return await ctx.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You have not set up a team role.\nPlease set up a team role by running /settings Team Role your team role id",
                    color=discord.Color.brand_red(),
                ),
                ephemeral=True,
            )
        for role in ctx.author.roles:
            if int(team_id[0]) == int(role.id):
                response = await db.get_mod_action(member=user.id)
                counter = 0
                for item in response:
                    pub_id, moderator, reason, action, date = item
                    date1, date2 = date.split(" ")
                    date1 = date1.split("-")
                    date = f"{date1[2]}.{date1[1]}.{date1[0]} {date2}"
                    em.add_field(
                        name=f"{action.capitalize()} (ID: {pub_id})",
                        value=f"**---Reason---**\n{reason}\n------------\nBy <@{moderator}>\nAt {date}",
                        inline=False,
                    )
                    counter += 1
                    if counter > 24:
                        break
                await ctx.response.send_message(embed=em, ephemeral=True)
                break
        else:

            await ctx.response.send_message(embed=em, ephemeral=True)


def setup(client: DragonBot):
    client.add_cog(UserCog(client))
