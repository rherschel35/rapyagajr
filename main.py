"""
Entry point for RaptorYagaJR - a small, single-purpose Discord bot.

It watches messages in specific channels and, whenever the letters "rap"
show up anywhere in a message (case-insensitive, as part of any word),
replies with "rip". See cogs/raptor.py for the actual logic.
"""

import asyncio
import logging
import os

import discord
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("raptor")

INITIAL_COGS = ["cogs.raptor"]


class RaptorBot(commands.Bot):
    async def setup_hook(self):
        for cog in INITIAL_COGS:
            await self.load_extension(cog)
            log.info("Loaded %s", cog)
        synced = await self.tree.sync()
        log.info("Synced %d global commands", len(synced))


def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN environment variable is not set")

    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True

    bot = RaptorBot(command_prefix="!", intents=intents, help_command=None)

    @bot.event
    async def on_ready():
        log.info("RaptorYagaJR has arrived. Logged in as %s (id=%s)", bot.user, bot.user.id)

    bot.run(token, log_handler=None)


if __name__ == "__main__":
    main()
