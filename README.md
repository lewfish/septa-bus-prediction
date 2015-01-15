septa-bus-prediction
===================

A project to learn a model of bus arrival time using time series data published by SEPTA.

Right now, I am just working on retrieving the route shape data for a bus route, and using using it to normalize the lat/lon position of a bus into route-centered coordinates (ie. between 0 and 1 from the start to the end of the route).

Install
=========
Install <a href="https://github.com/jarondl/pygtfs">pygtfs</a>. Change line 166 in pygtfs/gtfs_entities.py to be
```_validate_wheelchair = _validate_int_choice([None,0,1,2], 'wheelchair_boarding')``` to allow for null wheelchair_boarding fields. Then use the command-line gtfs2db tool to make a sqlite database with the contents of the Septa GTFS bus feed.

Install <a href="https://github.com/lewfish/gis-tools">lewfish/gis-tools</a> and make sure it's on the PYTHONPATH.

Then in this project, invoke ```pip install -r requirments.txt```

In lewfish/septaprediction/septa.py change the value of septa_fn to point to the database file created with gtfs2db.



Run
====
You can run a test by invoking ```python -m lewfish.septaprediction.septa```.

