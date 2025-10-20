# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.

import requests
import json

#vedant
def get_data():

    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?

    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "1924-01-01", 
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2024-10-20", 
            "orderby": "time-asc"}
    )


    return response.json()


def count_earthquakes(data):
    """
    Get the total number of earthquakes in the response.
    """
    return len(data['features'])


def get_magnitude(earthquake):
    """
    Retrieve the magnitude of an earthquake item.
    """
    return earthquake['properties']['mag']


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    coords = earthquake['geometry']['coordinates']
    return (coords[0], coords[1])


def get_maximum(data):
    """
    Get the magnitude and location of the strongest earthquake in the data.
    """
    all_earthquakes = data['features']

    if not all_earthquakes:
        return None, (None, None)

    strongest_earthquake = all_earthquakes[0]
    max_mag = get_magnitude(strongest_earthquake)

    for earthquake in all_earthquakes[1:]:
        current_mag = get_magnitude(earthquake)
        if current_mag > max_mag:
            max_mag = current_mag
            strongest_earthquake = earthquake

    max_loc = get_location(strongest_earthquake)
    
    return max_mag, max_loc


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)} earthquakes")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")
