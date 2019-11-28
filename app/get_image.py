import logging
from hashlib import sha256
from json import dumps
from pathlib import Path

import requests

from app.config import GAPIKEY

logger = logging.getLogger(__name__)

GAPI_MAP_URL = 'https://maps.googleapis.com/maps/api/staticmap'

FILE_PATH = Path('files')


def get_image(latitude: float, longitude: float, zoom: int = 13, size='600x400'):
    params = {
        'center': f'{latitude},{longitude}',
        'size': size,
        'zoom': zoom
    }

    request_hash = sha256(dumps(params, sort_keys=True).encode('utf8')).hexdigest()
    filename = FILE_PATH / f'{request_hash}.png'

    if filename.is_file():
        return request_hash

    image = google_get_image(params)

    with open(filename, 'wb') as f:
        f.write(image)

    return request_hash


def google_get_image(params) -> bytes:
    params.update({'key': GAPIKEY, 'maptype': 'satellite'})
    resp = requests.get(url=GAPI_MAP_URL, params=params)
    if resp.status_code != 200:
        logger.error(f'Problem: {resp.status_code} {resp.content}')
        resp.raise_for_status()
    return resp.content
