import logging

import discord
from discord.ext import commands

from DragonBot import DragonBot
from utils import db


class NukeCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="nuke", description="Clears messages in the channel")
    async def nuke(
        self,
        ctx: discord.ApplicationContext,
        amount: discord.Option(
            int, description="the amount of messages to clear", required=False
        ),
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
        limit = int(amount) if amount is not None else 100
        for role in ctx.author.roles:
            if int(team_id[0]) == int(role.id):
                purge = await ctx.channel.purge(
                    limit=limit,
                    reason=f"Nuke by {ctx.author.name}#{ctx.author.discriminator}",
                )
                purge = len(purge)
                await ctx.response.send_message(
                    embed=discord.Embed(
                        title=f"{ctx.author.name}#{ctx.author.discriminator} nuked {ctx.channel.name}",
                        description=f"{'One message' if purge == 1 else 'Zero messages' if purge == 0 else f'{purge} messages'} died this way",
                        color=discord.Color.dark_red(),
                    ).set_image(
                        url="https://townsquare.media/site/136/files/2022/03/attachment-nuke-federal-cloud-website.jpg"
                    )
                )
                break
        else:
            await ctx.response.send_message(
                f"You are not allowed to nuke a channel.", ephemeral=True
            )


def setup(client: DragonBot):
    client.add_cog(NukeCog(client))
