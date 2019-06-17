from Esi._config import USER_AGENT

ZKILL_URL = 'https://zkillboard.com/api/{}/'
DEFAULT_HEADERS = {'Accept-Encoding': 'gzip', 'User-Agent': USER_AGENT}
TIME_TO_CACHE = 3600
MAX_ITEMS = 300