import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
import discord

from discord.ext import commands

from cogs.error_handler import GenericErrorHandler
from cogs.settings import UserCog
from fb.env import (
    DISCORD_TOKEN,
    LOG_LEVEL,
    SENTRY_DSN,
)
from tasks import travel_task, alerts_task


logger = logging.getLogger(__name__)
logging.basicConfig(level=getattr(logging, LOG_LEVEL))

if SENTRY_DSN:
    sentry_logging = LoggingIntegration(
        level=logging.DEBUG,       # Capture info and above as breadcrumbs
        event_level=logging.ERROR  # Send errors as events
    )

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[sentry_logging, AioHttpIntegration()]
    )


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(activity=discord.Game(name='Torn City', type=1, url='https://www.torn.com'))
    print(f'Successfully logged in and booted...!')


bot.add_cog(GenericErrorHandler(bot))
bot.add_cog(UserCog(bot))
bot.loop.create_task(alerts_task(bot))
bot.loop.create_task(travel_task(bot))
bot.run(DISCORD_TOKEN)


