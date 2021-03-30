import pytest
from unittest.mock import patch

from app import get_image


@patch('app.get_image.requests')
def test_google_success(mock_requests):
    resp = get_image.google_get_image(latitude=123.02, longitude=456.1, zoom=1, size='240x120')

    assert resp == mock_requests.get.return_value.content
    mock_requests.get.assert_called_once_with(
        url='https://maps.googleapis.com/maps/api/staticmap',
        params={'center': '123.02,456.1', 'size': '240x120', 'zoom': 1, 'key': '', 'maptype': 'satellite'}
    )


@patch('app.get_image.requests')
def test_google_error(mock_requests):
    mock_requests.get.return_value.status_code = 404
    mock_requests.get.return_value.raise_for_status.side_effect = Exception

    with pytest.raises(Exception):
        get_image.google_get_image(latitude=123.02, longitude=456.1, zoom=1, size='240x120')
