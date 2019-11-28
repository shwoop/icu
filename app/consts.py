from enum import Enum


GAPI_MAP_URL = 'https://maps.googleapis.com/maps/api/staticmap'
ARCGIS_URL = (
    'https://utility.arcgisonline.com/arcgis/rest/services/Utilities/PrintingTools/GPServer/'
    'Export Web Map Task/execute'
)


class SatelliteProvider(Enum):
    google = 1
    arcgis = 2
