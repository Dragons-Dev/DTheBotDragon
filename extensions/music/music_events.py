import logging

import wavelink
import discord
from discord.ext import commands

import utils.utils
from DragonBot import DragonBot
from utils import db


log = logging.getLogger("DragonLog")


class MusicEvent(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener("on_wavelink_node_ready")
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        log.debug(f"Node {node.host} loaded with {node.identifier} as identifier")

    @commands.Cog.listener("on_wavelink_track_start")
    async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
        message_id = await db.get_setting(setting = "music_panel",
                                          guild = player.guild.id)
        channel_id = await db.get_setting(setting = "music_panel_channel",
                                          guild = player.guild.id)

        msg = await utils.utils.fetch_or_get_message(client = player.client,
                                                     message_id = int(message_id[0]),
                                                     channel_id = int(channel_id[0]))

def setup(client: DragonBot):
    client.add_cog(MusicEvent(client))
