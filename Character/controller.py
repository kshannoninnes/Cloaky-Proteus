import math
import asyncio
from datetime import datetime
from urllib.parse import quote_plus

from Esi.controller import search, get_character, get_corporation, get_portrait
from Zkillboard.controller import get_last_killmail


async def get_character_id(pilot_name):
    pilot_name = pilot_name.strip()
    strict = pilot_name.startswith('"') and pilot_name.endswith('"')
    pilot_name = pilot_name.strip('"')
    if strict:
        return await search(pilot_name, strict=True)
    else:
        return await search(pilot_name)

async def get_character_stats(char_id):
    stats = {}

    character, recent = await asyncio.gather(
        get_character(char_id),
        get_last_killmail(char_id)
    )

    stats['activity'] = 'Never' if not recent else await _last_active(recent['killmail_time'])

    stats['name'] = character['name']
    stats['corp'], stats['portrait'] = await asyncio.gather(
        get_corporation(character['corporation_id']),
        get_portrait(char_id)
    )
    stats['links'] = [
        'https://zkillboard.com/character/' + str(char_id),
        'https://evewho.com/pilot/' + quote_plus(stats['name'])
    ]

    return stats


async def _school_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)


async def _simplify_timedelta(timedelta, precise=False):
    days = timedelta.days
    hours = timedelta.total_seconds() / 60.0 / 60.0 - (days * 24)

    result = 'Today' if days < 1 else str(days) + ' days {}'

    if precise:
        return result.format(str(math.trunc(hours)) + ' hours ago')
    else:
        return result.format('ago')


async def _last_active(last_killmail):
    last_kill = datetime.strptime(last_killmail, '%Y-%m-%dT%H:%M:%SZ')
    difference = datetime.utcnow() - last_kill

    return await _simplify_timedelta(difference)
