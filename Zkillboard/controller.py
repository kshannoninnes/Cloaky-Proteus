from aiohttp import ClientSession
from asyncache import cached
from cachetools import TTLCache

from Discord.bot import logger
from Esi.controller import get_killmail
from Zkillboard.config import ZKILL_URL, DEFAULT_HEADERS, TIME_TO_CACHE, MAX_ITEMS


@cached(TTLCache(maxsize=MAX_ITEMS, ttl=TIME_TO_CACHE))
async def get_last_killmail(char_id):
    url = ZKILL_URL.format('characterID/' + str(char_id))
    recent_killmails = await _make_request(url)
    if recent_killmails:
        last_id = recent_killmails[0]['killmail_id']
        last_hash = recent_killmails[0]['zkb']['hash']
        last_killmail = await get_killmail(last_id, last_hash)
        return last_killmail
    else:
        return None


async def _make_request(uri):
    async with ClientSession(headers=DEFAULT_HEADERS) as session:
        async with session.get(uri) as res:
            if res.status in range(200, 300):
                return await res.json()
            else:
                logger.warn('Error retrieving data from zkill')
                logger.error(res)
                return None
