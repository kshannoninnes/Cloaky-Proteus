from discord.ext import commands

from Character.controller import get_character_id, get_closest_match, get_character_stats


class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='who'
    )
    async def who(self, ctx, *, pilot_name:str=None):
        """Look up an EVE Online character by name

        Use double quotes to force a strict match. eg. !who "Nosy" will not match a character named Nosy Fucker
        """
        if not pilot_name or len(pilot_name) < 3:
            return await ctx.channel.send('Character name too short, 3 characters minimum')

        returned = await get_character_id(pilot_name)
        if not returned:
            return await ctx.channel.send('Character not found')
        else:
            if len(returned['character']) > 1:
                char_id = await get_closest_match(pilot_name, returned['character'])
            else:
                char_id = returned['character'][0]

            character = await get_character_stats(char_id)

            return await ctx.channel.send(embed=character)

def setup(bot):
    bot.add_cog(Character(bot))