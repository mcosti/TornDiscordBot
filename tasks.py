import asyncio
import logging

from fb.entrypoint import generate_alerts
from fb.env import FREQUENCY, DRUGS_CHANNEL, PLUSHIES_CHANNEL, FLOWERS_CHANNEL, TRAVEL_FREQUENCY
from travel import get_embeds, ItemTypes


async def alerts_task(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        alerts = await generate_alerts()
        for key, alerts_list in alerts.items():
            user = bot.get_user(key)
            if not user:
                pass

            text = "\n".join([alert.to_discord() for alert in alerts_list])
            await user.send(text)
        await asyncio.sleep(FREQUENCY)


async def travel_task(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        drugs_channel = bot.get_channel(DRUGS_CHANNEL)
        plushies_channel = bot.get_channel(PLUSHIES_CHANNEL)
        flowers_channel = bot.get_channel(FLOWERS_CHANNEL)
        logging.info("Fetching stocks")
        embeds = get_embeds()

        if drugs_channel:
            for embed in embeds[ItemTypes.DRUG]:
                await drugs_channel.send(embed=embed)

        if plushies_channel:
            for embed in embeds[ItemTypes.PLUSHIE]:
                await plushies_channel.send(embed=embed)

        if flowers_channel:
            for embed in embeds[ItemTypes.FLOWER]:
                await flowers_channel.send(embed=embed)

        await asyncio.sleep(TRAVEL_FREQUENCY)