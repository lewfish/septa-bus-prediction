"""Tools for interacting with a GTFS database."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_shape_dicts(route_short_name, septa_fn):
    """Returns dicts that are useful for mapping from a route_short_name and block_id to a list of coordinates representing the route.

    Returns:
    route_block_to_shape -- (route_short_name, block_id) -> shape_id
    shape_to_path -- shape_id -> [(lat, lon), ...]
    """
    
    #modify this path to a sqlite file with
    #the gtfs data in it. 
    #to create this file, i used
    #https://github.com/jarondl/pygtfs.git
    e = create_engine(septa_fn)
    Session = sessionmaker(bind = e)
    s = Session()

    route_block_to_shape = {}
    q = "SELECT routes.route_short_name, trips.block_id, trips.shape_id \
    FROM routes INNER JOIN trips \
    ON routes.route_id == trips.route_id \
    WHERE routes.route_short_name == :rsn \
    GROUP BY trips.block_id"
    results = s.execute(q, {"rsn":route_short_name})
    
    for r in results:
        route_block_to_shape[(r.route_short_name, r.block_id)] = r.shape_id

    s_ids = set(route_block_to_shape.values())
    shape_to_path = {}
    for s_id in s_ids:
        q = "SELECT shapes.shape_pt_lat, shapes.shape_pt_lon \
        FROM shapes \
        WHERE shapes.shape_id == :s_id"

        results = s.execute(q, {'s_id':s_id})
        path = [tuple(r) for r in results]
        shape_to_path[s_id] = path
        
    s.close()

    return route_block_to_shape, shape_to_path

def test_get_shape_dicts():
    route_short_name = "47"
    #XXX change me
    septa_fn = "sqlite:////Users/lewfish/data/septa/septa_bus.sqlite"
    route_block_to_shape, shape_to_path = get_shape_dicts(route_short_name, septa_fn)
    
    for s_id, path in shape_to_path.iteritems():
        print s_id
        print path
        print
    
if __name__ == "__main__":
    test_get_shape_maps()
