/**
 * This function outputs a GeoJSON FeatureCollection (compatible with
 * OpenLayers). The geometry is stored in the geometry property, all other
 * properties in the properties property.
 * 
 * @author Volker Mische
 */
function(head, req) {
    var row, out, sep = '\n';

    // Send the same Content-Type as CouchDB would
    if (req.headers.Accept.indexOf('application/json')!=-1)
      start({"headers":{"Content-Type" : "application/json"}});
    else
      start({"headers":{"Content-Type" : "text/plain"}});

    if ('callback' in req.query) send(req.query['callback'] + "(");

    send('{"type": "FeatureCollection", "features":[');
    while (row = getRow()) {
        out = '{"type": "Feature", "geometry": ' + JSON.stringify(row.value.geometry);
        delete row.value.geometry;
        out += ', "properties": ' + JSON.stringify(row.value) + '}';

        send(sep + out);
        sep = ',\n';
    }
    send("]}");
    if ('callback' in req.query) send(")");
    
};
