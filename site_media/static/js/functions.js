/**
 * The MarkerClusterer object.
 * @type {MarkerCluster}
 */
var mc = null;

/**
 * The Map object.
 * @type {google.maps.Map}
 */
var map = null;

/**
 * The MarkerManager object.
 * @type {MarkerManager}
 */
var mgr = null;

/**
 * The KmlLayer object.
 * @type {google.maps.KmlLayer}
 */
var kmlLayer = null;

/**
 * The FusionTablesLayer object.
 * @type {google.maps.FusionTablesLayer}
 */
var fusionLayer = null;

/**
 * KML layer display/hide flag.
 * @type {boolean}
 */
var showKmlLayer = false;

/**
 * Fusion Tables layer display/hide flag.
 * @type {boolean}
 */
var showFusionLayer = false;

/**
 * Fusion Tables layer heatmap flag.
 * @type {boolean}
 */
var showFusionLayerHeatmap = false;

/**
 * Marker Clusterer display/hide flag.
 * @type {boolean}
 */
var showMarketClusterer = false;

/**
 * Marker Manager display/hide flag.
 * @type {boolean}
 */
var showMarketManager = false;


/**
 * Toggles heatmap use on Fusion Tables layer.
 */
function toggleFusionHeatmap() {
  if (fusionLayer) {
    showFusionLayerHeatmap = !showFusionLayerHeatmap;
    fusionLayer.set('heatmap', showFusionLayerHeatmap);
  }
}


/**
 * Toggles Fusion Tables layer visibility.
 */
function toggleFusion() {
  if (!fusionLayer) {
    fusionLayer = new google.maps.FusionTablesLayer(232506, {
      suppressInfoWindows: false
    });
    showFusionLayerHeatmap = false;
    fusionLayer.set('heatmap', showFusionLayerHeatmap);
  }
  showFusionLayer = !showFusionLayer;
  var li = document.getElementById('fusion-hm-li');
  if (showFusionLayer) {
    fusionLayer.setMap(map);
    li.style.visibility = 'visible';
  } else {
    fusionLayer.setMap(null);
    li.style.visibility = 'hidden';
  }
}


/**
 * Toggles KML layer visibility.
 */
function toggleKmlLayer() {
  if (!kmlLayer) {
    var kmlUrl = window.location.href.substring(
        0, 1 + window.location.href.lastIndexOf('/')) + 'markers.kml';
    var kmlUrl = 'http://www.noblood.org/_files/map/house_points_layer.kml';
    kmlLayer = new google.maps.KmlLayer(kmlUrl, {
      preserveViewport: true,
      suppressInfoWindows: false
    });

    var kmlUrl = 'http://www.noblood.org/_files/map/territory_boundaries.kml';
    kmlTerrBoundLayer = new google.maps.KmlLayer(kmlUrl, {
      preserveViewport: true,
      suppressInfoWindows: false
    });

    var kmlUrl = 'http://www.noblood.org/_files/map/Distrito_layer.kml';
    kmlDistrictsLayer = new google.maps.KmlLayer(kmlUrl, {
      preserveViewport: true,
      suppressInfoWindows: false
    });

    var kmlUrl = 'http://www.noblood.org/_files/map/block_layer.kml';
    kmlBlocksLayer = new google.maps.KmlLayer(kmlUrl, {
      preserveViewport: true,
      suppressInfoWindows: false
    });

  }
  showKmlLayer = !showKmlLayer;
  if (showKmlLayer) {
    //kmlDistrictsLayer.setMap(map);
    //kmlBlocksLayer.setMap(map);
    kmlTerrBoundLayer.setMap(map);
    kmlLayer.setMap(map);
  } else {
    kmlLayer.setMap(null);
  }
}

/**
 * Toggles Marker Manager visibility.
 */
function toggleMarkerManager() {
  showMarketManager = !showMarketManager;
  if (mgr) {
    if (showMarketManager) {
      mgr.addMarkers(markers.countries, 0, 5);
      mgr.addMarkers(markers.places, 6, 11);
      mgr.addMarkers(markers.locations, 12);
      mgr.refresh();
    } else {
      mgr.clearMarkers();
      mgr.refresh();
    }
  } else {
    mgr = new MarkerManager(map, {trackMarkers: true, maxZoom: 15});
    google.maps.event.addListener(mgr, 'loaded', function() {
      mgr.addMarkers(markers.countries, 0, 5);
      mgr.addMarkers(markers.places, 6, 11);
      mgr.addMarkers(markers.locations, 12);
      mgr.refresh();
    });
  }
}


/**
 * Toggles Marker Clusterer visibility.
 */
function toggleMarkerClusterer() {
  showMarketClusterer = !showMarketClusterer;
  if (showMarketClusterer) {
    if (mc) {
      mc.addMarkers(markers.locations);
      //mc.addMarkers(markers.countries);
    } else {
      mc = new MarkerClusterer(map, markers.locations, {maxZoom: 19});
      //mc = new MarkerClusterer(map, markers.countries, {maxZoom: 19});
    }
  } else {
    mc.clearMarkers();
  }
}
