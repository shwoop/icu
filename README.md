# ICU: I See You

Caching service for satellite images.

## Support

* google maps static image api (proprietary)

    This one is simple, it should work as is.

* arcgis (open):

    This is very janky, we can make a request and get an image back but we need to finely
    tune the translation of a centre into x-y min-max based on zoom and generally check we're
    getting back anything useful.

## Usage
Something along the lines of:
```
$ GAPIKEY=123 curl -X POST -json '{"latitude": 57.1463991, "longitude": -2.0934092}' \
    localhost:5050/api/v1/image
```
Please consult the swagger.

## THIS IS ALPHA CODE

* It current runs locally `python3.8 run.py`.
* All the docker/jenkins scripts have been nicked from a sister project.
* No tests whatsoever.
