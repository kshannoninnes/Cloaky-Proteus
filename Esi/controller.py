import json
import time
from urllib.error import HTTPError

from esipy import EsiApp, EsiClient

from Discord.bot import logger
from Esi._config import USER_AGENT, MAX_RETRY


async def search(query, category='character', strict=False):
    return await _id_op('get_search', categories=category, search=query, strict=strict)

async def get_character(char_id):
    return await _id_op('get_characters_character_id', character_id=char_id)

async def get_portrait(char_id):
    return await _id_op('get_characters_character_id_portrait', character_id=char_id)

async def get_corporation(char_id):
    return await _id_op('get_corporations_corporation_id', corporation_id=char_id)

async def get_killmail(kill_id, kill_hash):
    return await _id_op('get_killmails_killmail_id_killmail_hash', killmail_id=kill_id, killmail_hash=kill_hash)

async def _id_op(op_type, **kwargs):
    operation = esi.op[op_type](**kwargs)
    result = client.request(operation)

    return await _check_result(result)

async def _check_result(result):
    valid_dict = json.loads(result.raw.decode('utf-8'))
    if result.status == 200:
        return valid_dict
    else:
        logger.error("{}: {}".format(result.status, valid_dict.get('error')))
        raise ValueError(valid_dict.get('error', ''))

def _load_esi():
    loaded = False
    count = 0
    while not loaded:
        if count < MAX_RETRY:
            count += 1
            try:
                esi_app = EsiApp().get_latest_swagger
                esi_client = EsiClient(
                    retry_requests=True,
                    headers={'User-Agent': USER_AGENT},
                    raw_body_only=True)
                loaded = True
                return esi_app, esi_client
            except HTTPError:
                logger.warning('Loading swagger failed ' + str(count) + '/' + str(MAX_RETRY) + ', retrying...')
                time.sleep(0.3)
                pass
        else:
            raise ConnectionError('Error loading swagger. Please restart the bot.')

esi, client = _load_esi()