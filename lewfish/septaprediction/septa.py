"""Some tools for interacting with SEPTA data feeds."""

import requests

import matplotlib.pyplot as plt

from .gtfs import get_shape_dicts
from lewfish.gistools.geopath import GeoPath

def get_pos(route_short_name):
    """Returns list of current positions for buses on a SEPTA route"""
    
    pos_url_base = "http://www3.septa.org/hackathon/TransitView"
    pos_url = "%s/%s" % (pos_url_base, route_short_name)
    positions = requests.get(pos_url).json()
    return positions["bus"]

def test_get_pos():
    route_short_name = "47"
    positions = get_pos(route_short_name)
    print positions

def test_bus_map():
    route_short_name = "47"

    #a sample element returned by a call to get_pos
    bus_pos_data = {"lat":"39.958591","lng":"-75.151909","label":"8678","VehicleID":"8678","BlockID":"3350","Direction":"SouthBound","destination":"Whitman Plaza","Offset":"8"}

    bus_pos_data = {"lat":"39.949104","lng":"-75.152412","label":"5563","VehicleID":"5563","BlockID":"7928","Direction":"NorthBound","destination":"5th - Godrey","Offset":"8"}

    #XXX change me
    septa_fn = "sqlite:////Users/lewfish/data/septa/septa_bus.sqlite"
    route_block_to_shape, shape_to_path = get_shape_dicts(route_short_name, septa_fn)
    
    shape_id = route_block_to_shape[(route_short_name, bus_pos_data['BlockID'])]

    #route_id 13075
    #can two trips with the same block_id have different shape_ids? that would be a problem.
    
    #assert(shape_id == "163743")

    path = shape_to_path[shape_id]
    geo_path = GeoPath(path)

    bus_pos = (float(bus_pos_data['lat']), float(bus_pos_data['lng']))
    dist_to_path = geo_path.get_dist_to_path(bus_pos)

    lats, lons = zip(*geo_path.utm_path_orig)
    plt.plot(lats,lons)
    utm_bus_pos = geo_path.to_utm(bus_pos)
    plt.scatter([utm_bus_pos[0]],
                [utm_bus_pos[1]])
    plt.show()

    print dist_to_path
    #bus is within m meters of the published route
    m = 3
    assert(dist_to_path < 0.001 * m)

if __name__ == "__main__":
    #test_get_pos()
    test_bus_map()
    
        
    

