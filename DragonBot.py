import datetime
import logging

import discord
import pomice
from discord.ext import commands, tasks
import wavelink


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
        await self.wait_until_ready()
        await self.pool.create_node(
            bot=self,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
            identifier="MAIN",
        )

    async def on_ready(self) -> None:
        if self.first_start:
            log.info(
                f"Bot started as {self.user.name}#{self.user.discriminator} | {self.user.id}"
            )
            await db.set_up()
            log.debug("Database setup successful")
            await self.con_nodes()
            # await wavelink.NodePool.create_node(
            #    bot=self, host="127.0.0.1", port=2333, password="youshallnotpass"
            # )
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
