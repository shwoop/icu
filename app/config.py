import multiprocessing
from os import environ

PORT = int(environ.get('PORT', 5050))
DEBUG = bool(environ.get('DEBUG', False))

GAPIKEY = str(environ.get('GAPIKEY', ''))

# gunicorn
bind = f':{PORT}'
if DEBUG:
    workers = 1
    threads = 1
    reload = True
else:
    workers = multiprocessing.cpu_count() * 2 + 1
    threads = multiprocessing.cpu_count() * 2
