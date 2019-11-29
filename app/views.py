from flask import jsonify, request, send_file

from app.consts import SatelliteProvider
from app.get_image import get_image


def image():
    data = request.get_json()
    args = {'latitude': data['latitude'], 'longitude': data['longitude']}
    if provider := data.get('provider'):
        args['provider'] = SatelliteProvider[provider]
    if zoom := data.get('zoom'):
        args['zoom'] = zoom

    image_hash = get_image(**args)

    resp = send_file(f'../files/{image_hash}.png', mimetype='image/png')
    resp.direct_passthrough = False
    return resp


def health():
    return jsonify({'status': 'ok'})
