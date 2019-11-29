import json
import logging
from collections import defaultdict
from hashlib import sha256
from pathlib import Path

import requests

from app.config import GAPIKEY
from app.consts import ARCGIS_URL, GAPI_MAP_URL, SatelliteProvider

logger = logging.getLogger(__name__)

FILE_PATH = Path('files')


def get_image(
    latitude: float,
    longitude: float,
    zoom: int = 13,
    size: str = '600x400',
    provider: SatelliteProvider = SatelliteProvider.google
):
    params = {
        'latitide': latitude,
        'longitude': longitude,
        'size': size,
        'zoom': zoom,
        'provider': provider.name
    }

    request_hash = sha256(json.dumps(params, sort_keys=True).encode('utf8')).hexdigest()
    filename = FILE_PATH / f'{request_hash}.png'

    if filename.is_file():
        return request_hash

    image = PROVIDER_METHODS[provider](latitude=latitude, longitude=longitude, zoom=zoom, size=size)

    with open(filename, 'wb') as f:
        f.write(image)

    return request_hash


def google_get_image(latitude, longitude, zoom, size) -> bytes:
    params = {
        'center': f'{latitude},{longitude}',
        'size': size,
        'zoom': zoom,
        'key': GAPIKEY,
        'maptype': 'satellite'
    }
    resp = requests.get(url=GAPI_MAP_URL, params=params)
    if resp.status_code != 200:
        logger.error(f'Problem: {resp.status_code} {resp.content}')
        resp.raise_for_status()
    return resp.content


ARCGIS_ZOOM_LEVELS = defaultdict(lambda: 0.0225)
ARCGIS_ZOOM_LEVELS.update({
    13: 0.0225,
})


def arcgis_get_image(latitude, longitude, zoom, size) -> bytes:
    image_size = size.split('x')

    aspect_ratio = int(image_size[0]) / int(image_size[1])
    zoom_ratio = ARCGIS_ZOOM_LEVELS[zoom]
    ymin = latitude - zoom_ratio
    ymax = latitude + zoom_ratio
    xmin = longitude - (zoom_ratio * aspect_ratio)
    xmax = longitude + (zoom_ratio * aspect_ratio)

    web_map = {
        'mapOptions': {
            'extent': {
                'xmin': xmin,
                'ymin': ymin,
                'xmax': xmax,
                'ymax': ymax,
                'spatialReference': {
                    'wkid': 4326
                }
            }
        },
        'operationalLayers': [],
        'baseMap': {
            'title': 'Topographic Basemap',
            'baseMapLayers': [
                {
                    'url': 'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer'
                }
            ]
        },
        'exportOptions': {
            'outputSize': image_size,
        }
    }
    params = {
        'f': 'json',
        'Format': 'PNG32',
        'Layout_Template': 'MAP_ONLY',
        'Web_Map_as_JSON': json.dumps(web_map),
    }

    resp = requests.post(url=ARCGIS_URL, params=params)
    content = json.loads(resp.content)
    if resp.status_code != 200:
        logger.error(f'Problem: {resp.status_code} {resp.content}')
        resp.raise_for_status()
    if 'error' in content:
        logger.error(f'Error: {content}')
        raise Exception('Bad request')

    url = content['results'][0]['value']['url']

    resp = requests.get(url)
    if resp.status_code != 200:
        logger.error(f'Problem: {resp.status_code} {resp.content}')
        resp.raise_for_status()

    return resp.content


PROVIDER_METHODS = {
    SatelliteProvider.google: google_get_image,
    SatelliteProvider.arcgis: arcgis_get_image,
}
