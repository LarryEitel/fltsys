// global greenline object
var greenline = {
	infobubble: {
		station: new InfoBubble({minWidth: 160, maxWidth: 400, minborderWidth: 2, borderColor: '#4F7B41'}),
		activity: new InfoBubble({minWidth: 160, maxWidth: 400, minborderWidth: 2, borderColor: '#4F7B41'})
	},
	activities: {},
	explore: {
		items: {}
	},
	rating: {}
};

greenline.createBasemap = function (mapdiv) {
	
	// map
	greenline.map = new google.maps.Map(document.getElementById(mapdiv));

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
			featureType: "transit.line",
			elementType: "geometry",
			stylers: [
				{ hue: "#ff0000" },
				{ visibility: "on" },
				{ lightness: -20 }
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
	
	greenline.map.mapTypes.set("simple", simple);
	greenline.map.setMapTypeId("simple");
	greenline.map.streetViewControl = false;
	greenline.map.setOptions({
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
	greenline.icons = {
		'shadow': new google.maps.MarkerImage(greenline.static_url + 'img/isicons/shadow.png',
			new google.maps.Size(51,37),
			new google.maps.Point(0,0),
			new google.maps.Point(16,37)
		),
		// station icon
		'station': new google.maps.MarkerImage(greenline.static_url + 'img/isicons/train.png',
			new google.maps.Size(32,37),
			new google.maps.Point(0,0),
			new google.maps.Point(16,37)
		),
		'i': new google.maps.MarkerImage(greenline.static_url + 'img/isicons/idea.png',
			new google.maps.Size(32,37),
			new google.maps.Point(0,0),
			new google.maps.Point(16,37)
		),
		'm': new google.maps.MarkerImage(greenline.static_url + 'img/isicons/text.png',
			new google.maps.Size(32,37),
			new google.maps.Point(0,0),
			new google.maps.Point(16,37)
		),
		'n': new google.maps.MarkerImage(greenline.static_url + 'img/isicons/text.png',
			new google.maps.Size(32,37),
			new google.maps.Point(0,0),
			new google.maps.Point(16,37)
		),
		'e': new google.maps.MarkerImage(greenline.static_url + 'img/isicons/photo.png',
			new google.maps.Size(32,37),
			new google.maps.Point(0,0),
			new google.maps.Point(16,37)
		),
		'photo': new google.maps.MarkerImage(greenline.static_url + 'img/isicons/photo.png',
			new google.maps.Size(32,37),
			new google.maps.Point(0,0),
			new google.maps.Point(16,37)
		),
		'video': new google.maps.MarkerImage(greenline.static_url + 'img/isicons/video.png',
			new google.maps.Size(32,37),
			new google.maps.Point(0,0),
			new google.maps.Point(16,37)
		),
		'd': new google.maps.MarkerImage(greenline.static_url + 'img/isicons/chart.png',
			new google.maps.Size(32,37),
			new google.maps.Point(0,0),
			new google.maps.Point(16,37)
		)
	};
}

// render station markers
greenline.createStationMarker = function (options) {
	var s_ll = new google.maps.LatLng(options.lat,options.lon);
	var s_marker = new google.maps.Marker({
		position: s_ll, 
		map: greenline.map,
		title: options.title,
		shadow: greenline.icons['shadow'],
		icon: greenline.icons['station'],
		zIndex: 0
	});
	var s_area = new google.maps.Circle({
		map: greenline.map,
		fillColor: '#4F7B41',
		strokeColor: '#FFFFFF',
		fillOpacity: .3,
		strokeWeight: .6,
		radius: 804.67 // 804.67m = 0.5mi
	});
	s_area.bindTo('center', s_marker, 'position');
	greenline.createInfoBubble('station', s_marker, '<div class="infobubble"><span class="title">' + options.title + '</span><p>' + options.desc + '<br><a href="' + options.url + '">Explore the Station Area!</a></p></div>');
}

// render Greenline
greenline.createGreenline = function (options) {
	var line = new google.maps.Polyline({
		path: google.maps.geometry.encoding.decodePath(options.points),
		levels: greenline.decodeLevels(options.levels),
		strokeColor: '#4F7B41',
		strokeOpacity: 0.9,
		strokeWeight: 6,
		zoomFactor: options.zoomFactor, 
		numLevels: options.numLevels,
		map: greenline.map
	});
}

// requires 3rd party infobubble lib http://google-maps-utility-library-v3.googlecode.com/svn/trunk/infobubble/
greenline.createInfoBubble = function (type, marker, contentstring) {
	google.maps.event.addListener(marker, 'click', function() {
		greenline.infobubble[type].setContent(contentstring);
		greenline.infobubble[type].open(greenline.map, marker);
	});
}

// encoded polylines for google maps
greenline.decodeLevels = function (encodedLevelsString) {
	var decodedLevels = [];
	for (var i = 0; i < encodedLevelsString.length; ++i) {
		var level = encodedLevelsString.charCodeAt(i) - 63;
		decodedLevels.push(level);
	}
	return decodedLevels;
}

// load shared items for explore page
greenline.explore.loadItems = function () {
	// update filter options
	var filter = {
		bbox: greenline.map.getBounds().toUrlValue(4),
		itemtype: $("#select-itemtype option:selected").val(),
		station: $("#select-station option:selected").val(),
		theme: $("#select-theme option:selected").val()
	};
	// load data
	$.getJSON('/map/items/',
	filter,
	function(data) {
		// remove markers not matiching the filter
		$.each(greenline.explore.items, function(i,item){
			if (data[i] === undefined) { //existing item not found in current filter
				// remove marker and delete object
				greenline.explore.items[i].setMap(null);
				delete greenline.explore.items[i];
			}
		});
		// add new markers to map
		$.each(data, function(i,item){
			if (greenline.explore.items[i] === undefined) {
				greenline.explore.items[i] = new google.maps.Marker({
					position: new google.maps.LatLng(item.lat, item.lon), 
					map: greenline.map,
					title: item.title,
					shadow: greenline.icons['shadow'],
					icon: greenline.icons[item.itemtype],
					zIndex: 1
				});
				greenline.createInfoBubble('activity', greenline.explore.items[i], '<div class="infobubble"><span class="title">' + item.title + '</span><p>' + item.desc + '<br><a href="' + item.url + '">View details and discussion!</a></p></div>');
			}
		});
	});
}
