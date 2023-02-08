import datetime

import discord
from discord.ext import commands

from DragonBot import DragonBot
from utils import db


class TimeoutCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="timeout", description="Timeout a user for a specified amount of time"
    )
    async def timeout(
        self,
        ctx: discord.ApplicationContext,
        user: discord.Option(
            input_type=discord.SlashCommandOptionType.user,
            description="mention a user to timeout him",
        ),
        time: discord.Option(
            required=True,
            choices=[
                discord.OptionChoice("10 s"),
                discord.OptionChoice("5 m"),
                discord.OptionChoice("10 m"),
                discord.OptionChoice("30 m"),
                discord.OptionChoice("1 h"),
                discord.OptionChoice("2 h"),
                discord.OptionChoice("3 h"),
                discord.OptionChoice("6 h"),
                discord.OptionChoice("12 h"),
                discord.OptionChoice("1 d"),
                discord.OptionChoice("2 d"),
                discord.OptionChoice("3 d"),
                discord.OptionChoice("4 d"),
                discord.OptionChoice("5 d"),
                discord.OptionChoice("6 d"),
                discord.OptionChoice("1 w"),
                discord.OptionChoice("2 w"),
                discord.OptionChoice("3 w"),
                discord.OptionChoice("4 w"),
            ],
        ),
        reason: discord.Option(
            description = "a reason for the timeout",
            )
    ):
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
                user = user.strip("<@!>")
                user = ctx.guild.get_member(int(user))
                time, duration = time.split(" ")
                time = int(time)
                if duration == "s":
                    timeout = datetime.timedelta(seconds=time)
                elif duration == "m":
                    timeout = datetime.timedelta(minutes=time)
                elif duration == "h":
                    timeout = datetime.timedelta(hours=time)
                elif duration == "d":
                    timeout = datetime.timedelta(days=time)
                elif duration == "w":
                    timeout = datetime.timedelta(weeks=time)
                else:
                    await ctx.response.send_message(
                        "This should never happen", ephemeral=True
                    )
                until = datetime.datetime.utcnow() + timeout
                await user.timeout(until=until, reason="Not given for now")
                log = await db.get_setting(
                    setting="mod log channel", guild=ctx.guild_id
                )
                em = discord.Embed(
                    description = f"**Member: **{user.name}#{user.discriminator} ({user.id})\n**Action: **Timeout until {until.strftime('%d.%m.%Y %H:%M')}\n**Reason: **{reason}",
                    timestamp = datetime.datetime.now(),
                    color = discord.Color.gold(),
                )
                em.set_author(
                    name = f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})",
                    icon_url = ctx.author.display_avatar,
                )
                em.set_footer(text = f"Case: {len(await db.get_mod_action(action = '*'))}")
                if log is None:
                    await ctx.response.send_message(
                        content = f"Please set a log channel to send logs.",
                        embed = em,
                        ephemeral = True,
                    )

                else:
                    log = self.client.get_channel(int(log[0]))
                    await ctx.response.send_message(embed = em, ephemeral = True)
                    await log.send(embed = em)
                break
        else:
            await ctx.response.send_message(f"You are not allowed to timeout a user.")


def setup(client: DragonBot):
    client.add_cog(TimeoutCog(client))
