function(keys, values, rereduce) {
    var MAX = 5;
    var vals = {};
    var lastkey = null;
    if(!rereduce) {
        for(var k in keys) {
            if(vals[keys[k][0]]) vals[keys[k][0]] += values[k];
            else vals[keys[k][0]] = values[k];
        }
        lastkey = keys[keys.length-1][0];
    }
    else {
        vals = values[0];
        for(var v = 1; v < values.length; v++) {
            for(var t in values[v]) {
                if(vals[t]) vals[t] += values[v][t];
                else vals[t] = values[v][t];
            }
        }
    }
    var top = [];
    for(var t in vals){
        top[top.length] = [t, vals[t]];
    }
    function sort_vals(a, b) {
        return b[1] - a[1];
    }
    top.sort(sort_vals);
    for(var n = MAX; n < top.length; n++) {
        if(top[n][0] != lastkey) vals[top[n][0]] = undefined;
    }
    return vals;
}