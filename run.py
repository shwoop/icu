#!/usr/bin/env python3.8
from app.app import create_app
from app.config import DEBUG, PORT


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=PORT, debug=DEBUG)
