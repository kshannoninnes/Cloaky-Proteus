import Esi.commands as esi
import discord
import urllib.parse
from discord.ext import commands

class CharacterBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='who',
        description='Evewho character lookup'
    )
    async def who(self, ctx):
        arg = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with):]
        returned = await esi.search(arg)
        if not returned:
            await ctx.channel.send('Character not found')
        elif len(returned['character']) > 1:
            await ctx.channel.send('Multiple matches, aborting...')
        else:
            id = returned['character'][0]
            character = await esi.get_character(id)

            name = character['name']
            corp = await esi.get_corporation(character['corporation_id'])
            portrait = await esi.get_portrait(id)
            links = [
                'https://zkillboard.com/character/' + str(id),
                'https://evewho.com/pilot/' + urllib.parse.quote_plus(name)
            ]

            embed = discord.Embed(
                title = name,
                color=184076,
                description=corp['name']
            ).set_thumbnail(
                url=portrait['px512x512']
            ).add_field(
                name='Last Active',
                value='N/A'
            ).add_field(
                name = 'Links',
                value = '\n'.join(links)
            )

            await ctx.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(CharacterBot(bot))