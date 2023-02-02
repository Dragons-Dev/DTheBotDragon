import aiosqlite
from config import DBPATH, DBFOLD
import os


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
            type TEXT, 
            member INTEGER,
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
            """)
            response = await cursor.fetchone()
            if response is None:
                return None
            else:
                return response[0]


async def add_warn():
    pass
