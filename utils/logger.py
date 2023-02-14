import datetime
import logging
import os
from pathlib import Path


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, style="{", datefmt="%d-%m-%y %H:%M:%S")
        return formatter.format(record)


FMT = "[{levelname:^9}] [{asctime}] [{name}] [{module}:{lineno}] : {message}"
FORMATS = {
    logging.DEBUG: f"\33[37m{FMT}\33[0m",
    logging.INFO: f"\33[36m{FMT}\33[0m",
    logging.WARNING: f"\33[33m{FMT}\33[0m",
    logging.ERROR: f"\33[31m{FMT}\33[0m",
    logging.CRITICAL: f"\33[1m\33[31m{FMT}\33[0m",
}


log = logging.getLogger("DragonLog")
log.setLevel(logging.DEBUG)
if not Path("logs").exists():
    os.mkdir("logs")
if len(os.listdir("logs")) > 7:
    for file in os.listdir("logs"):
        os.remove("logs/" + file)
        break

log_path = f"logs/{log.name} {datetime.datetime.now().strftime('%Y-%m-%d')}.log"
file_format = logging.Formatter(
    "[{levelname:^9}] [{asctime}] [{name}] [{module:^4}:{lineno:^4}] | {message}",
    style="{",
    datefmt="%d-%m-%y %H:%M:%S",
)


file_handler = logging.FileHandler(log_path, "w")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_format)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(CustomFormatter())

log.addHandler(file_handler)
log.addHandler(console_handler)
