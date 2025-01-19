function initMap() {
    // Map options
    const location = { lat: 40.712776, lng: -74.005974 }; // Coordinates for New York
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: location,
    });

    // Marker
    const marker = new google.maps.Marker({
        position: location,
        map: map,
        title: "123 Unchained Ave, City, Country",
    });
}

// Ensure the initMap function is available globally
if (typeof window !== 'undefined') {
    window.initMap = initMap;
}
