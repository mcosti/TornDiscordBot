import asyncio
import aiohttp
import requests
import logging

from .exceptions import TornException


class TornAPI:
    endpoint = 'https://api.torn.com/user/'

    @staticmethod
    def fetch_for_key(key):
        params = {
            'key': key,
            'selections': 'notifications,events,messages,travel,cooldowns,bars,basic,icons',
        }

        resp = requests.get(TornAPI.endpoint, params).json()
        if 'error' in resp:
            raise TornException(**resp['error'])

        return resp

    @staticmethod
    async def fetch_torn_user_data(session, params, id):
        # return dummyTornRequest
        async with session.get(TornAPI.endpoint, params=params) as response:
            resp = await response.json()
            if 'error' in resp:
                raise TornException(user_id=id, **resp['error'])

            return resp

    @staticmethod
    async def run(users):
        """ Gather many HTTP call made async
        Args:
            users: a list of Users
        Return:
            responses: A list of dict like object containing http response
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for user in users:
                tasks.append(
                    TornAPI.fetch_torn_user_data(
                        session,
                        user.params,
                        user.id
                    )
                )

            responses = await asyncio.gather(*tasks, return_exceptions=True)
            return responses

    @staticmethod
    async def fetch_all(users):
        logging.info("Fetching torn data for all users")
        responses = await TornAPI.run(users)
        logging.info("Done fetching")
        return responses
