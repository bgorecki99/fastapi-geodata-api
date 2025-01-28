# FastAPI GeoData API
[![CI Pipeline](https://github.com/bgorecki99/fastapi-geodata-api/actions/workflows/ci.yml/badge.svg)](https://github.com/bgorecki99/fastapi-geodata-api/actions/workflows/ci.yml)

A FastAPI application which uses GeoPandas to create endpoints that manipulate the York GeoJSON datasets ([found here](https://open-innovations.org/data/geojson.html)). The following datasets are in use:
1. [Conservation Areas](https://data.yorkopendata.org/dataset/befc8b34-a954-4527-b355-1fdfbb78e3db)
2. [Local Nature Reserves](https://data.yorkopendata.org/dataset/ad6aebcb-4d27-4d3b-ab21-3573f8dd9367)
3. [Pharmacies](https://data.yorkopendata.org/dataset/f16ee625-a2ec-402b-bfb8-216a421e2546)
4. [GP Surgeries](https://data.yorkopendata.org/dataset/5490d87f-aacf-4f4e-9607-06a33a09b78b)
5. [Dog and Litter Bins - All Incidents](https://data.yorkopendata.org/dataset/dog-and-litter-bins-all-incidents)

## Running Application
This application has been set-up with docker compose. To run the application use
```
docker compose up -d
```

## Endpoints Explained
### /nearest-gp-pharmacy?latitude={}&longitude={}
Given valid latitude and longitude values (within York to receive a non-empty response) this endpoint will return the nearest GP to your location and the nearest Pharmacy to the located GP.
![image](https://github.com/user-attachments/assets/851717ee-13e5-4dc5-b506-ff4c737bf799)

### /gp-within-radius?latitude={}&longitude={}&radius={}
Given valid latitude and longitude values (within York to receive a non-empty response) and a radius (above 0) this endpoint will return all GPs located within that radius.
![image](https://github.com/user-attachments/assets/53a588b9-7310-4efe-9226-209667e78e3d)

### /bins-in-nature-areas/
This endpoint returns the number of litter/dog bins within each Conservation Area and Local Nature Reserve in York.
![image](https://github.com/user-attachments/assets/49baa65c-73b2-401e-9fcf-b5a0b599372c)

### /upload-geojson/
This endpoint allows the user to upload valid GeoJSON files and returns a summary of the file. This includes the number of feature rows, feature column names, coordinate reference system of the file and all unique geometry types.

![image](https://github.com/user-attachments/assets/d0f23871-2670-467b-a52f-3d349329d1ab)
![image](https://github.com/user-attachments/assets/91582a40-9f70-4b6b-bedd-2b7372b82601)

