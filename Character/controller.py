import math
import asyncio
from datetime import datetime
from discord import Embed
from urllib.parse import quote_plus
from fuzzywuzzy import process

from Esi.controller import search, get_character, get_all_characters, get_corporation, get_portrait
from Zkillboard.controller import get_last_killmail


async def get_character_id(pilot_name):
    pilot_name = pilot_name.strip()
    strict = pilot_name.startswith('"') and pilot_name.endswith('"')
    pilot_name = pilot_name.strip('"')
    if strict:
        return await search(pilot_name, strict=True)
    else:
        return await search(pilot_name)

async def get_closest_match(pilot_name, char_list):
    all_chars = await get_all_characters(char_list)
    char_names = []

    for char in all_chars:
        char_names.append(char['name'])

    closest_name = process.extractOne(pilot_name, char_names)
    closest = next((char for char in all_chars if char['name'] == closest_name[0]), None)

    return closest['id']

async def get_character_stats(char_id):
    stats = {'links': []}

    character, recent = await asyncio.gather(
        get_character(char_id),
        get_last_killmail(char_id)
    )
    stats['name'] = character['name']
    stats['activity'] = 'Never' if not recent else await _last_active(recent['killmail_time'])

    stats['corp'], stats['portrait'], stats['links'] = await asyncio.gather(
        get_corporation(character['corporation_id']),
        get_portrait(char_id),
        _get_character_links(id=char_id, name=character['name'])
    )

    return await _build_character_embed(stats)

async def _get_character_links(**character):
    return await asyncio.gather(
        _build_markdown_hyperlink('Zkillboard', 'https://zkillboard.com/character/' + str(character['id']) + '/'),
        _build_markdown_hyperlink('Evewho', 'https://evewho.com/pilot/' + quote_plus(character['name']))
    )

async def _build_character_embed(character):
    embed = Embed(
        title=character['name'],
        color=184076,
        description=character['corp']['name']
    ).set_thumbnail(
        url=character['portrait']['px512x512']
    ).add_field(
        name='Last Active',
        value=character['activity']
    ).add_field(
        name='Links',
        value='\n'.join(character['links']),
        inline=False
    )

    return embed

async def _build_markdown_hyperlink(text, url):
    return '[' + text + '](' + url + ')'


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
