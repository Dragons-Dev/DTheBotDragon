import asyncio
import logging
import json
import random

import aiohttp
import discord
import pomice
from discord.ext import commands
from pycord import multicog


import config
from views import verification_v, board_v, counter_v, join2create_v
from utils import db, logger, statics

log = logging.getLogger("DragonLog")


def pre_start_hook() -> None:
    print(
        """
╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╱╭━━╮╱╱╱╭╮
╰╮╭╮┃╱╱╱╱╱╱╱╱╱╱╱╱╱┃╭╮┃╱╱╭╯╰╮
╱┃┃┃┣━┳━━┳━━┳━━┳━╮┃╰╯╰┳━┻╮╭╯
╱┃┃┃┃╭┫╭╮┃╭╮┃╭╮┃╭╮┫╭━╮┃╭╮┃┃
╭╯╰╯┃┃┃╭╮┃╰╯┃╰╯┃┃┃┃╰━╯┃╰╯┃╰╮
╰━━━┻╯╰╯╰┻━╮┣━━┻╯╰┻━━━┻━━┻━╯
╱╱╱╱╱╱╱╱╱╭━╯┃
╱╱╱╱╱╱╱╱╱╰━━╯
"""
    )
    client.load_extensions("extensions", recursive=True)
    multicog.apply_multicog(client)


class DragonBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_start = True
        self.pool = pomice.NodePool()

    async def read_nodes(self):
        with open("lavalinks.json", "r") as f:
            data: dict = json.load(f)
        tasks = [
            asyncio.create_task(self.connect_node(key, value))
            for key, value in data.items()
        ]
        await self.wait_until_ready()
        await asyncio.gather(*tasks)
        log.info(f"We got {len(self.pool.nodes)} Nodes in total.")

    async def connect_node(self, node, values):
        identifier = node.upper()
        try:
            await self.pool.create_node(
                bot=self,
                host=values["HOST"],
                port=values["PORT"],
                password=values["PASSWORD"],
                secure=values["SECURE"],
                identifier=identifier,
                fallback=True,
                log_level=logging.WARNING,
                spotify_client_id=(
                    None if values["SPOTIFY_ID"] == "" else values["SPOTIFY_ID"]
                ),
                spotify_client_secret=(
                    None if values["SPOTIFY_SECRET"] == "" else values["SPOTIFY_SECRET"]
                ),
            )
            log.info(
                f"Lavalink '{identifier}' connected on {'https' if values['SECURE'] is True else 'http'}://{values['HOST']}:{values['PORT']}"
            )
        except pomice.NodeConnectionFailure:
            log.warning(
                f"Node didn't respond: Lavalink '{identifier}' didn't connect on {'https' if values['SECURE'] is True else 'http'}://{values['HOST']}:{values['PORT']}"
            )
        except pomice.LavalinkVersionIncompatible:
            log.error(
                f"Incompatible Lavalink Version:  '{identifier}' didn't connect on {'https' if values['SECURE'] is True else 'http'}://{values['HOST']}:{values['PORT']}"
            )
        except ValueError:
            log.warning(
                f"ValueError: Lavalink '{identifier}' didn't connect on {'https' if values['SECURE'] is True else 'http'}://{values['HOST']}:{values['PORT']}"
            )
        except aiohttp.ContentTypeError:
            log.warning(
                f"ContentTypeError: Lavalink '{identifier}' had issues on {'https' if values['SECURE'] is True else 'http'}://{values['HOST']}:{values['PORT']}"
            )

    async def on_ready(self) -> None:
        if self.first_start:
            self.add_view(verification_v.VerificationView())
            self.add_view(counter_v.CounterView())
            self.add_view(join2create_v.Join2CreateBoard())
            await db.set_up()
            log.debug("Database setup successful")
            if config.MUSIC_ENABLED:
                await self.read_nodes()
            self.first_start = False
            log.info(f"Bot started as {self.user.name}#{self.user.discriminator} | {self.user.id}")
            await asyncio.sleep(10)
            await self.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name=f"{len(self.users)} users"
                ),
                status=discord.Status.online,
            )

client = DragonBot(
    command_prefix=commands.when_mentioned,
    case_insensitive=True,
    strip_after_prefix=True,
    intents=discord.Intents.all(),
    debug_guilds=config.GUILDS,
    activity=discord.Activity(type=discord.ActivityType.playing, name="starting"),
    status=discord.Status.dnd,
)


if __name__ == "__main__":
    pre_start_hook()
    client.run(config.DISCORD_TOKEN)
