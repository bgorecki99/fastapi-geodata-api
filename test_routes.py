"""
Unit testing for app/routes.py.

This checks all endpoints for both a valid
and invalid response and ensures all endpoints
are working as expected.
"""
__author__ = "Bartosz Gorecki"
__date_created__ = "27/01/2025"
__last_updated__ = "27/01/2025"
__email__ = "bartoszgorecki01@gmail.com"
__maintainer__ = "Bartosz Gorecki"
__version__ = "1.0.0"

import pytest
from io import BytesIO
import json
from fastapi.testclient import TestClient
from app.routes import router
from mock_data import (
    mock_nearest_gp_pharmacy_response,
    mock_gp_within_radius_response,
    mock_bins_in_nature_areas_response
)


@pytest.fixture
def client():
    """Setup FastAPI client for testing API endpoints.

    This fixture initialiaes a TestClient instance of the FastAPI app,
    which includes the necessary router for testing. It allows simulating
    HTTP requests and inspecting the responses in test cases.

    Returns:
        TestClient: A FastAPI TestClient to simulate requests to
        the application.
    """
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)  # Include the router
    return TestClient(app)


def test_nearest_gp_pharmacy(client):
    """Testing '/nearest-gp-pharmacy' endpoint
    with valid request.

    Args:
        client (TestClient): The FastAPI test client used to send the request.
    """
    # Call the endpoint with mock latitude and longitude
    params = {
        "latitude": 53.95308834600985,
        "longitude": -1.0627414822978332
    }
    response = client.get("/nearest-gp-pharmacy", params=params)
    print(response.json())
    # Assert the status code and response
    assert response.status_code == 200  # Assert a successful response

    expected_response = mock_nearest_gp_pharmacy_response
    actual_response = response.json()

    # Assert the returned data is as expected
    assert actual_response == expected_response


def test_gp_within_radius(client):
    """Testing '/gp-within-radius' endpoint
    with valid request.

    Args:
        client (TestClient): The FastAPI test client used to send the request.
    """
    params = {
        "latitude": 53.95308834600985,
        "longitude": -1.0627414822978332,
        "radius": 1
    }
    response = client.get("/gp-within-radius", params=params)
    assert response.status_code == 200
    assert response.json() == mock_gp_within_radius_response


def test_find_bins(client):
    """Testing '/bins-in-nature-areas'
    with valid request.

    Args:
        client (TestClient): The FastAPI test client used to send the request.
    """
    response = client.get("/bins-in-nature-areas")
    assert response.status_code == 200
    assert response.json() == mock_bins_in_nature_areas_response


def test_upload_geojson(client):
    """Testing the file upload (POST /upload-geojson/) endpoint
    with valid GeoJSON data.

    Args:
        client (TestClient): The FastAPI test client used to send the request.
    """
    # Create a mock file in GeoJSON format
    mock_file_content = json.dumps({
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-1.0627414822978332, 53.95308834600985]
            },
            "properties": {
                "name": "Test Feature"
            }
        }]
    })
    file = BytesIO(mock_file_content.encode())
    file.name = "test.geojson"

    # Make the POST request to upload the file
    response = client.post(
        "/upload-geojson/",
        files={"file": ("test.geojson", file, "application/geo+json")}
    )

    assert response.status_code == 200
    response_data = response.json()

    # Check for valid response fields
    assert "rows" in response_data
    assert "columns" in response_data
    assert "geometry_types" in response_data
    assert "crs" in response_data


def test_invalid_geojson_upload(client):
    """Testing invalid GeoJSON upload (POST /upload-geojson/)
    endpoint which should fail.

    Args:
        client (TestClient): The FastAPI test client used to send the request.
    """
    # Create a mock invalid GeoJSON file
    file = BytesIO(b"Invalid GeoJSON content")
    file.name = "invalid.geojson"

    # Try uploading the invalid file
    response = client.post(
        "/upload-geojson/",
        files={"file": ("invalid.geojson", file, "application/geo+json")}
    )

    assert response.status_code == 400
    response_data = response.json()

    # Assert that the error message is present in the response
    assert "error" in response_data


def test_invalid_coordinates(client):
    """Testing invalid latitude/longitude (edge case)
    for /nearest-gp-pharmacy/ endpoint.

    Args:
        client (TestClient): The FastAPI test client used to send the request.
    """
    # Call the endpoint with invalid coordinates
    response = client.get("/nearest-gp-pharmacy?latitude=1000&longitude=1000")

    assert response.status_code == 400
    response_data = response.json()

    assert "error" in response_data
    assert response_data["error"] == "Invalid latitude or longitude."


# Example of testing invalid radius for GP search
def test_invalid_radius(client):
    """Testing invalid radius (below 0) for GP search
    for /gp-within-radius/ endpoint.

    Args:
        client (TestClient): The FastAPI test client used to send the request.
    """
    # Call the endpoint with an invalid radius
    response = client.get(
        "/gp-within-radius?latitude=53.959&longitude=-1.2921&radius=-5"
    )

    assert response.status_code == 400
    response_data = response.json()

    assert "error" in response_data
    assert response_data["error"] == "Invalid radius."


def test_no_gps_within_radius(client):
    """Testing no data found
    for /gp-within-radius/ endpoint.

    Args:
        client (TestClient): The FastAPI test client used to send the request.
    """
    params = {
        "latitude": 54.70262759047464,
        "longitude": -1.9656533157159222,
        "radius": 1
    }
    response = client.get("/gp-within-radius", params=params)
    assert response.status_code == 404
    assert response.json() == {
        "error": "No GPs found within the specified radius"
    }
