(function () {
  function initProjectMapPicker() {
    if (typeof L === "undefined") return;

    var mapEl = document.getElementById("project-map-picker");
    var latEl = document.getElementById("id_latitude");
    var lngEl = document.getElementById("id_longitude");
    var locationEl = document.getElementById("id_location_name");
    var cityEl = document.getElementById("id_location_city");
    var postcodeEl = document.getElementById("id_location_postcode");
    var searchEl = document.getElementById("project-map-search");
    var searchBtn = document.getElementById("project-map-search-btn");

    if (!mapEl || !latEl || !lngEl) return;

    var startLat = parseFloat(latEl.value);
    var startLng = parseFloat(lngEl.value);

    if (Number.isNaN(startLat)) startLat = 20.5937;
    if (Number.isNaN(startLng)) startLng = 78.9629;

    var map = L.map(mapEl).setView([startLat, startLng], latEl.value && lngEl.value ? 14 : 5);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);

    var marker = L.marker([startLat, startLng], { draggable: true }).addTo(map);

    function setCoordinates(lat, lng) {
      latEl.value = Number(lat).toFixed(6);
      lngEl.value = Number(lng).toFixed(6);
    }

    setCoordinates(startLat, startLng);

    marker.on("dragend", function (e) {
      var point = e.target.getLatLng();
      setCoordinates(point.lat, point.lng);
      reverseGeocode(point.lat, point.lng);
    });

    map.on("click", function (e) {
      marker.setLatLng(e.latlng);
      setCoordinates(e.latlng.lat, e.latlng.lng);
      reverseGeocode(e.latlng.lat, e.latlng.lng);
    });

    function fillAddressFields(address, displayName) {
      if (!address) return;
      if (postcodeEl && !postcodeEl.value && address.postcode) {
        postcodeEl.value = address.postcode;
      }
      if (cityEl && !cityEl.value) {
        cityEl.value = address.city || address.town || address.village || address.state_district || "";
      }
      if (locationEl && !locationEl.value && displayName) {
        locationEl.value = displayName;
      }
    }

    function reverseGeocode(lat, lng) {
      var url = "https://nominatim.openstreetmap.org/reverse?format=json&lat=" + encodeURIComponent(lat) + "&lon=" + encodeURIComponent(lng);
      fetch(url, {
        headers: {
          Accept: "application/json",
        },
      })
        .then(function (res) {
          return res.json();
        })
        .then(function (data) {
          if (!data) return;
          fillAddressFields(data.address || {}, data.display_name || "");
        })
        .catch(function () {});
    }

    function geocodeSearch() {
      var q = (searchEl && searchEl.value ? searchEl.value : "").trim();
      if (!q) return;

      var url = "https://nominatim.openstreetmap.org/search?format=json&limit=1&q=" + encodeURIComponent(q);

      fetch(url, {
        headers: {
          Accept: "application/json",
        },
      })
        .then(function (res) {
          return res.json();
        })
        .then(function (data) {
          if (!data || !data.length) return;

          var result = data[0];
          var lat = parseFloat(result.lat);
          var lng = parseFloat(result.lon);

          marker.setLatLng([lat, lng]);
          map.setView([lat, lng], 14);
          setCoordinates(lat, lng);
          fillAddressFields(result.address || {}, result.display_name || q);
          reverseGeocode(lat, lng);
        })
        .catch(function () {});
    }

    if (searchBtn) {
      searchBtn.addEventListener("click", geocodeSearch);
    }

    if (searchEl) {
      searchEl.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
          event.preventDefault();
          geocodeSearch();
        }
      });
    }

    setTimeout(function () {
      map.invalidateSize();
    }, 0);
  }

  document.addEventListener("DOMContentLoaded", initProjectMapPicker);
})();
