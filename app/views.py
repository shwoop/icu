from flask import jsonify, request, send_file

from app.get_image import get_image


def image():
    data = request.get_json()
    image_hash = get_image(latitude=data['latitude'], longitude=data['longitude'])
    resp = send_file(f'../files/{image_hash}.png', mimetype='image/png')
    resp.direct_passthrough = False
    return resp


def health():
    return jsonify({'status': 'ok'})
