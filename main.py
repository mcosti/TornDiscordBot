import asyncio
from pprint import pprint

from fb.entrypoint import generate_alerts

loop = asyncio.get_event_loop()
get_alerts = loop.run_until_complete(generate_alerts())
pprint(get_alerts)
