import datetime
import logging

import discord
from discord.ext import commands, tasks
from wavelink import NodePool

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
        self.first_start = False

    async def on_ready(self) -> None:
        log.info(
            f"Bot started as {self.user.name}#{self.user.discriminator} | {self.user.id}"
        )
        await db.set_up()
        log.debug("Database setup successful")
        if not self.first_start:
            await NodePool.create_node(
                bot=self, host="localhost", port=2333, password="youshallnotpass"
            )
            self.first_start = True


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
