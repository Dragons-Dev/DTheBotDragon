import logging

import discord
from discord.ext import commands
import pomice

from DragonBot import DragonBot
from DragonPlayer.DragonPlayer import DragonPlayer
from utils import utils


class StatsCog(commands.Cog):
    def __init__(self, client):
        self.client: DragonBot = client

    @commands.slash_command(
        name="stats",
        description="Show some statistics about the bot and the music node",
    )
    async def stats(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if not ctx.voice_client:
            node = self.client.pool.get_best_node(
                algorithm=pomice.NodeAlgorithm.by_ping
            )
        else:
            player: DragonPlayer = ctx.voice_client
            node = player.node
        n_stats = node.stats
        em = discord.Embed(
            title="Lavalink Statistics",
            description=f"""
```
Node      | {node._identifier}
CPU Load  | {round(float(n_stats.cpu_system_load), 2)}% on {n_stats.cpu_cores} Cores
RAM Usage | {round(float(n_stats.used/(1024*1024*1024)), 2)}GB/{round(float(n_stats.allocated/(1024*1024*1024)), 2)}GB
Players   | {n_stats.players_active} active from {n_stats.players_total} total
Uptime    | {utils.sec_to_min(n_stats.uptime/1000)}
Ping      | {int(node.ping)}ms
```""",
            color=discord.Color.purple(),
        )
        await ctx.followup.send(embed=em)


def setup(client: DragonBot):
    client.add_cog(StatsCog(client))
