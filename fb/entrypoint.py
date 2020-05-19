import asyncio
import logging
import atexit

from fb.alerts import Alert, AlertTypes
from fb.torn.TornAPI import TornAPI
from fb.models import DataComparator
from fb.torn.exceptions import TornException, TornErrorCode
from fb.torn.models import TornData
from fb.database import Database
from fb.env import LOG_LEVEL

logger = logging.getLogger()
logging.basicConfig(level=getattr(logging, LOG_LEVEL))


db = Database()


async def handle_errors(results):
    bad_users = []
    alerts = {}
    sleep = False
    for result in results:
        if isinstance(result, TornException):
            if result.users_fault:
                bad_users.append(result)

            if result.code == TornErrorCode.IP_BLOCK or result.torns_fault:
                sleep = True

        results.remove(result)

    for exc in bad_users:
        user = db.get_user(exc.user_id)
        db.delete_user(user)
        alerts[user.credentials.discord_id] = Alert(
            "Your torn key is invalid, so your account has been deleted",
            AlertTypes.INVALID_KEY
        )

    if sleep:
        logger.error("IP block or torn api problems. Sleeping for 30 minutes")
        await asyncio.sleep(30 * 60)
        logger.info("IP block sleep ended.")

    return alerts


async def generate_alerts():
    new_alerts = {}
    users = db.get_all_users()
    results = await TornAPI.fetch_all(users.values())
    error_alerts = await handle_errors(results)
    for discord_id, alert in error_alerts.items():
        new_alerts[discord_id] = [alert]

    users_torn_data = [TornData.from_data(data) for data in results]
    for new_user_data in users_torn_data:
        id = new_user_data.player_id
        try:
            user = users[id]
            alerts = DataComparator(user.torn_data, new_user_data, user.settings).compute_alerts()
            if alerts:
                new_alerts[user.credentials.discord_id] = alerts
            user.torn_data = new_user_data
            user.save(save_torn_data=True)

        except KeyError:
            logger.error(f"Could not find user {id} in firebase users. weird")
    return new_alerts


atexit.register(db.save_on_exit)
