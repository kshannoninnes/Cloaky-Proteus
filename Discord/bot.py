import warnings
import logging
import sys

from discord.ext import commands

from Discord._config import TOKEN, PREFIX

bot = commands.Bot(command_prefix=PREFIX)

warnings.filterwarnings('ignore', message='Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning')

@bot.event
async def on_ready():
    for cog in cogs:
        bot.load_extension(cog)
    logger.info('Ready!')

@bot.event
async def on_command(ctx):
    command = ctx.message.content
    channel = ctx.message.channel.name
    user = ctx.message.author.name + '#' + ctx.message.author.discriminator

    logger.info('Received command "%s" in %s from %s', command, channel, user)

@bot.event
async def on_error(event, *args, **kwargs):
        exception = sys.exc_info()[1]
        message = str(exception.args[0])
        if isinstance(exception, ConnectionError):
            sys.exit(message)
        else:
            logger.error(message + ' ' + exception.original.msg)

def _load_logger():
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log

logger = _load_logger()
cogs = ['Character.commands']

if __name__ == '__main__':
    bot.run(TOKEN)