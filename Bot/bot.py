import logging
import sys
from discord.ext import commands
from Bot._config import TOKEN, PREFIX

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

bot = commands.Bot(command_prefix=PREFIX)
cogs = ['Character.bot']

@bot.event
async def on_ready():
    for cog in cogs:
        bot.load_extension(cog)
    print('Ready...')

@bot.event
async def on_command(ctx):
    command = ctx.message.content
    channel = ctx.message.channel.name
    user = ctx.message.author.name + '#' + ctx.message.author.discriminator

    logger.info('Received command "%s" in %s from %s', command, channel, user)

if __name__ == '__main__':
    bot.run(TOKEN)