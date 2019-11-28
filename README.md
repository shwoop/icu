# Satellite Image Service

ICU: I see you

Caching service for satellite images.

Currently only supports google's static image api (proprietary) but we should
add support for ARCGIS (open).

## Usage
Something along the lines of:
```
$ curl -X POST -json '{"latitude": 57.1463991, "longitude": -2.0934092}' \
    localhost:5050/api/v1/image
```
Please consult the swagger.

## THIS IS ALPHA CODE

* It current runs locally `python3.8 run.py`.
* All the docker/jenkins scripts have been nicked from a sister project.
* No tests whatsoever.
