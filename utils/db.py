import os
import datetime

import aiosqlite

from config import DBPATH, DBFOLD


async def set_up() -> None:
    if not DBFOLD.exists():
        os.mkdir(DBFOLD)
        if not DBPATH.exists():
            open(DBPATH, "w").close()
    async with aiosqlite.connect(DBPATH) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS mod_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            member INTEGER,
            moderator INTEGER,
            reason TEXT,
            action TEXT, 
            time timestamp)
            """)

            await cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
            setting TEXT,
            value TEXT,
            guild INTEGER)
            """)

        await conn.commit()


async def insert_setting(setting: str, value: str, guild: int):
    setting = setting.lower()
    value = value.lower()
    async with aiosqlite.connect(DBPATH) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            SELECT value FROM settings where setting = ? AND guild = ?
            """, (setting, guild))
            response = await cursor.fetchone()
            if response is None:
                await cursor.execute("""
                INSERT INTO settings (setting, value, guild) VALUES (?, ?, ?)
                """, (setting, value, guild))
            else:
                await cursor.execute("""
                UPDATE settings SET value = ? WHERE setting = ? AND guild = ?
                """, (value, setting, guild))
        await conn.commit()


async def get_setting(setting: str, guild: int) -> str | None:
    setting = setting.lower()
    async with aiosqlite.connect(DBPATH) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            SELECT value FROM settings where setting = ? AND guild = ?
            """, (setting, guild))
            response = await cursor.fetchone()
            if response is None:
                return None
            else:
                return response


async def add_mod_action(member: int, moderator: int, reason: str, action: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DBPATH) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
            INSERT INTO mod_actions (member, moderator, reason, action, time) VALUES (?, ?, ?, ?, ?)
            """, (member, reason, action.lower(), timestamp))
        await conn.commit()


async def get_mod_action(member: int = None, action: str = None) -> tuple | list[tuple] | None:
    if member is not None:
        async with aiosqlite.connect(DBPATH) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    SELECT id, moderator, reason, action, time FROM mod_actions WHERE member = ?
                    """, (member,))
                response = await cursor.fetchall()
                if response is None:
                    return None
                else:
                    return response
    if action is not None:
        pass
