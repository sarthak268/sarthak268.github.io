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
    { lat: 36.7783, lng: -119.4179, name: "California", region: "United States", type: "lived", posts: [
      { shortcode: "DceXiEqAQOo", date: "Aug 25, 2026", caption: "California Mule Deer, Mariposa Grove of Giant Sequoias, Yosemite National Park" },
      { shortcode: "DVVeimsFB5k", date: "Mar 1, 2026", caption: "Big Sur, California" },
      { shortcode: "DUZSPYeEhST", date: "Feb 5, 2026", caption: "Yosemite Falls, Yosemite National Park, California" },
      { shortcode: "DT7aZv_FE-d", date: "Jan 25, 2026", caption: "Madera, California" },
      { shortcode: "DTuScvlFEn4", date: "Jan 19, 2026", caption: "Lake Tahoe, California & Nevada" },
      { shortcode: "DTXaJi0FBk7", date: "Jan 11, 2026", caption: "Tunnel View, Yosemite National Park, California" },
      { shortcode: "DTPUmf8EfDH", date: "Jan 7, 2026", caption: "Altamont Pass Wind Farm, Altamont, California" }
    ] },
    { lat: 47.7511, lng: -120.7401, name: "Washington", region: "United States", type: "lived", posts: [
      { shortcode: "DS1jcmVEWzg", date: "Dec 28, 2025", caption: "Ann Lake, North Cascades, Washington" }
    ] },
    { lat: 41.2033, lng: -77.1945, name: "Pennsylvania", region: "United States", type: "lived" },
    { lat: 28.7041, lng: 77.1025, name: "Delhi", region: "India", type: "lived" },

    { lat: 34.0489, lng: -111.0937, name: "Arizona", region: "United States", type: "visited", posts: [
      { shortcode: "DUFmcZEFbZr", date: "Jan 29, 2026", caption: "Upper Antelope Canyon, Navajo Nation, Arizona" }
    ] },
    { lat: 39.5501, lng: -105.7821, name: "Colorado", region: "United States", type: "visited" },
    { lat: 41.6032, lng: -73.0877, name: "Connecticut", region: "United States", type: "visited" },
    { lat: 27.6648, lng: -81.5158, name: "Florida", region: "United States", type: "visited" },
    { lat: 32.1656, lng: -82.9001, name: "Georgia", region: "United States", type: "visited" },
    { lat: 40.6331, lng: -89.3985, name: "Illinois", region: "United States", type: "visited" },
    { lat: 40.2672, lng: -86.1349, name: "Indiana", region: "United States", type: "visited" },
    { lat: 39.0119, lng: -98.4842, name: "Kansas", region: "United States", type: "visited" },
    { lat: 45.2538, lng: -69.4455, name: "Maine", region: "United States", type: "visited" },
    { lat: 39.0458, lng: -76.6413, name: "Maryland", region: "United States", type: "visited" },
    { lat: 42.4072, lng: -71.3824, name: "Massachusetts", region: "United States", type: "visited" },
    { lat: 44.3148, lng: -85.6024, name: "Michigan", region: "United States", type: "visited" },
    { lat: 38.5739, lng: -92.6038, name: "Missouri", region: "United States", type: "visited" },
    { lat: 38.8026, lng: -116.4194, name: "Nevada", region: "United States", type: "visited" },
    { lat: 43.1939, lng: -71.5724, name: "New Hampshire", region: "United States", type: "visited" },
    { lat: 40.0583, lng: -74.4057, name: "New Jersey", region: "United States", type: "visited" },
    { lat: 43.2994, lng: -74.2179, name: "New York", region: "United States", type: "visited" },
    { lat: 35.7596, lng: -79.0193, name: "North Carolina", region: "United States", type: "visited" },
    { lat: 40.4173, lng: -82.9071, name: "Ohio", region: "United States", type: "visited" },
    { lat: 43.8041, lng: -120.5542, name: "Oregon", region: "United States", type: "visited", posts: [
      { shortcode: "DU2WM2KkQ-q", date: "Feb 16, 2026", caption: "Portland, Oregon" }
    ] },
    { lat: 41.5801, lng: -71.4774, name: "Rhode Island", region: "United States", type: "visited" },
    { lat: 35.5175, lng: -86.5804, name: "Tennessee", region: "United States", type: "visited" },
    { lat: 39.3210, lng: -111.0937, name: "Utah", region: "United States", type: "visited", posts: [
      { shortcode: "DcWqxMHDzq6", date: "Aug 22, 2026", caption: "Zion National Park, Utah" },
      { shortcode: "DT4gAoOkd_B", date: "Jan 23, 2026", caption: "Canyonlands National Park, Utah" },
      { shortcode: "DTj_qnFlJMP", date: "Jan 15, 2026", caption: "Arches National Park, Utah" }
    ] },
    { lat: 37.4316, lng: -78.6569, name: "Virginia", region: "United States", type: "visited" },
    { lat: 38.5976, lng: -80.4549, name: "West Virginia", region: "United States", type: "visited" },

    { lat: 49.2827, lng: -123.1207, name: "Vancouver", region: "Canada", type: "visited" },

    { lat: 15.2993, lng: 74.1240, name: "Goa", region: "India", type: "visited" },
    { lat: 29.0588, lng: 76.0856, name: "Haryana", region: "India", type: "visited" },
    { lat: 31.1048, lng: 77.1734, name: "Himachal Pradesh", region: "India", type: "visited" },
    { lat: 15.3173, lng: 75.7139, name: "Karnataka", region: "India", type: "visited" },
    { lat: 20.9517, lng: 85.0985, name: "Odisha", region: "India", type: "visited" },
    { lat: 31.1471, lng: 75.3412, name: "Punjab", region: "India", type: "visited" },
    { lat: 27.0238, lng: 74.2179, name: "Rajasthan", region: "India", type: "visited" },
    { lat: 27.5330, lng: 88.5122, name: "Sikkim", region: "India", type: "visited" },
    { lat: 18.1124, lng: 79.0193, name: "Telangana", region: "India", type: "visited" },
    { lat: 30.0668, lng: 79.0193, name: "Uttarakhand", region: "India", type: "visited" },
    { lat: 26.8467, lng: 80.9462, name: "Uttar Pradesh", region: "India", type: "visited" },
    { lat: 22.9868, lng: 87.8550, name: "West Bengal", region: "India", type: "visited" },

    { lat: -8.3405, lng: 115.0920, name: "Bali", region: "Indonesia", type: "visited" },
    { lat: 28.3949, lng: 84.1240, name: "Nepal", region: "Nepal", type: "visited" },
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

  var COLORS = { lived: "#f4b942", visited: "#e74c3c" };

  var el = document.getElementById("globeViz");
  var hoveredPoint = null;

  function baseRadius(d) {
    return d.type === "lived" ? 0.9 : 0.65;
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
    .pointAltitude(0.015)
    .pointRadius(pointRadius)
    .pointResolution(24)
    .pointsTransitionDuration(120)
    .pointLabel(function (d) {
      var loc = d.region && d.region !== d.name ? d.name + ", " + d.region : d.name;
      return "<div style=\"font-size:12px; padding:2px 4px;\">" + loc + "</div>";
    })
    .width(el.clientWidth)
    .height(600);

  globe.pointOfView({ altitude: 1.8 }, 0);

  globe.controls().autoRotate = true;
  globe.controls().autoRotateSpeed = 0.4;
  globe.controls().enableZoom = true;

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
