---
layout:     page
title:      My Travel Diary
permalink:  /travel/
---

> "How can I leave my mark on the world, I thought, unless I get out there first and see it?" <br>
> – Phil Knight, Shoe Dog

<span class="list-item">Here's everywhere I've wandered so far. Still plenty of pins left to drop.</span>

<div style="margin: 16px 0 8px; font-size: 85%;">
  <span style="display:inline-flex; align-items:center; margin-right:18px;"><span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#f4b942; margin-right:6px;"></span>Lived</span>
  <span style="display:inline-flex; align-items:center;"><span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#e74c3c; margin-right:6px;"></span>Visited</span>
</div>

<div id="globeViz" style="width:100%; height:600px; margin:0 auto; cursor:grab;"></div>

<div id="travel-photo-modal" style="display:none; position:fixed; inset:0; z-index:1000; background:rgba(0,0,0,0.75); align-items:center; justify-content:center; padding:24px;">
  <div style="position:relative; max-width:540px; width:100%; max-height:90vh; overflow-y:auto; background:var(--bg-secondary); border-radius:8px; padding:16px;">
    <button id="travel-photo-close" aria-label="Close" style="position:absolute; top:8px; right:12px; background:none; border:none; font-size:24px; line-height:1; cursor:pointer; color:var(--text-primary);">&times;</button>
    <div id="travel-photo-title" style="font-size:90%; font-weight:600; margin:4px 36px 12px 0; color:var(--text-primary);"></div>
    <div id="travel-photo-embed"></div>
    <div id="travel-photo-nav" style="display:flex; align-items:center; justify-content:center; gap:24px; margin-top:12px;">
      <button id="travel-photo-prev" aria-label="Previous" style="cursor:pointer; background:none; border:none; font-size:120%; color:var(--text-secondary);">&larr;</button>
      <span id="travel-photo-count" style="font-size:80%; color:var(--text-secondary);"></span>
      <button id="travel-photo-next" aria-label="Next" style="cursor:pointer; background:none; border:none; font-size:120%; color:var(--text-secondary);">&rarr;</button>
    </div>
  </div>
</div>

<script src="https://unpkg.com/globe.gl@2.46.2/dist/globe.gl.min.js"></script>
<script src="//www.instagram.com/embed.js"></script>
<script>
(function () {
  var places = [
    { lat: 37.3382, lng: -121.8863, name: "San Jose", region: "California", type: "visited" },
    { lat: 37.5483, lng: -121.9886, name: "Fremont", region: "California", type: "visited" },
    { lat: 37.5630, lng: -122.3255, name: "San Mateo", region: "California", type: "lived" },
    { lat: 37.7208, lng: -121.6527, name: "Altamont", region: "California", type: "visited", posts: [
      { shortcode: "DTPUmf8EfDH", date: "Jan 7, 2026", caption: "Altamont Pass Wind Farm, Altamont, California" }
    ] },
    { lat: 34.0522, lng: -118.2437, name: "Los Angeles", region: "California", type: "visited" },
    { lat: 33.6846, lng: -117.8265, name: "Irvine", region: "California", type: "visited" },
    { lat: 34.4208, lng: -119.6982, name: "Santa Barbara", region: "California", type: "visited" },
    { lat: 37.7749, lng: -122.4194, name: "San Francisco", region: "California", type: "visited", posts: [
      { shortcode: "DTuScvlFEn4", date: "Jan 19, 2026", caption: "Lake Tahoe, California & Nevada" }
    ] },
    { lat: 37.8970, lng: -122.5811, name: "Muir Woods", region: "California", type: "visited" },
    { lat: 36.9741, lng: -122.0308, name: "Santa Cruz", region: "California", type: "visited" },
    { lat: 36.6002, lng: -121.8947, name: "Monterey Bay", region: "California", type: "visited" },
    { lat: 38.2975, lng: -122.2869, name: "Napa", region: "California", type: "visited" },
    { lat: 37.6485, lng: -118.9721, name: "Mammoth Lakes", region: "California", type: "visited" },
    { lat: 36.9613, lng: -120.0607, name: "Madera", region: "California", type: "visited", posts: [
      { shortcode: "DceXiEqAQOo", date: "Aug 25, 2026", caption: "California Mule Deer, Mariposa Grove of Giant Sequoias, Yosemite National Park" },
      { shortcode: "DUZSPYeEhST", date: "Feb 5, 2026", caption: "Yosemite Falls, Yosemite National Park, California" },
      { shortcode: "DT7aZv_FE-d", date: "Jan 25, 2026", caption: "Madera, California" },
      { shortcode: "DTXaJi0FBk7", date: "Jan 11, 2026", caption: "Tunnel View, Yosemite National Park, California" }
    ] },
    { lat: 36.2704, lng: -121.8081, name: "Big Sur", region: "California", type: "visited", posts: [
      { shortcode: "DVVeimsFB5k", date: "Mar 1, 2026", caption: "Big Sur, California" }
    ] },
    { lat: 36.4627, lng: -116.8668, name: "Furnace Creek", region: "California", type: "visited" },
    { lat: 34.1347, lng: -116.3190, name: "Joshua Tree", region: "California", type: "visited" },
    { lat: 36.4388, lng: -118.9045, name: "Three Rivers", region: "California", type: "visited" },
    { lat: 36.4247, lng: -121.3263, name: "Soledad", region: "California", type: "visited" },
    { lat: 34.2746, lng: -119.2290, name: "Ventura", region: "California", type: "visited" },
    { lat: 47.6062, lng: -122.3321, name: "Seattle", region: "Washington", type: "lived", posts: [
      { shortcode: "DS1jcmVEWzg", date: "Dec 28, 2025", caption: "Ann Lake, North Cascades, Washington" }
    ] },
    { lat: 46.7580, lng: -122.0309, name: "Ashford", region: "Washington", type: "visited" },
    { lat: 48.1181, lng: -123.4307, name: "Port Angeles", region: "Washington", type: "visited" },
    { lat: 48.5279, lng: -121.4471, name: "Marblemount", region: "Washington", type: "visited" },
    { lat: 47.5962, lng: -120.6615, name: "Leavenworth", region: "Washington", type: "visited" },
    { lat: 40.4406, lng: -79.9959, name: "Pittsburgh", region: "Pennsylvania", type: "lived" },
    { lat: 39.9526, lng: -75.1652, name: "Philadelphia", region: "Pennsylvania", type: "visited" },
    { lat: 28.7041, lng: 77.1025, name: "Delhi", region: "India", type: "lived" },

    { lat: 36.9147, lng: -111.4558, name: "Page", region: "Arizona", type: "visited", posts: [
      { shortcode: "DUFmcZEFbZr", date: "Jan 29, 2026", caption: "Upper Antelope Canyon, Navajo Nation, Arizona" }
    ] },
    { lat: 39.7392, lng: -104.9903, name: "Denver", region: "Colorado", type: "visited" },
    { lat: 40.0150, lng: -105.2705, name: "Boulder", region: "Colorado", type: "visited" },
    { lat: 40.3772, lng: -105.5217, name: "Estes Park", region: "Colorado", type: "visited" },
    { lat: 25.7617, lng: -80.1918, name: "Miami", region: "Florida", type: "visited" },
    { lat: 33.7490, lng: -84.3880, name: "Atlanta", region: "Georgia", type: "visited" },
    { lat: 41.8781, lng: -87.6298, name: "Chicago", region: "Illinois", type: "visited" },
    { lat: 39.7684, lng: -86.1581, name: "Indianapolis", region: "Indiana", type: "visited" },
    { lat: 39.1141, lng: -94.6275, name: "Kansas City", region: "Kansas", type: "visited" },
    { lat: 44.3876, lng: -68.2039, name: "Bar Harbor", region: "Maine", type: "visited" },
    { lat: 39.2904, lng: -76.6122, name: "Baltimore", region: "Maryland", type: "visited" },
    { lat: 42.3601, lng: -71.0589, name: "Boston", region: "Massachusetts", type: "visited" },
    { lat: 42.3736, lng: -71.1097, name: "Cambridge", region: "Massachusetts", type: "visited" },
    { lat: 42.3314, lng: -83.0458, name: "Detroit", region: "Michigan", type: "visited" },
    { lat: 42.2808, lng: -83.7430, name: "Ann Arbor", region: "Michigan", type: "visited" },
    { lat: 38.6270, lng: -90.1994, name: "St. Louis", region: "Missouri", type: "visited" },
    { lat: 39.0997, lng: -94.5786, name: "Kansas City", region: "Missouri", type: "visited" },
    { lat: 36.1699, lng: -115.1398, name: "Las Vegas", region: "Nevada", type: "visited" },
    { lat: 39.5296, lng: -119.8138, name: "Reno", region: "Nevada", type: "visited" },
    { lat: 40.7178, lng: -74.0435, name: "Jersey City", region: "New Jersey", type: "visited" },
    { lat: 40.7128, lng: -74.0060, name: "New York City", region: "New York", type: "visited" },
    { lat: 42.8864, lng: -78.8784, name: "Buffalo", region: "New York", type: "visited" },
    { lat: 35.4767, lng: -83.3206, name: "Cherokee", region: "North Carolina", type: "visited" },
    { lat: 39.9612, lng: -82.9988, name: "Columbus", region: "Ohio", type: "visited" },
    { lat: 41.4993, lng: -81.6944, name: "Cleveland", region: "Ohio", type: "visited" },
    { lat: 39.5401, lng: -82.4071, name: "Logan", region: "Ohio", type: "visited" },
    { lat: 45.5152, lng: -122.6784, name: "Portland", region: "Oregon", type: "visited", posts: [
      { shortcode: "DU2WM2KkQ-q", date: "Feb 16, 2026", caption: "Portland, Oregon" }
    ] },
    { lat: 42.2249, lng: -121.7817, name: "Klamath Falls", region: "Oregon", type: "visited" },
    { lat: 41.8240, lng: -71.4128, name: "Providence", region: "Rhode Island", type: "visited" },
    { lat: 41.4901, lng: -71.3128, name: "Newport", region: "Rhode Island", type: "visited" },
    { lat: 35.7143, lng: -83.5102, name: "Gatlinburg", region: "Tennessee", type: "visited" },
    { lat: 38.5733, lng: -109.5498, name: "Moab", region: "Utah", type: "visited", posts: [
      { shortcode: "DT4gAoOkd_B", date: "Jan 23, 2026", caption: "Canyonlands National Park, Utah" },
      { shortcode: "DTj_qnFlJMP", date: "Jan 15, 2026", caption: "Arches National Park, Utah" }
    ] },
    { lat: 37.1677, lng: -113.0008, name: "Springdale", region: "Utah", type: "visited", posts: [
      { shortcode: "DcWqxMHDzq6", date: "Aug 22, 2026", caption: "Zion National Park, Utah" },
    ] },
    { lat: 38.8816, lng: -77.0910, name: "Arlington", region: "Virginia", type: "visited" },
    { lat: 38.0293, lng: -78.4767, name: "Charlottesville", region: "Virginia", type: "visited" },
    { lat: 38.9182, lng: -78.1944, name: "Front Royal", region: "Virginia", type: "visited" },
    { lat: 38.3498, lng: -81.6326, name: "Charleston", region: "West Virginia", type: "visited" },
    { lat: 38.4251, lng: -79.8164, name: "Green Bank", region: "West Virginia", type: "visited" },
    { lat: 38.9072, lng: -77.0369, name: "Washington", region: "DC", type: "visited" },
    { lat: 43.4799, lng: -110.7624, name: "Jackson", region: "Wyoming", type: "visited" },
    { lat: 44.6621, lng: -111.1041, name: "West Yellowstone", region: "Montana", type: "visited" },
    { lat: 45.2033, lng: -111.6786, name: "Cameron", region: "Montana", type: "visited" },

    { lat: 49.2827, lng: -123.1207, name: "Vancouver", region: "Canada", type: "visited" },

    { lat: 15.4909, lng: 73.8278, name: "Panaji", region: "Goa", type: "visited" },
    { lat: 28.4595, lng: 77.0266, name: "Gurugram", region: "Haryana", type: "visited" },
    { lat: 31.1048, lng: 77.1734, name: "Shimla", region: "Himachal Pradesh", type: "visited" },
    { lat: 32.2432, lng: 77.1892, name: "Manali", region: "Himachal Pradesh", type: "visited" },
    { lat: 32.0096, lng: 77.3147, name: "Kasol", region: "Himachal Pradesh", type: "visited" },
    { lat: 32.2190, lng: 76.3234, name: "Dharamshala", region: "Himachal Pradesh", type: "visited" },
    { lat: 30.9010, lng: 76.9650, name: "Kasauli", region: "Himachal Pradesh", type: "visited" },
    { lat: 32.5387, lng: 75.9710, name: "Dalhousie", region: "Himachal Pradesh", type: "visited" },
    { lat: 12.9716, lng: 77.5946, name: "Bengaluru", region: "Karnataka", type: "visited" },
    { lat: 19.8135, lng: 85.8312, name: "Puri", region: "Odisha", type: "visited" },
    { lat: 26.9124, lng: 75.7873, name: "Jaipur", region: "Rajasthan", type: "visited" },
    { lat: 27.3389, lng: 88.6065, name: "Gangtok", region: "Sikkim", type: "visited" },
    { lat: 17.3850, lng: 78.4867, name: "Hyderabad", region: "Telangana", type: "visited" },
    { lat: 30.3165, lng: 78.0322, name: "Dehradun", region: "Uttarakhand", type: "visited" },
    { lat: 30.0869, lng: 78.2676, name: "Rishikesh", region: "Uttarakhand", type: "visited" },
    { lat: 30.4598, lng: 78.0644, name: "Mussoorie", region: "Uttarakhand", type: "visited" },
    { lat: 29.3919, lng: 79.4542, name: "Nainital", region: "Uttarakhand", type: "visited" },
    { lat: 26.8467, lng: 80.9462, name: "Lucknow", region: "Uttar Pradesh", type: "visited" },
    { lat: 27.1767, lng: 78.0081, name: "Agra", region: "Uttar Pradesh", type: "visited" },
    { lat: 28.5355, lng: 77.3910, name: "Noida", region: "Uttar Pradesh", type: "visited" },
    { lat: 27.0410, lng: 88.2663, name: "Darjeeling", region: "West Bengal", type: "visited" },

    { lat: -8.3405, lng: 115.0920, name: "Bali", region: "Indonesia", type: "visited" },
    { lat: 28.2096, lng: 83.9856, name: "Pokhara", region: "Nepal", type: "visited" },
    { lat: 1.3521, lng: 103.8198, name: "Singapore", region: "Singapore", type: "visited" },
    { lat: 13.7563, lng: 100.5018, name: "Bangkok", region: "Thailand", type: "visited" },
    { lat: 7.7407, lng: 98.7784, name: "Phi Phi Island", region: "Thailand", type: "visited" },
    { lat: 7.8804, lng: 98.3923, name: "Phuket", region: "Thailand", type: "visited" },
    { lat: 25.2048, lng: 55.2708, name: "Dubai", region: "United Arab Emirates", type: "visited" },
    { lat: 48.8566, lng: 2.3522, name: "Paris", region: "France", type: "visited" },
    { lat: 49.3988, lng: 8.6724, name: "Heidelberg", region: "Germany", type: "visited" },
    { lat: 50.1109, lng: 8.6821, name: "Frankfurt", region: "Germany", type: "visited" },
    { lat: 47.3769, lng: 8.5417, name: "Zurich", region: "Switzerland", type: "visited" }
  ];

  var livedLocations = places.filter(function (place) {
    return place.type === "lived";
  });
  places = places.filter(function (place) {
    if (place.type === "lived") return true;
    return !livedLocations.some(function (livedPlace) {
      var sameLabel = livedPlace.name === place.name && livedPlace.region === place.region;
      var sameCoordinates = livedPlace.lat === place.lat && livedPlace.lng === place.lng;
      return sameLabel || sameCoordinates;
    });
  });
  places.sort(function (a, b) {
    return (a.type === "lived" ? 1 : 0) - (b.type === "lived" ? 1 : 0);
  });

  var COLORS = { lived: "#f4b942", visited: "#e74c3c" };

  var el = document.getElementById("globeViz");
  var hoveredPoint = null;
  var referenceCameraDistance;
  var lastCameraDistance;
  var zoomScale = 1;

  function baseRadius(d) {
    return 0.3 * zoomScale;
  }

  function pointRadius(d) {
    var base = baseRadius(d);
    if (d === hoveredPoint && d.posts && d.posts.length) {
      return base * 1.7;
    }
    return base;
  }

  var globe = Globe()(el)
    .globeImageUrl("https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg")
    .bumpImageUrl("https://unpkg.com/three-globe/example/img/earth-topology.png")
    .backgroundImageUrl("https://unpkg.com/three-globe/example/img/night-sky.png")
    .backgroundColor("rgba(0,0,0,0)")
    .showAtmosphere(true)
    .atmosphereColor("#3498db")
    .atmosphereAltitude(0.18)
    .pointsData(places)
    .pointLat("lat")
    .pointLng("lng")
    .pointColor(function (d) { return COLORS[d.type]; })
    .pointAltitude(0)
    .pointRadius(pointRadius)
    .pointResolution(24)
    .pointsTransitionDuration(120)
    .pointLabel(function (d) {
      var loc = d.region && d.region !== d.name ? d.name + ", " + d.region : d.name;
      return "<div style=\"font-size:12px; padding:2px 4px;\">" + loc + "</div>";
    })
    .width(el.clientWidth)
    .height(600);

  globe.pointOfView({ lat: 39.8283, lng: -98.5795, altitude: 1.8 }, 0);

  // Keep markers the same apparent size as the camera zooms. Point radii are
  // specified in globe-space units, so they must shrink as the camera gets
  // closer and grow as it moves away.
  referenceCameraDistance = globe.camera().position.length();
  lastCameraDistance = referenceCameraDistance;
  function updatePointScale() {
    var cameraDistance = globe.camera().position.length();
    if (Math.abs(cameraDistance - lastCameraDistance) / referenceCameraDistance < 0.001) return;
    lastCameraDistance = cameraDistance;
    zoomScale = cameraDistance ? cameraDistance / referenceCameraDistance : 1;
    globe.pointRadius(pointRadius);
  }

  globe.controls().autoRotate = true;
  globe.controls().autoRotateSpeed = 0.4;
  globe.controls().enableZoom = true;
  globe.controls().addEventListener("change", updatePointScale);

  el.addEventListener("pointerdown", function () {
    globe.controls().autoRotate = false;
    el.style.cursor = "grabbing";
  });
  el.addEventListener("pointerup", function () {
    el.style.cursor = "grab";
  });

  globe.onPointHover(function (point) {
    el.style.cursor = point && point.posts && point.posts.length ? "pointer" : "grab";
    if (point !== hoveredPoint) {
      hoveredPoint = point;
      globe.pointRadius(pointRadius);
    }
  });

  window.addEventListener("resize", function () {
    globe.width(el.clientWidth);
  });

  // --- Photo modal ---
  var modal = document.getElementById("travel-photo-modal");
  var embedEl = document.getElementById("travel-photo-embed");
  var titleEl = document.getElementById("travel-photo-title");
  var countEl = document.getElementById("travel-photo-count");
  var prevBtn = document.getElementById("travel-photo-prev");
  var nextBtn = document.getElementById("travel-photo-next");
  var closeBtn = document.getElementById("travel-photo-close");

  var currentPosts = [];
  var currentIndex = 0;

  function renderPost() {
    var post = currentPosts[currentIndex];
    titleEl.textContent = post.caption + " · " + post.date;
    countEl.textContent = (currentIndex + 1) + " / " + currentPosts.length;
    prevBtn.style.visibility = currentIndex > 0 ? "visible" : "hidden";
    nextBtn.style.visibility = currentIndex < currentPosts.length - 1 ? "visible" : "hidden";
    var permalink = "https://www.instagram.com/p/" + post.shortcode + "/";
    embedEl.innerHTML =
      '<div class="ig-embed-wrap" style="position:relative;">' +
      '<blockquote class="instagram-media" data-instgrm-permalink="' + permalink + '" data-instgrm-version="14" style="margin:0; width:100%;"></blockquote>' +
      '<div class="ig-embed-overlay" style="position:absolute; inset:0; z-index:2; cursor:pointer;" title="View on Instagram"></div>' +
      '</div>';
    var overlay = embedEl.querySelector(".ig-embed-overlay");
    overlay.addEventListener("click", function () {
      window.open(permalink, "_blank", "noopener");
    });

    if (window.instgrm && window.instgrm.Embeds) {
      window.instgrm.Embeds.process();
    }
  }

  function openModal(posts) {
    currentPosts = posts;
    currentIndex = 0;
    modal.style.display = "flex";
    renderPost();
  }

  function closeModal() {
    modal.style.display = "none";
    embedEl.innerHTML = "";
  }

  globe.onPointClick(function (point) {
    if (point && point.posts && point.posts.length) {
      openModal(point.posts);
    }
  });

  prevBtn.addEventListener("click", function () {
    if (currentIndex > 0) {
      currentIndex -= 1;
      renderPost();
    }
  });
  nextBtn.addEventListener("click", function () {
    if (currentIndex < currentPosts.length - 1) {
      currentIndex += 1;
      renderPost();
    }
  });
  closeBtn.addEventListener("click", closeModal);
  modal.addEventListener("click", function (e) {
    if (e.target === modal) closeModal();
  });
  document.addEventListener("keydown", function (e) {
    if (modal.style.display !== "flex") return;
    if (e.key === "Escape") closeModal();
    if (e.key === "ArrowLeft" && currentIndex > 0) { currentIndex -= 1; renderPost(); }
    if (e.key === "ArrowRight" && currentIndex < currentPosts.length - 1) { currentIndex += 1; renderPost(); }
  });
})();
</script>

<span class="list-item"><a href="/100_things/">List of things I want to do in my lifetime</a></span>
