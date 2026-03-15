// 🔑 Remplace par ta clé Mapbox (gratuite)
mapboxgl.accessToken = 'TA_CLE_MAPBOX_ICI';

navigator.geolocation.getCurrentPosition(successLocation, errorLocation, {
  enableHighAccuracy: true
});

function setupMap(center) {
  const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v12',
    center: center,
    zoom: 14
  });

  const nav = new mapboxgl.NavigationControl();
  map.addControl(nav);

  new mapboxgl.Marker().setLngLat(center).addTo(map);
}

function successLocation(position) {
  setupMap([position.coords.longitude, position.coords.latitude]);
}

function errorLocation() {
  // fallback: Paris
  setupMap([2.3522, 48.8566]);
}
