var options = { enableHighAccuracy: true };
var coords;

function init() {
  initi();
}

function initi() {
  $.getJSON("/get_data", function(data) {

    var markers = [];
    var center = { lat: data[0].lat, lng: data[0].lng };

    var map = new google.maps.Map(document.getElementById('map-canvas'), {
      center: center,
      scrollwheel: true,
      zoom: 9
    });

    $.each(data, function (index, item) {
      var image = '/get_image/' + item.thumb;
      var latlng = { lat: item.lat, lng: item.lng };

      var icon = {
        url: image
      };

      var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        icon: icon,
        optimized: false
      });

      marker.lat = latlng.lat;
      marker.img = image;

      markers.push(marker);

      var photoCanvas = $('#photo-canvas')

      google.maps.event.addListener(marker, 'click', function() {
        $('#info').text(this.lat);
        $('<a/>')
          .append($('<img>').prop('src', marker.img))
          .prop('title', marker.lat)
          .appendTo(photoCanvas)
      });
    });

    var markerCluster = new MarkerClusterer(map, markers,
            {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});

    var overlay = new google.maps.OverlayView();
    overlay.draw = function () {
      this.getPanes().markerLayer.id='marker-layer';
    };
    overlay.setMap(map);
  });
}

function getCenter(markersData) {
  var lats = []
  var lngs = []

  for (i = 0; i < markersData.length; i++) {
    lats.push(markersData[i].gps_data.latitude);
    lngs.push(markersData[i].gps_data.longitude);
  }

  var minLat = Math.min.apply(Math, lats);
  var minLng = Math.min.apply(Math, lngs);
  var maxLat = Math.max.apply(Math, lats);
  var maxLng = Math.max.apply(Math, lngs);

  var lat = (maxLat + minLat) / 2;
  var lng = (maxLng + minLng) / 2;

  return new google.maps.LatLng(lat, lng);
}

function getLocation() {
  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition, onError, options);
  } else {
      alert("Geolocation is not supported by this browser.");
  }
}

function showPosition(position) {
  coords = position.coords;
  alert("Latitude: " + coords.latitude + "<br>Longitude: " + coords.longitude);
  initMap(coords.latitude, coords.longitude);
}

function onError(err) {
  alert("An error has occured: " + err.message);
}