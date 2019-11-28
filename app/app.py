from logging.config import dictConfig

import connexion


def create_app():
    con_app = connexion.FlaskApp(__name__, specification_dir='../apispec/')
    flask_app = con_app.app

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    with flask_app.app_context():
        flask_app.url_map.strict_slashes = False
        con_app.add_api(
            'openapi.yml',
            validate_responses=True,
            strict_validation=True
        )

    return flask_app
