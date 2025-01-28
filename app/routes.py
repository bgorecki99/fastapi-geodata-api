"""
All API routes are contained here.

Within this script there are various GeoPandas
applications on the York GeoJSON datasets found from
https://open-innovations.org/data/geojson.html.
"""

__author__ = "Bartosz Gorecki"
__date_created__ = "26/01/2025"
__last_updated__ = "27/01/2025"
__email__ = "bartoszgorecki01@gmail.com"
__maintainer__ = "Bartosz Gorecki"
__version__ = "1.0.0"

import json
import os
import logging
from logging.handlers import RotatingFileHandler
from fastapi import APIRouter, File, UploadFile
import geopandas as gpd
from shapely.geometry import Point
from fastapi.responses import JSONResponse, HTMLResponse

# Initialize a new router for routes
router = APIRouter()


def setup_logging():
    """
    This sets up the log file in the current directory logs.
    """
    # Ensure the logs directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs", exist_ok=True)

    # Set up the logging handler
    file_handler = RotatingFileHandler(
        "logs/dev_errors.log", maxBytes=10240, backupCount=3
    )
    file_handler.setLevel(logging.ERROR)

    # Create a logging format. TIME:LEVEL:MESSAGE:LOCATION
    log_format = (
        "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
    )
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    # Set up the logger
    logger = logging.getLogger()  # Root logger
    logger.setLevel(logging.ERROR)  # Set the global logging level
    logger.addHandler(file_handler)


setup_logging()
logger = logging.getLogger()


def load_geojson(filepath):
    """Loads geojson data into a GeoDataFrame.

    Args:
        filepath (str): the filepath of the file to be read.

    Raises:
        FileNotFoundError: Raise exception if file cannot be found.
        RuntimeError: Raise exception if file cannot be read.

    Returns:
        GeoDataFrame: the GeoDataFrame of the dataset.
    """
    # Resolve the path relative to the directory of this file (routes.py)
    base_path = os.path.dirname(
        os.path.abspath(__file__)
    )  # Get the directory of this file
    full_path = os.path.join(base_path, filepath)  # Combine with the relative file path

    if not os.path.exists(full_path):
        logger.error(f"File not found: {full_path}")
        raise FileNotFoundError(f"File not found: {full_path}")

    try:
        return gpd.read_file(full_path)
    except Exception as e:
        logger.error(f"Error loading file {full_path}: {e}")
        raise RuntimeError(f"Error loading file {full_path}: {e}")


# Read in the geojson York datasets
gp_gdf = load_geojson("../data/GP_Surgeries.geojson")
pharmacy_gdf = load_geojson("../data/Pharmacies.geojson")
bins_gdf = load_geojson("../data/Dog_Litter_bins_incidents_(all).geojson")
nature_reserves_gdf = load_geojson("../data/Local_nature_reserves.geojson")
conservation_areas_gdf = load_geojson("../data/Conservation_Areas.geojson")


def transform_to_bng(gdf, crs=27700):
    """Converts GeoDataFrame to BNG coordinate
    reference system.

    Args:
        gdf (GeoDataFrame): The GeoDataFrame to be reprojected.
        crs (int, optional): The CRS to reproject to. Defaults to "EPSG:27700".

    Returns:
        GeoDataFrame: Reprojected GeoDataFrame.
    """
    return gdf.to_crs(epsg=crs)


@router.get("/nearest-gp-pharmacy")
async def nearest_gp_pharmacy(latitude: float, longitude: float):
    """Using a lat + long value, return the nearest
    GP and then the nearest pharmacy to the GP
    using the York dataset.

    Args:
        latitude (float): the latitude of the point.
        longitude (float): the longitude of the point.

    Returns:
        JSON: a json object containing nearest GP
        and nearest pharmacy to GP information.
    """
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        logger.warning(f"Invalid latitude or longitude: {latitude}, {longitude}")
        return JSONResponse(
            status_code=400, content={"error": "Invalid latitude or longitude."}
        )

    input_point = Point(longitude, latitude)

    if gp_gdf is None or gp_gdf.empty:
        logger.error("GP GeoJSON data is not available.")
        return JSONResponse(content={"error": "GP data not available"}, status_code=500)

    if pharmacy_gdf is None or pharmacy_gdf.empty:
        logger.error("Pharmacy GeoJSON data is not available.")
        return JSONResponse(
            content={"error": "Pharmacy data not available"}, status_code=500
        )

    # Convert to BNG which uses metres (more accurate distance calculation)
    gp_gdf_bng = transform_to_bng(gp_gdf)
    pharmacy_gdf_bng = transform_to_bng(pharmacy_gdf)

    # Convert point provided to same crs
    input_point = gpd.GeoSeries([input_point], crs="EPSG:4326")
    input_point = input_point.to_crs(epsg=27700)

    # Calculate the distances from input point to each GP point in GDF
    gp_gdf_bng["distance"] = gp_gdf_bng.geometry.distance(input_point.iloc[0])

    # Find the row (GP) with the minimum distance to the input point
    nearest_gp = gp_gdf_bng.loc[gp_gdf_bng["distance"].idxmin()]

    # Store the point of the nearest GP
    nearest_gp_point = gpd.GeoSeries(
        [Point(nearest_gp["geometry"].x, nearest_gp["geometry"].y)]
    )

    # Calculate the distances from nearest GP to each pharmacy point in GDF
    pharmacy_gdf_bng["distance"] = pharmacy_gdf_bng.geometry.distance(
        nearest_gp_point.iloc[0]
    )

    # Find the row (pharmacy) which is closest to the nearest GP
    nearest_pharmacy_to_gp = pharmacy_gdf_bng.loc[pharmacy_gdf_bng["distance"].idxmin()]

    # Construct the json response for nearest GP and nearest pharmacy to GP
    json_response = {
        "nearest_gp": {
            "name": nearest_gp["Address_1"],
            "address": {
                "address1": nearest_gp["Address_1"],
                "address2": nearest_gp["Address_2"],
                "town": nearest_gp["Town"],
                "postcode": nearest_gp["Postcode"],
            },
            "opening_hours": {
                "mondayToFriday": nearest_gp["opening_ho"],
                "saturday": nearest_gp["Saturday"],
                "sunday": nearest_gp["Sunday"],
            },
            "distance_meters": nearest_gp["distance"],
        },
        "nearest_pharmacy_from_gp": {
            "pharmacyName": nearest_pharmacy_to_gp["PharmacyName"],
            "address": {
                "address1": nearest_pharmacy_to_gp["PharmacyAddress1"],
                "address2": nearest_pharmacy_to_gp["PharmacyAddress2"],
                "address3": nearest_pharmacy_to_gp["PharmacyAddress3"],
                "postcode": nearest_pharmacy_to_gp["Postcode"],
            },
            "distanceInMetres": nearest_pharmacy_to_gp["distance"],
        },
    }

    return JSONResponse(content=json_response)


@router.get("/gp-within-radius")
async def gp_within_radius(latitude: float, longitude: float, radius: float):
    """Given a centre point and radius, find GPS within radius
    using York dataset.

    Args:
        latitude (float): The latitude of the centre point.
        longitude (float): The longitude of the centre point.
        radius (float): The radius (miles) to search.

    Returns:
        JSON: a json object containing all GPs
        within given radius.
    """
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        logger.warning(f"Invalid latitude or longitude: {latitude}, {longitude}")
        return JSONResponse(
            status_code=400, content={"error": "Invalid latitude or longitude."}
        )

    if radius <= 0:
        logger.warning(f"Invalid radius: {radius}")
        return JSONResponse(status_code=400, content={"error": "Invalid radius."})

    if gp_gdf is None or gp_gdf.empty:
        logger.error("GP GeoJSON data is not available.")
        return JSONResponse(content={"error": "GP data not available"}, status_code=500)

    centre_point = Point(longitude, latitude)

    # Convert to BNG which uses metres (more accurate distance calculation)
    gp_gdf_bng = transform_to_bng(gp_gdf)
    centre_point = gpd.GeoSeries([centre_point], crs="EPSG:4326")
    centre_point = centre_point.to_crs(epsg=27700)

    METRES_IN_MILE = 1609.34
    # convert miles of radius to metres
    radius_metres = radius * METRES_IN_MILE

    # Create buffer of metres provided and find gps within radius
    buffer = centre_point.buffer(radius_metres).iloc[0]
    gps_within_radius = gp_gdf_bng[gp_gdf_bng.geometry.within(buffer)]

    if gps_within_radius.empty:
        return JSONResponse(
            content={"error": "No GPs found within the specified radius"},
            status_code=404,
        )

    json_response = {"gp_data": []}

    # Iterate through GP data within the radius and build the response
    for index, row in gps_within_radius.iterrows():
        gp = {
            "address1": row["Address_1"],
            "address2": row["Address_2"],
            "town": row["Town"],
            "postcode": row["Postcode"],
            "openingHours": row["opening_ho"],
            "saturday": row["Saturday"],
            "sunday": row["Sunday"],
        }

        json_response["gp_data"].append(gp)

    return JSONResponse(content=json_response)


@router.get("/bins-in-nature-areas")
async def find_bins():
    """Counts number of bins within each nature reserve
    and conservation area within the York dataset.

    Returns:
        JSON: a json object containing all nature reserves
        and conservation areas with a bin count attached for
        each area.
    """
    if bins_gdf is None or bins_gdf.empty:
        logger.error("Dog or Litter Bin GeoJSON data is not available.")
        return JSONResponse(
            content={"error": "Dog or Litter Bin data not available"}, status_code=500
        )

    if nature_reserves_gdf is None or nature_reserves_gdf.empty:
        logger.error("Nature Reserve GeoJSON data is not available.")
        return JSONResponse(
            content={"error": "Nature Reserve data not available"}, status_code=500
        )

    if conservation_areas_gdf is None or conservation_areas_gdf.empty:
        logger.error("Conservation Area GeoJSON data is not available.")
        return JSONResponse(
            content={"error": "Conservation Area data not available"}, status_code=500
        )

    # Get number of bins (points) within each nature reserve (polygons)
    bins_in_nature_reserves = gpd.sjoin(
        bins_gdf, nature_reserves_gdf, how="inner", predicate="within"
    )
    # Get number of bins (points) within each conservation area (polygons)
    bins_in_conservation_areas = gpd.sjoin(
        bins_gdf, conservation_areas_gdf, how="inner", predicate="within"
    )

    # Get count for each nature reserve and append count column to GDF
    counts = bins_in_nature_reserves.groupby("index_right").size()
    nature_reserves_gdf["bin_count"] = (
        nature_reserves_gdf.index.map(counts).fillna(0).astype(int)
    )

    # Get count for each conservation area and append count column to GDF
    counts = bins_in_conservation_areas.groupby("index_right").size()
    conservation_areas_gdf["bin_count"] = (
        conservation_areas_gdf.index.map(counts).fillna(0).astype(int)
    )

    json_response = {"nature_reserve_bin_count": [], "conservation_area_bin_count": []}

    # Iterate through nature reserve data and build response
    # with count of bins within each nature reserve
    for index, row in nature_reserves_gdf.iterrows():
        nature_reserve = {
            "type": "Nature Reserve",
            "name": row["LV_NAME"],
            "details": row["LV_DETAILS"],
            "description": row["DESCRIPTION"],
            "binCount": row["bin_count"],
        }

        json_response["nature_reserve_bin_count"].append(nature_reserve)

    # Iterate through conservation area data and build response
    # with count of bins within each conservation area
    for index, row in conservation_areas_gdf.iterrows():
        conservation_area = {
            "type": "Conservation Area",
            "name": row["Name"],
            "binCount": row["bin_count"],
        }

        json_response["conservation_area_bin_count"].append(conservation_area)

    return JSONResponse(content=json_response)


# Serving an HTML form where users can upload a GeoJSON file
@router.get("/upload-geojson/", response_class=HTMLResponse)
async def serve_upload_form():
    """Serving an HTML form where users can upload a GeoJSON file

    Returns:
        HTMLResponse: an HTML form to upload GeoJSON data.
    """
    html_content = """
    <html>
        <body>
            <h2>Upload a GeoJSON file</h2>
            <form
                action="/upload-geojson/"
                method="post"
                enctype="multipart/form-data"
            >
                <input
                    type="file"
                    name="file"
                    accept=".geojson" required
                >
                <input
                    type="submit"
                    value="Upload"
                >
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.post("/upload-geojson/")
async def upload_geojson(file: UploadFile = File(...)):
    """Reads GeoJSON file and returns a summary of its contents.

    Args:
        file (UploadFile, optional): The uploaded GeoJSON file.
                                     Defaults to File(...).

    Raises:
        ValueError: Thrown if file provided is not GeoJSON.
        ValueError: Thrown if GeoJSON file does not contain features data.

    Returns:
        JSON: A JSON object with a summary of the file including
        number of rows, columns, coordinate reference system and
        geometry types.
    """
    try:
        if not file.filename.endswith(".geojson"):
            logger.warning(f"Uploaded file is not of type GeoJSON: {file.content_type}")
            raise ValueError("Uploaded file must be a valid GeoJSON file.")

        # Read the uploaded file content
        file_content = await file.read()

        MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB
        if len(file_content) > MAX_UPLOAD_SIZE:
            logger.warning(
                f"File too large: {file.filename} " f"(size: {len(file_content)} bytes)"
            )
            return JSONResponse(
                status_code=400, content={"error": "File is too large."}
            )

        # Load the content as a GeoJSON object
        geojson_data = json.loads(file_content)

        # Validate GeoJSON file to ensure it contains feature data
        if "features" not in geojson_data:
            logger.warning(
                "Uploaded GeoJSON file does not contain features: " f"{file.filename}"
            )
            raise ValueError("Uploaded file is not a valid GeoJSON file.")

        columns = set()

        # For each feature in GeoJSON file add all the keys (property names)
        # from the feature's properties
        for feature in geojson_data["features"]:
            columns.update(feature["properties"].keys())

        summary = {
            "rows": len(geojson_data["features"]),  # Number of rows in GeoJSON
            "columns": list(columns),  # Unique property names (columns)
            "crs": geojson_data.get("crs", "N/A"),  # CRS (if exists)
            "geometry_types": list(
                {feature["geometry"]["type"] for feature in geojson_data["features"]}
            ),  # Unique geometry types
        }

        # Return the GeoJSON data as a JSON response
        return JSONResponse(content=summary)
    except ValueError as ve:
        logger.exception(f"Unexpected error: {str(ve)}")
        return JSONResponse(status_code=400, content={"error": str(ve)})
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})
