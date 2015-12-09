# -*- coding: utf-8 -*-

def googleGeo(lookUpArea = "New York City, NY"):
    # Source: https://pypi.python.org/pypi/geocoder
    import requests
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': lookUpArea}
    r = requests.get(url, params=params)
    results = r.json()['results']
    location = results[0]['geometry']['location']
    # print (location['lat'], location['lng'])
    return location['lng'], location['lat']


def getGeoArea(area = "New York City, NY"):
    cityLongitudeDelta = 2 # Assumption: Most places are vertically long
    cityLatitudeDelta  = 1 # Assumption: 2 degrees wide is fair to assume

    longitude, latitude = googleGeo(lookUpArea=area)
    # print(longitude, latitude)
    approxCoordinateString = str(int(longitude - cityLongitudeDelta)) + "," + str(int(latitude - cityLatitudeDelta)) + "," + str(int(longitude + cityLongitudeDelta)) + "," + str(int(latitude + cityLatitudeDelta))
    return approxCoordinateString # "New York City, NY" : '-74,40,-73,41'

# print getGeoArea()
