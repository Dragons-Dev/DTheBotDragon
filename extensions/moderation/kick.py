import datetime

import discord
from discord.ext import commands

from DragonBot import DragonBot
from utils import db


class KickCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="kick", description="kicks a given member")
    async def kick(
        self,
        ctx: discord.ApplicationContext,
        user: discord.Option(
            input_type=discord.SlashCommandOptionType.user,
            description="mention a user to kick him",
        ),
        reason: discord.Option(
            description="a reason for the kick",
        ),
    ):
        team_id = await db.get_setting(setting="team role", guild=str(ctx.guild_id))
        if team_id is None:
            return await ctx.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You have not set up a team role.\nPlease set up a team role by running /settings 'Team Role' 'your team role id'",
                    color=discord.Color.brand_red(),
                ),
                ephemeral=True,
            )
        for role in ctx.author.roles:
            if int(team_id[0]) == int(role.id):
                user = user.strip("<@!>")
                user = ctx.guild.get_member(int(user))
                await ctx.guild.kick(user=user, reason=reason)
                log = await db.get_setting(
                    setting="mod log channel", guild=ctx.guild_id
                )
                em = discord.Embed(
                    description=f"**Member: **{user.name}#{user.discriminator} ({user.id})\n**Action: **Kick\n**Reason: **{reason}",
                    timestamp=datetime.datetime.now(),
                    color=discord.Color.red(),
                )
                em.set_author(
                    name=f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})",
                    icon_url=ctx.author.display_avatar,
                )
                em.set_footer(
                    text=f"Case: {len(await db.get_mod_action(action = '*'))}"
                )
                await db.add_mod_action(
                    member=user.id,
                    moderator=ctx.author.id,
                    reason=reason,
                    action="kick",
                )
                if log is None:
                    await ctx.response.send_message(
                        content=f"Please set a log channel to send logs.",
                        embed=em,
                        ephemeral=True,
                    )

                else:
                    log = self.client.get_channel(int(log[0]))
                    await ctx.response.send_message(embed=em, ephemeral=True)
                    await log.send(embed=em)
                break
        else:
            await ctx.response.send_message(
                f"You are not allowed to kick a user.", ephemeral=True
            )


def setup(client: DragonBot):
    client.add_cog(KickCog(client))
