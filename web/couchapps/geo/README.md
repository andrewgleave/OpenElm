# Helper Functions for GeoCouch

This is a [CouchApp](http://couchapp.org/page/index) providing spatial functions and a set of helper scripts for GeoCouch. You can find the CouchApp in the `couchapp/` directory. For instructions on using GeoCouch, see the [GeoCouch Readme](github.com/vmx/couchdb#readme)

### Quick install (without cloning this repo)

Replicate this CouchApp from @maxogden's [public couch](http://max.couchone.com/apps/_design/geo) to your database:

    curl -X POST http://YOURCOUCH/_replicate -d '{"source":"http://max.couchone.com/apps","target":"http://YOURCOUCH/DBNAME", "doc_ids":["_design/geo"]}'

### In-depth install

If you wish to modify the functions in this repo before you use them, you can clone and push using the `couchapp` utility. Otherwise see the Quick install section above.

First you'll need to install the [CouchApp command line utility](http://couchapp.org/page/installing).

A specific document structure is used consistently within all utilities and examples, assuming that location information is provided in `doc.geometry` containing a valid GeoJSON struct. If your document structure differs, don't forget to adapt the (spatial) views.

    // add a document with a valid geometry into your database
    $ curl -X PUT http://localhost:5984/DBNAME/myfeature -d '{"type":"Feature", "color":"orange" ,"geometry":{"type":"Point","coordinates":[11.395,48.949444]}}'
    {"ok":true,"id":"myfeature","rev":"1-2eeb1e5eee6c8e7507b671aa7d5b0654"}

Once you have the couchapp utility working, <code>git clone</code> this repo and go into this folder and execute <code>couchapp init</code>. To upload these utils into your couch run <code>couchapp push http://YOURCOUCH/DATABASENAME</code>.

### [Spatial Views](https://github.com/vmx/couchdb)

#### points.js

A spatial view that additionally emits the original GeoJSON value (doc.geometry) 

Example:

	$ curl 'http://localhost:5984/yourdb/_design/geo/_spatial/points?bbox=80,88,90,90'
	{
	   "update_seq":203,
	   "rows":[
	      {
	         "id":"c0c048ad2770bb836a10f164cc08a3e5",
	         "bbox":[
	            81.0876957164146,
	            89.14168435614556,
	            81.0876957164146,
	            89.14168435614556
	         ],
	         "value":{
	            "id":"c0c048ad2770bb836a10f164cc08a3e5",
	            "geometry":{
	               "type":"Point",
	               "coordinates":[
	                  81.0876957164146,
	                  89.14168435614556
	               ]
	            }
	         }
	      }
	   ]
	}

#### pointsFull.js

A spatial view that emits both GeoJSON and the full document (as value).  

Example:

	$ curl 'http://localhost:5984/yourdb/_design/geo/_spatial/pointsFull?bbox=80,88,90,90'	
	{
	   "update_seq":203,
	   "rows":[
	      {
	         "id":"c0c048ad2770bb836a10f164cc08a3e5",
	         "bbox":[
	            81.0876957164146,
	            89.14168435614556,
	            81.0876957164146,
	            89.14168435614556
	         ],
	         "value":{
	            "_id":"c0c048ad2770bb836a10f164cc08a3e5",
	            "_rev":"1-0e087449742a73b5ce0df1415b1af3f3",
	            "geometry":{
	               "type":"Point",
	               "coordinates":[
	                  81.0876957164146,
	                  89.14168435614556
	               ]
	            }
	         }
	      }
	   ]
	}

#### pointsOnly.js

A spatial view that only emits GeoJSON and no additional value.

Example:

	$ curl 'http://localhost:5984/yourdb/_design/geo/_spatial/pointsOnly?bbox=80,88,90,90'	
	{
	   "update_seq":203,
	   "rows":[
	      {
	         "id":"c0c048ad2770bb836a10f164cc08a3e5",
	         "bbox":[
	            81.0876957164146,
	            89.14168435614556,
	            81.0876957164146,
	            89.14168435614556
	         ],
	         "value":null
	      }
	   ]
	}

#### titleSubtitle.js

This is a generic version of a design document that returns title and 
subtitle within the value key so they can be used to populate map 
callouts without sending another request to Couch.

It is meant to work with data that has title and subtitle in a 
properties object, as described here:

[http://opencivicdata.org](http://opencivicdata.org)

For example:

    {
      "category" : "aCategory",
      "properties" : {"title" : "theTitle", "subtitle" : "theSubtitle", "other": "other properties"},
      "start" : "",
      "end" : "",
      "geometry": {
             "coordinates": [
                 -122.59439,
                 45.5316951
             ],
             "type": "Point"
         }
    }

A database or document-type-specific version could inject text into the values, such as this title:

    function(doc) { 
    	emit(doc.geometry || {type: 'Point', coordinates: [0,0]}, 
    		{'title': (typeof(doc.station) == 'undefined') ? 'Unnamed' : 'Fire Station ' + doc.station, 
    		'subtitle': (typeof(doc.address) == 'undefined') ? 'Unknown' : doc.address})
    }

The above statement assumes that each document has geometry, station and address keys.

The general form below will only return documents that have geometry and properties keys.

### [Views](http://guide.couchdb.org/draft/views.html)

#### all 

A simple map function that returns all documents. It's like _all_docs, but you can use it as a regular view.

### [List Functions](http://guide.couchdb.org/draft/transforming.html)

#### csv.js

Not geo-specific (e.g. you can use it on any database in Couch). Simply takes your documents and emits a CSV object representing them. One limitation of this list is that every document is expected to have the same schema.

Example:

    $ curl http://localhost:5984/yourdb/_design/geo/_list/csv/all

    _id,_rev,hello
    0a631dc03a00e13a48f39817000003ae,1-15f65339921e497348be384867bb940f,world
    0a631dc03a00e13a48f3981700000c36,1-15f65339921e497348be384867bb940f,world
    0a631dc03a00e13a48f3981700001114,1-15f65339921e497348be384867bb940f,world

#### kml.js

This list function generates a simple KML feed

Example:

    $ curl http://localhost:5984/yourdb/_design/geo/_spatiallist/kml/points?bbox=0,0,45,45

    <?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
    <name>GeoCouch Result - KML Feed</name>      
    <Placemark>
      <name>b7f31f5062745b6ca1c1adfc0c2351a1</name>
      <Point><coordinates>-122.676375038274,45.5233877497394,0</coordinates></Point>
    </Placemark>
    </Document>
    </kml>


#### geojson.js 

This function outputs a GeoJSON FeatureCollection (compatible with OpenLayers). 
  
Example:

	$curl -X GET 'http://localhost:5984/yourdb/_design/geo/_spatiallist/geojson/points?bbox=80,88,90,90'	
	{
	   "type":"FeatureCollection",
	   "features":[
	      {
	         "type":"Feature",
	         "geometry":{
	            "type":"Point",
	            "coordinates":[
	               81.0876957164146,
	               89.14168435614556
	            ]
	         },
	         "properties":{
	            "id":"c0c048ad2770bb836a10f164cc08a3e5"
	         }
	      }
	   ]
	}

#### radius.js

This will take the centroid of the bbox parameter and a supplied radius parameter in meters and filter the rectangularly shaped bounding box result set by circular radius.

**WARNING** This only works with on points, not lines or polygons yet

Example:

	$ curl -X GET http://localhost:5984/yourdb/_design/geo/_spatiallist/radius/points?bbox=-122.67,45.52,-122.67,45.52&radius=50
	{
	   "type":"FeatureCollection",
	   "features":[
	      {
		 "type":"Feature",
		 "geometry":{
		    "coordinates":[
		       -122.676375038274,
		       45.5233877497394
		    ],
		    "type":"Point"
		 },
		 "properties":{
		    "id":"b7f31f5062745b6ca1c1adfc0c2351a1"
		 }
	      }
	   ]
	}


## Helper Scripts

In the folder `misc` you can find helpful scripts or snippets for GeoCouch.

### geocouch-filler-js

This node.js script can be handy for generating test data. It creates random documents within given value ranges. The script expects the following parameters:

 * The URI of the database to fill
 * A bounding box of the area to fill (as bbox JSON array)
 * The number of documents to generate

Example call:

	node geocouch-filler.js http://localhost:5984/yourdb [-180,-90,180,90] 1000

This will create 1000 documents with random locations spread over the whole world.


## License

Licensed under the MIT License.
