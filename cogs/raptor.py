"""
The bot's one and only trick: whenever a message contains the letters
"rap" in a row, anywhere, in any word (case-insensitive) - "rap", "wrap",
"grape", "scraps", all of it - reply with "rip".

It also joins in: when someone else says "rip" (as its own word - "rip",
"RIP", "rip bro", "R.I.P." - but not "trip" or "script"), it says "rip" too.
It never answers other bots, including itself, so it can't loop.

Restricted to specific channels via the RAPTOR_CHANNEL_IDS env var
(comma-separated channel IDs). If that's not set, it responds anywhere it
can see messages.
"""

import logging
import os
import re

import discord
from discord.ext import commands

log = logging.getLogger("raptor.trigger")

TRIGGER = "rap"
REPLY = "rip"

# "rip" as a word of its own, dots allowed: rip, RIP, r.i.p, R.I.P.
RIP_PATTERN = re.compile(r"(?<![a-z0-9])r\.?i\.?p\.?(?![a-z0-9])", re.IGNORECASE)


def should_reply(content: str) -> bool:
    text = (content or "").lower()
    return TRIGGER in text or bool(RIP_PATTERN.search(text))


def _parse_channel_ids(env_value: str | None):
    if not env_value:
        return None
    ids = set()
    for part in env_value.split(","):
        part = part.strip()
        if part.isdigit():
            ids.add(int(part))
    return ids or None


class Raptor(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.allowed_channel_ids = _parse_channel_ids(os.getenv("RAPTOR_CHANNEL_IDS"))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if not message.guild:
            return
        if self.allowed_channel_ids and message.channel.id not in self.allowed_channel_ids:
            return

        if not should_reply(message.content):
            return

        try:
            await message.channel.send(REPLY)
        except discord.HTTPException:
            log.exception("Failed to send reply in %s", message.channel.id)


async def setup(bot: commands.Bot):
    await bot.add_cog(Raptor(bot))
