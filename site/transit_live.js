function init() {
    var map = new OpenLayers.Map('map');
    var gphy = new OpenLayers.Layer.Google(
        "Google Physical",
        {type: google.maps.MapTypeId.TERRAIN}
    );
    map.addLayers([gphy]);

    // Google.v3 uses EPSG:900913 as projection, so we have to
    // transform our coordinates
    map.setCenter(new OpenLayers.LonLat(0, 0).transform(
        new OpenLayers.Projection("EPSG:4326"),
        map.getProjectionObject()
    ), 1);

    var date = new Date();
    $.getJSON("/regos/regos.json?" + date.getTime(), function(data) {
        var markers = new OpenLayers.Layer.Markers( "Markers" );
        var icon = new OpenLayers.Icon('marker.png', size, offset);
        map.addLayer(markers);
        for (i in data) {
            var rego = data[i];
            var username = rego[0];
            var loc = rego[1];
            var lat = rego[2];
            var lng = rego[3];
            var size = new OpenLayers.Size(21,25);
            var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
            var llat = new OpenLayers.LonLat(lng, lat).transform(
                new OpenLayers.Projection("EPSG:4326"),
                map.getProjectionObject()
            );
            markers.addMarker(new OpenLayers.Marker(llat, icon.clone()));
        }
    });

    var getLive = function() {
        var date = new Date();
        $.getJSON("/calc/2004.json?" + date.getTime(), function(data) {
            var e = $("#live");
            e.empty();
            e.append($("<p><strong>Updating live...</strong><br/>" + data['nenter'] + " entry observations, " + data['nleft'] + " leaving observations. Avg. result 1AU = " + data['result'] + "km</p>"));
        });
    }

    var liveUpdate = function()
    {
        getLive();
        setTimeout(getLive, 30 * 1000);
    }

    liveUpdate();
}

init();
