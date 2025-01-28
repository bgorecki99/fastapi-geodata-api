"""
The FastAPI main app. Contains the routes
created in routes.py.
"""
__author__ = "Bartosz Gorecki"
__date_created__ = "26/01/2025"
__last_updated__ = "26/01/2025"
__email__ = "bartoszgorecki01@gmail.com"
__maintainer__ = "Bartosz Gorecki"
__version__ = "1.0.0"

from fastapi import FastAPI
from app import routes

app = FastAPI(title="Geospatial Data Processing API for York Data")

app.include_router(routes.router)


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}
