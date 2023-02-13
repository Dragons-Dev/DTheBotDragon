import sqlite3
import datetime
import random
import asyncio
from config import DBPATH


def add_mod_action(member: int, moderator: int, reason: str, action: str) -> None:
    timestamp = datetime.datetime.now()
    conn = sqlite3.connect(r"E:\DragonBot\data\main.sqlite")
    cursor = conn.cursor()
    for _ in range(500):
        cursor.execute(
            """
        INSERT INTO mod_actions (member, moderator, reason, action, time) VALUES (?, ?, ?, ?, ?)
        """,
            (member, moderator, reason, action.lower(), timestamp),
        )
    conn.commit()


mods = [
    622130169657688074,
    511219492332896266,
    695695261669785691,
    239151351341383680,
    579395061222080563,
    723520858559348766,
    701027384840814623,
    514845794969583616
]

for i in range(500):
    add_mod_action(
        member = random.choice(mods),
        moderator = random.choice(mods),
        reason = "DB Spammer",
        action = "Warn")



