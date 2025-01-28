"""
Mock data for valid responses in test_routes.py
"""

__author__ = "Bartosz Gorecki"
__date_created__ = "27/01/2025"
__last_updated__ = "27/01/2025"
__email__ = "bartoszgorecki01@gmail.com"
__maintainer__ = "Bartosz Gorecki"
__version__ = "1.0.0"

# Mock valid response data for
# /nearest-gp-pharmacy?latitude=53.95308834600985&longitude=-1.0627414822978332
mock_nearest_gp_pharmacy_response = {
    "nearest_gp": {
        "name": "Park View Surgery",
        "address": {
            "address1": "Park View Surgery",
            "address2": "28 Millfield Ave, Hull Road",
            "town": "York",
            "postcode": "YO10 3AB",
        },
        "opening_hours": {
            "mondayToFriday": "8:30am - 6pm",
            "saturday": "Closed",
            "sunday": "Closed",
        },
        "distance_meters": 486.83660169527997,
    },
    "nearest_pharmacy_from_gp": {
        "pharmacyName": "Whitworth Chemists Ltd",
        "address": {
            "address1": "275 Melrosegate",
            "address2": "",
            "address3": "",
            "postcode": "YO10 3SN",
        },
        "distanceInMetres": 195.88062717871836,
    },
}

# Mock valid response data for
# /gp-within-radius?latitude=53.95308834600985&longitude=-1.0627414822978332&radius=1
mock_gp_within_radius_response = {
    "gp_data": [
        {
            "address1": "Unity Health, York Campus",
            "address2": "Newton Way, Heslington",
            "town": "York",
            "postcode": "YO10 5DE",
            "openingHours": "8:30am - 6pm",
            "saturday": "9am - 1pm",
            "sunday": "Closed",
        },
        {
            "address1": "Jorvik Gillygate Medical Practice",
            "address2": "Woolpack House, The Stonebow",
            "town": "York",
            "postcode": "YO1 7NP",
            "openingHours": "8am - 6pm",
            "saturday": "Closed",
            "sunday": "Closed",
        },
        {
            "address1": "Unity Health",
            "address2": "18 Wenlock Terrace",
            "town": "York",
            "postcode": "YO10 4DU",
            "openingHours": "8am - 6pm",
            "saturday": "Closed",
            "sunday": "Closed",
        },
        {
            "address1": "Clementhorpe Health Centre",
            "address2": "Cherry Street",
            "town": "York",
            "postcode": "YO23 1AP",
            "openingHours": "8:30am - 6pm",
            "saturday": "Closed",
            "sunday": "Closed",
        },
        {
            "address1": "Heworth Green Surgery",
            "address2": "45 Heworth Green, Heworth",
            "town": "York",
            "postcode": "YO31 7SX",
            "openingHours": "Mon-Thurs 8:30am - 8pm, Fri 8:30am - 6pm. Evenings (6:30pm - 8pm) open for pre-booked appointments only\n",
            "saturday": "Closed",
            "sunday": "Closed",
        },
        {
            "address1": "Park View Surgery",
            "address2": "28 Millfield Ave, Hull Road",
            "town": "York",
            "postcode": "YO10 3AB",
            "openingHours": "8:30am - 6pm",
            "saturday": "Closed",
            "sunday": "Closed",
        },
        {
            "address1": "Tang Hall Lane Surgery",
            "address2": "190 Tang Hall Lane",
            "town": "York",
            "postcode": "YO10 3RL",
            "openingHours": "8:30am - 6pm",
            "saturday": "Closed",
            "sunday": "Closed",
        },
        {
            "address1": "East Parade Medical Practice",
            "address2": "89 East Parade",
            "town": "York",
            "postcode": "YO31 7YD",
            "openingHours": "8:30am - 12:30pm, 2pm - 6pm",
            "saturday": "Closed",
            "sunday": "Closed",
        },
        {
            "address1": "Monkgate",
            "address2": "35 Monkgate",
            "town": "York",
            "postcode": "YO31 7PB",
            "openingHours": "Mon 8am - 7:30pm, Tues/Wed 7:30am - 6pm, Thurs/Fri 8am - 6pm",
            "saturday": "Closed",
            "sunday": "Closed",
        },
    ]
}

# Mock valid response data for
# /bins-in-nature-areas
mock_bins_in_nature_areas_response = {
    "nature_reserve_bin_count": [
        {
            "type": "Nature Reserve",
            "name": "St Nicholas Fields",
            "details": "St Nicholas Field, Bull Lane, Layerthorpe, York",
            "description": "St Nicholas Fields is in Tang Hall and was designated as a local nature reserve in 2004 ",
            "binCount": 3,
        },
        {
            "type": "Nature Reserve",
            "name": "Hob Moor",
            "details": "Hob Moor Nature Reserve, Hob Moor Drive, York",
            "description": "Hob Moor local nature reserve is behind Edmund Wilson Swimming Pool, Thanet Road and to the west of Tadcaster Road",
            "binCount": 8,
        },
        {
            "type": "Nature Reserve",
            "name": "Acomb Wood and Meadow",
            "details": "Acomb Wood, Acomb Wood Close, York",
            "description": "This ten-acres of mixed woodland and ancient meadow is a green oasis in the middle of a large housing estate",
            "binCount": 0,
        },
        {
            "type": "Nature Reserve",
            "name": "Clifton Backies",
            "details": "Clifton Backies Nature Reserve, Water Lane, York",
            "description": "Clifton Backies is situated between Bootham Stray and Water Lane in Clifton Without",
            "binCount": 1,
        },
        {
            "type": "Nature Reserve",
            "name": "Hassacarr",
            "details": "Hassacarr Nature Reserve, Hassacarr Lane, York, YO19 5PB",
            "description": "Hassacarr Nature Reserve is owned by Dunnington Parish Council and managed by Dunnington Conservation Group",
            "binCount": 0,
        },
    ],
    "conservation_area_bin_count": [
        {
            "type": "Conservation Area",
            "name": "Strensall Village Conservation Area",
            "binCount": 17,
        },
        {
            "type": "Conservation Area",
            "name": "Acomb Conservation Area",
            "binCount": 11,
        },
        {"type": "Conservation Area", "name": "Haxby Conservation Area", "binCount": 1},
        {"type": "Conservation Area", "name": "Haxby Conservation Area", "binCount": 1},
        {
            "type": "Conservation Area",
            "name": "Heslington Conservation Area",
            "binCount": 1,
        },
        {
            "type": "Conservation Area",
            "name": "Heslington Conservation Area",
            "binCount": 1,
        },
        {
            "type": "Conservation Area",
            "name": "Central Historic Core Conservation Area",
            "binCount": 124,
        },
        {
            "type": "Conservation Area",
            "name": "Clifton Conservation Area",
            "binCount": 4,
        },
        {
            "type": "Conservation Area",
            "name": "St. Paul's Square/Holgate Road Conservation Area",
            "binCount": 0,
        },
        {
            "type": "Conservation Area",
            "name": "Heworth Green/East Parade Conservation Area",
            "binCount": 4,
        },
        {"type": "Conservation Area", "name": "New Walk/Terry Avenue", "binCount": 7},
        {
            "type": "Conservation Area",
            "name": "Fulford Road Conservation Area",
            "binCount": 0,
        },
        {
            "type": "Conservation Area",
            "name": "Tadcaster Road Conservation Area",
            "binCount": 32,
        },
        {
            "type": "Conservation Area",
            "name": "The Racecourse and Terry's Factory Conservation Area",
            "binCount": 6,
        },
        {
            "type": "Conservation Area",
            "name": "Middlethorpe Conservation Area",
            "binCount": 0,
        },
        {
            "type": "Conservation Area",
            "name": "Bishopthorpe Conservation Area",
            "binCount": 5,
        },
        {
            "type": "Conservation Area",
            "name": "Copmanthorpe Conservation Area",
            "binCount": 5,
        },
        {
            "type": "Conservation Area",
            "name": "Askham Bryan Conservation Area",
            "binCount": 0,
        },
        {
            "type": "Conservation Area",
            "name": "Askham Richard Conservation Area",
            "binCount": 0,
        },
        {
            "type": "Conservation Area",
            "name": "Upper Poppleton Conservation Area",
            "binCount": 5,
        },
        {
            "type": "Conservation Area",
            "name": "Nether Poppleton Conservation Area",
            "binCount": 4,
        },
        {
            "type": "Conservation Area",
            "name": "Skelton Conservation Area",
            "binCount": 1,
        },
        {
            "type": "Conservation Area",
            "name": "Clifton (Malton Way/Shipton Road) Conservation Area",
            "binCount": 0,
        },
        {
            "type": "Conservation Area",
            "name": "New Earswick Conservation Area",
            "binCount": 2,
        },
        {
            "type": "Conservation Area",
            "name": "Huntington Conservation Area",
            "binCount": 4,
        },
        {
            "type": "Conservation Area",
            "name": "Osbaldwick Conservation Area",
            "binCount": 0,
        },
        {
            "type": "Conservation Area",
            "name": "Elvington Conservation Area",
            "binCount": 0,
        },
        {
            "type": "Conservation Area",
            "name": "Wheldrake Conservation Area",
            "binCount": 3,
        },
        {
            "type": "Conservation Area",
            "name": "Escrick Conservation Area",
            "binCount": 0,
        },
        {
            "type": "Conservation Area",
            "name": "Stockton-on-the-Forest Conservation Area",
            "binCount": 1,
        },
        {
            "type": "Conservation Area",
            "name": "Fulford Village Conservation Area",
            "binCount": 5,
        },
        {
            "type": "Conservation Area",
            "name": "Strensall Railway Buildings Conservation Area",
            "binCount": 1,
        },
        {
            "type": "Conservation Area",
            "name": "Towthorpe Village Conservation Area",
            "binCount": 0,
        },
        {
            "type": "Conservation Area",
            "name": "Dunnington Conservation Area",
            "binCount": 2,
        },
        {
            "type": "Conservation Area",
            "name": "Murton Conservation Area",
            "binCount": 2,
        },
        {
            "type": "Conservation Area",
            "name": "Nestle/Rowntree Conservation Area",
            "binCount": 0,
        },
        {"type": "Conservation Area", "name": "The Retreat", "binCount": 0},
    ],
}
