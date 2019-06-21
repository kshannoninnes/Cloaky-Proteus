from discord import Embed
from discord.ext import commands

from Character.controller import get_character_id, get_character_stats


class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='who',
        description='EVE Online Character Lookup'
    )
    async def who(self, ctx):
        """Look up an EVE Online character by name

        Use double quotes to force a strict match.
        """
        pilot_name = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with):]

        if not len(pilot_name):
            return await ctx.channel.send('Character name too short, 3 characters minimum')

        returned = await get_character_id(pilot_name)
        if not returned:
            return await ctx.channel.send('Character not found')
        elif len(returned['character']) > 1:
            return await ctx.channel.send('Multiple matches, aborting...')
        else:
            char_id = returned['character'][0]
            character = await get_character_stats(char_id)

            embed = Embed(
                title = character['name'],
                color=184076,
                description=character['corp']['name']
            ).set_thumbnail(
                url=character['portrait']['px512x512']
            ).add_field(
                name='Last Active',
                value=character['activity']
            ).add_field(
                name = 'Links',
                value = '\n'.join(character['links'])
            )

            return await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Character(bot))