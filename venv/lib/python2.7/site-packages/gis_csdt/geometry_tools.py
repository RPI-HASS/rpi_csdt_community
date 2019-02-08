from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import Distance
from math import pow, sqrt, asin, sin, cos, radians
from geopy import Point as gpPoint
from geopy.distance import VincentyDistance

EARTH_RADIUS = Distance(km=6371)


def haversin(theta):
    return pow(sin(theta/2), 2)


def ahaversin(haversine):
    return 2 * asin(sqrt(haversine))


def haversine_distance(lat1, lon1, lat2, lon2):
    # convert to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    diff_lat = lat2-lat1
    diff_lon = lon2-lon1
    haversine = haversin(diff_lat) + cos(lat1) * cos(lat2) * haversin(diff_lon)
    assert haversine >= 0 and haversine <= 1
    # get distance from haversine
    return EARTH_RADIUS * ahaversin(haversine)


def circle_as_polygon(lat, lon, n=12, distance=Distance(km=1)):
    # this can be done all in degrees because that's what geopy uses!
    points = []
    # build points, loop around circle
    for angle in [360.*i/n for i in range(0, n)]:
        curr = VincentyDistance(kilometers=distance.km) \
               .destination(gpPoint(lat, lon), angle)
        points.append((curr.longitude, curr.latitude))
    # loop back to the first point for the n+1th point in the list
    points.append(points[0])
    return Polygon(tuple(points))
