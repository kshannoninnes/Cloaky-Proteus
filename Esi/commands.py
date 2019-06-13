from Bot.bot import logger
import json

from esipy import EsiApp, EsiClient
from Esi._config import USER_AGENT

esi = EsiApp().get_latest_swagger
client = EsiClient(
    retry_requests=True,
    headers={'User-Agent': USER_AGENT},
    raw_body_only=True
)


async def search(query, category='character', strict=False):
    """
    Search EVE entities
    :param query: Term to search for
    :param category: List of categories to check
    :param strict: Whether to use strict search.
    :return: search results
    """
    operation = esi.op['get_search'](categories=category, search=query, strict=strict)
    result = client.request(operation)

    return await _check_result(result)

async def get_character(id):
    return await _id_op('get_characters_character_id', character_id=id)

async def get_portrait(id):
    return await _id_op('get_characters_character_id_portrait', character_id=id)

async def get_corporation(id):
    return await _id_op('get_corporations_corporation_id', corporation_id=id)

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
        raise ValueError(dict.get('error', ''))
