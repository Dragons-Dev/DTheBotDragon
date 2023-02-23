import datetime
import logging
import json

import discord
import pomice
from discord.ext import commands, tasks


import config
from utils import db, logger

log = logging.getLogger("DragonLog")


ascii_art = """
╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╱╭━━╮╱╱╱╭╮
╰╮╭╮┃╱╱╱╱╱╱╱╱╱╱╱╱╱┃╭╮┃╱╱╭╯╰╮
╱┃┃┃┣━┳━━┳━━┳━━┳━╮┃╰╯╰┳━┻╮╭╯
╱┃┃┃┃╭┫╭╮┃╭╮┃╭╮┃╭╮┫╭━╮┃╭╮┃┃
╭╯╰╯┃┃┃╭╮┃╰╯┃╰╯┃┃┃┃╰━╯┃╰╯┃╰╮
╰━━━┻╯╰╯╰┻━╮┣━━┻╯╰┻━━━┻━━┻━╯
╱╱╱╱╱╱╱╱╱╭━╯┃
╱╱╱╱╱╱╱╱╱╰━━╯
"""


def pre_start_hook():
    print(ascii_art)
    client.load_extensions("extensions", recursive=True)


class DragonBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_start = True
        self.pool = pomice.NodePool()

    async def con_nodes(self):
        with open("lavalinks.json", "r") as f:
            data: dict = json.load(f)
        await self.wait_until_ready()
        for node, values in data.items():
            await self.pool.create_node(
                bot=self,
                host=values["HOST"],
                port=values["PORT"],
                password=values["PASSWORD"],
                secure=values["SECURE"],
                identifier=node,
                spotify_client_id=(
                    None if values["SPOTIFY_ID"] == "" else values["SPOTIFY_ID"]
                ),
                spotify_client_secret=(
                    None if values["SPOTIFY_SECRET"] == "" else values["SPOTIFY_SECRET"]
                ),
            )
            log.info(
                f"Lavalink {node} connected on {'https' if values['SECURE'] is True else 'http'}://{values['HOST']}:{values['PORT']}"
            )

    async def on_ready(self) -> None:
        if self.first_start:
            log.info(
                f"Bot started as {self.user.name}#{self.user.discriminator} | {self.user.id}"
            )
            await db.set_up()
            log.debug("Database setup successful")
            await self.con_nodes()
            self.first_start = False


client = DragonBot(
    command_prefix=commands.when_mentioned,
    case_insensitive=True,
    strip_after_prefix=True,
    intents=discord.Intents.all(),
    debug_guilds=config.GUILDS,
    activity=discord.Activity(type=discord.ActivityType.watching, name="you"),
    state=discord.Status.online,
)


if __name__ == "__main__":
    pre_start_hook()
    client.run(config.DISCORD_TOKEN)
