// global flt object
var flt = {
    explore: {
        items: {}
    },
    rating: {}
};


flt.createBasemap = function (mapdiv) {
    flt.map = new google.maps.Map(document.getElementById(mapdiv));

    // simple map style
    var simple_style =  [
        {
            featureType: "administrative",
            elementType: "geometry",
            stylers: [
                { visibility: "off" }
            ]
        },{
            featureType: "administrative",
            elementType: "labels",
            stylers: [
                { visibility: "on" },
                { hue: "#d70000" },
                { lightness: 10 },
                { saturation: -95 }
            ]
        },{
            featureType: "landscape",
            elementType: "all",
            stylers: [
                { visibility: "off" }
            ]
        },{
            featureType: "poi",
            elementType: "geometry",
            stylers: [
                { visibility: "off" }
            ]
        },{
            featureType: "poi",
            elementType: "labels",
            stylers: [
                { visibility: "on" },
                { hue: "#d70000" },
                { lightness: 10 },
                { saturation: -95 }
            ]
        },{
            featureType: "transit",
            elementType: "all",
            stylers: [
                { visibility: "off" }
            ]
        },{
            featureType: "road",
            elementType: "geometry",
            stylers: [
                { hue: "#d70000" },
                { visibility: "simplified" },
                { lightness: 10 },
                { saturation: -95 }
            ]
        },{
            featureType: "road",
            elementType: "labels",
            stylers: [
                { visibility: "off" }
            ]
        },{
            featureType: "water",
            elementType: "geometry",
            stylers: [
                { visibility: "on" },
                { hue: "#0091ff" },
                { lightness: 30 },
                { saturation: -100 }
            ]
        },{
            featureType: "water",
            elementType: "labels",
            stylers: [
                { visibility: "off" }
            ]
        }
    ];

    var simple_options = {
        name: "Simple"
    }

    var simple = new google.maps.StyledMapType(simple_style, simple_options);


    flt.map.mapTypes.set("simple", simple);
    flt.map.setMapTypeId("simple");
    flt.map.streetViewControl = false;
    flt.map.setOptions({
        mapTypeControlOptions: {
            position: google.maps.ControlPosition.TOP_RIGHT,
            mapTypeIds: ["simple",google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.SATELLITE],
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        },
        panControl: false,
        zoomControlOptions: {
            style: google.maps.ZoomControlStyle.SMALL
        },
    });

    // map icons
    flt.icons = {
        'shadow': new google.maps.MarkerImage(flt.static_url + 'img/isicons/shadow.png',
            new google.maps.Size(51,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        // station icon
        'dot': new google.maps.MarkerImage(flt.static_url + 'img/isicons/dot.png',
            new google.maps.Size(6,6),
            new google.maps.Point(0,0),
            new google.maps.Point(3,6)
        ),
        // station icon
        'station': new google.maps.MarkerImage(flt.static_url + 'img/isicons/train.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'i': new google.maps.MarkerImage(flt.static_url + 'img/isicons/idea.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'm': new google.maps.MarkerImage(flt.static_url + 'img/isicons/text.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'n': new google.maps.MarkerImage(flt.static_url + 'img/isicons/text.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'e': new google.maps.MarkerImage(flt.static_url + 'img/isicons/photo.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'photo': new google.maps.MarkerImage(flt.static_url + 'img/isicons/photo.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'video': new google.maps.MarkerImage(flt.static_url + 'img/isicons/video.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'd': new google.maps.MarkerImage(flt.static_url + 'img/isicons/chart.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        )
    };
}

// render station markers
flt.createEnMarker = function (options) {
    var s_ll = new google.maps.LatLng(options.lat,options.lon);
    var s_marker = new google.maps.Marker({
        position: s_ll, 
        map: flt.map,
        title: options.title,
        //shadow: flt.icons['shadow'],
        icon: flt.icons['dot'],
        zIndex: 0
    });
}


// render flt
flt.createPoly = function (options) {
    var poly = new google.maps.Polygon({
        path: google.maps.geometry.encoding.decodePath(options.points),
        levels: flt.decodeLevels(options.levels),
        strokeColor: '#4F7B41',
        strokeOpacity: 0.9,
        strokeWeight: 1,
        zoomFactor: options.zoomFactor, 
        numLevels: options.numLevels,
        map: flt.map
    });
}

// requires 3rd party infobubble lib http://google-maps-utility-library-v3.googlecode.com/svn/trunk/infobubble/
flt.createInfoBubble = function (type, marker, contentstring) {
    google.maps.event.addListener(marker, 'click', function() {
        flt.infobubble[type].setContent(contentstring);
        flt.infobubble[type].open(flt.map, marker);
    });
}

flt.decodeLevels = function (encodedLevelsString) {
    var decodedLevels = [];
    for (var i = 0; i < encodedLevelsString.length; ++i) {
        var level = encodedLevelsString.charCodeAt(i) - 63;
        decodedLevels.push(level);
    }
    return decodedLevels;
}

// load shared items for explore page
flt.explore.loadItems = function () {
    // update filter options
    var filter = {
        bbox: flt.map.getBounds().toUrlValue(4),
        };
    // load data
    $.getJSON('/map/items/',
        filter,
        function(data) {
            // add new markers to map
            $.each(data, function(i,item){
                if (flt.explore.items[i] === undefined) {
                    flt.explore.items[i] = new google.maps.Marker({
                    position: new google.maps.LatLng(item.lat, item.lon), 
                        map: flt.map,
                            title: item.title,
                                shadow: flt.icons['shadow'],
                                icon: flt.icons[item.itemtype],
                                zIndex: 1
                                });
                                }
                                });
                            });
                        }
                
    






















