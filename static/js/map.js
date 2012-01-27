/**
 * Initializes the map and listeners.
 */
function initialize() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position){
                var latitude = position.coords.latitude;
                var longitude = position.coords.longitude;
                var coords = new google.maps.LatLng(latitude, longitude);
                var mapOptions = {
                    zoom: 15,
                    center: coords,
                    mapTypeControl: true,
                    navigationControlOptions: {
                        style: google.maps.NavigationControlStyle.SMALL
                    },
                    mapTypeId: google.maps.MapTypeId.ROADMAP
                    };
                    map = new google.maps.Map(
                        document.getElementById("map"), mapOptions
                        );
                    var marker = new google.maps.Marker({
                            position: coords,
                            map: map,
                            title: "Your current location!"
                    });
     
            }
        );
    }else {
        alert("Geolocation API is not supported in your browser.");
        var coords = new google.maps.LatLng(9.980516,-84.163063);
        var mapOptions = {
            zoom: 15,
            center: coords,
            mapTypeControl: true,
            navigationControlOptions: {
                style: google.maps.NavigationControlStyle.SMALL
            },
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(
            document.getElementById("map"), mapOptions
            );
        var marker = new google.maps.Marker({
                position: coords,
                map: map,
                title: "Your current location!"
        });
    }

}

google.maps.event.addDomListener(window, 'load', initialize);
