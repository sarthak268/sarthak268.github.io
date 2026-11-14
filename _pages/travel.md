---
layout:     page
title:      My Travel Diary
permalink:  /travel/
---

<link rel="stylesheet" href="{{ '/css/travel.css' | relative_url }}">

<div class="travel-intro">
  <p>Here's everywhere I've wandered so far. Still plenty of pins left to drop.</p>
  <span class="travel-eyebrow">A PERSONAL ATLAS</span>
</div>

<section class="travel-atlas" aria-label="Interactive travel globe">
  <div class="travel-toolbar">
    <div class="travel-view-switch" role="group" aria-label="Locations shown">
      <button type="button" id="travel-all" aria-pressed="true">All places <span id="travel-place-total"></span></button>
      <button type="button" id="travel-photos" aria-pressed="false">With photos <span id="travel-photo-total"></span></button>
    </div>
    <label class="travel-photo-picker">Photo journal
      <select id="travel-photo-select"><option value="">Choose a location</option></select>
    </label>
  </div>
  <div class="travel-globe-stage">
    <div id="globeViz" aria-label="Travel globe. Drag to rotate; scroll to zoom. Use the photo journal menu to open photos with a keyboard."></div>
    <div class="travel-map-tools" role="group" aria-label="Globe controls">
      <button type="button" id="travel-usa">USA</button>
      <button type="button" id="travel-india">India</button>
      <button type="button" id="travel-reset" aria-label="Reset globe view">Reset</button>
    </div>
    <span class="travel-globe-hint">Drag to explore · Scroll to zoom</span>
  </div>
  <div class="travel-map-footer">
    <div class="travel-legend" aria-label="Map legend">
      <span><i class="travel-key travel-key-lived"></i>Lived</span>
      <span><i class="travel-key travel-key-visited"></i>Visited</span>
      <span><i class="travel-key travel-key-photo"><svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 6h4l2-3h4l2 3h4v14H4z"/><circle cx="12" cy="12" r="3.5"/></svg></i>Photos to open</span>
      <span><i class="travel-key travel-key-plain"></i>No photos yet</span>
    </div>
    <span id="travel-map-status" role="status">Camera pins open the photo journal</span>
  </div>
</section>

<div id="travel-photo-modal" role="dialog" aria-modal="true" aria-labelledby="travel-photo-title" style="display:none; position:fixed; inset:0; z-index:1000; background:rgba(0,0,0,0.75); align-items:center; justify-content:center; padding:24px;">
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
  var places = {{ site.data.travel_places | jsonify }};
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

  function hasPhotos(place) { return !!(place.posts && place.posts.length); }
  function locationName(place) {
    return place.region && place.region !== place.name ? place.name + ", " + place.region : place.name;
  }
  var photoPlaces = places.filter(hasPhotos);
  document.getElementById("travel-place-total").textContent = places.length;
  document.getElementById("travel-photo-total").textContent = photoPlaces.length;

  var COLORS = { lived: "#f4b942", visited: "#e74c3c" };

  var el = document.getElementById("globeViz");
  var hoveredPoint = null;
  var referenceCameraDistance;
  var lastCameraDistance;
  var zoomScale = 1;

  function baseRadius(d) {
    return (hasPhotos(d) ? 0.3 : 0.36) * zoomScale;
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
    .backgroundColor("rgba(0,0,0,0)")
    .showAtmosphere(true)
    .atmosphereColor("#3498db")
    .atmosphereAltitude(0.13)
    .pointsData(places)
    .pointLat("lat")
    .pointLng("lng")
    .pointColor(function (d) { return COLORS[d.type]; })
    .pointAltitude(0.002)
    .pointRadius(pointRadius)
    .pointResolution(24)
    .pointsTransitionDuration(120)
    .pointLabel(function (d) {
      var loc = d.region && d.region !== d.name ? d.name + ", " + d.region : d.name;
      var tooltip = document.createElement("div");
      tooltip.style.cssText = "font-size:12px; padding:2px 4px;";
      tooltip.textContent = loc;
      var availability = document.createElement("div");
      availability.style.cssText = "font-size:11px; margin-top:4px; opacity:.8";
      availability.textContent = hasPhotos(d) ? d.posts.length + " photo posts · Click to open" : "No photos yet";
      tooltip.appendChild(availability);
      (d.national_parks || []).forEach(function (name) {
        var park = document.createElement("div");
        park.style.cssText = "font-size:11px; margin-top:4px;";
        park.textContent = name + " National Park";
        tooltip.appendChild(park);
      });
      return tooltip.outerHTML;
    })
    .width(el.clientWidth)
    .height(el.clientHeight)
    .pathPoints("coordinates")
    .pathPointLat(function (p) { return p[1]; })
    .pathPointLng(function (p) { return p[0]; })
    .pathPointAlt(0.001)
    .pathStroke(null)
    .pathColor(function (d) { return d.kind === "countries" ? "rgba(230,240,255,0.7)" : "rgba(200,220,245,0.34)"; })
    .pathTransitionDuration(0)
    .pointerEventsFilter(function (obj, data) { return !data || !data.boundary; })
    .htmlElementsData(photoPlaces)
    .htmlLat("lat")
    .htmlLng("lng")
    .htmlAltitude(0.008)
    .htmlElement(function (place) {
      var marker = document.createElement("button");
      marker.type = "button";
      marker.className = "travel-photo-pin";
      marker.style.setProperty("--pin-color", COLORS[place.type]);
      marker.title = locationName(place) + " · " + place.posts.length + " photo posts";
      marker.setAttribute("aria-label", "Open photos from " + locationName(place));
      marker.innerHTML = '<svg viewBox="0 0 24 24" width="9" height="9" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 6h4l2-3h4l2 3h4v14H4z"/><circle cx="12" cy="12" r="3.5"/></svg>';
      marker.addEventListener("click", function (event) {
        event.stopPropagation();
        globe.controls().autoRotate = false;
        openModal(place.posts);
      });
      return marker;
    });

  fetch({{ '/assets/maps/travel-boundaries.geojson' | relative_url | jsonify }})
    .then(function (response) {
      if (!response.ok) throw new Error("Boundary data unavailable");
      return response.json();
    })
    .then(function (data) {
      var paths = [];
      data.features.forEach(function (feature) {
        var lines = feature.geometry.type === "MultiLineString" ? feature.geometry.coordinates : [feature.geometry.coordinates];
        lines.forEach(function (coordinates) {
          paths.push({ coordinates: coordinates, kind: feature.properties.kind, boundary: true });
        });
      });
      globe.pathsData(paths);
    })
    .catch(function () {
      document.getElementById("travel-map-status").textContent = "Borders unavailable · Photo pins still work";
    });

  function showPlaces(photosOnly) {
    globe.pointsData(photosOnly ? photoPlaces : places);
    document.getElementById("travel-all").setAttribute("aria-pressed", String(!photosOnly));
    document.getElementById("travel-photos").setAttribute("aria-pressed", String(photosOnly));
  }
  document.getElementById("travel-all").addEventListener("click", function () { showPlaces(false); });
  document.getElementById("travel-photos").addEventListener("click", function () { showPlaces(true); });
  function focusGlobe(lat, lng, altitude) {
    globe.controls().autoRotate = false;
    globe.pointOfView({ lat: lat, lng: lng, altitude: altitude }, 900);
  }
  document.getElementById("travel-usa").addEventListener("click", function () { focusGlobe(39, -98, 1.2); });
  document.getElementById("travel-india").addEventListener("click", function () { focusGlobe(22, 79, 1.1); });
  document.getElementById("travel-reset").addEventListener("click", function () {
    showPlaces(false);
    focusGlobe(39.8283, -98.5795, 1.8);
  });
  var photoSelect = document.getElementById("travel-photo-select");
  photoPlaces.sort(function (a, b) { return a.name.localeCompare(b.name); });
  photoPlaces.forEach(function (place, index) {
    var option = document.createElement("option");
    option.value = index;
    option.textContent = locationName(place) + " (" + place.posts.length + ")";
    photoSelect.appendChild(option);
  });
  photoSelect.addEventListener("change", function () {
    if (photoSelect.value === "") return;
    var place = photoPlaces[Number(photoSelect.value)];
    focusGlobe(place.lat, place.lng, 1.2);
    openModal(place.posts);
    photoSelect.value = "";
  });

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

  globe.controls().autoRotate = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  globe.controls().autoRotateSpeed = 0.4;
  globe.controls().enableZoom = true;
  globe.controls().addEventListener("change", updatePointScale);

  el.addEventListener("pointerdown", function () {
    globe.controls().autoRotate = false;
  });

  globe.onPointHover(function (point) {
    if (point !== hoveredPoint) {
      hoveredPoint = point;
      globe.pointRadius(pointRadius);
    }
  });

  window.addEventListener("resize", function () {
    globe.width(el.clientWidth).height(el.clientHeight);
  });

  // --- Photo modal ---
  var modal = document.getElementById("travel-photo-modal");
  var embedEl = document.getElementById("travel-photo-embed");
  var titleEl = document.getElementById("travel-photo-title");
  var countEl = document.getElementById("travel-photo-count");
  var prevBtn = document.getElementById("travel-photo-prev");
  var nextBtn = document.getElementById("travel-photo-next");
  var closeBtn = document.getElementById("travel-photo-close");

  var returnFocus;
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
      '</div><a class="travel-instagram-link" href="' + permalink + '" target="_blank" rel="noopener">View post on Instagram ↗</a>';
    var overlay = embedEl.querySelector(".ig-embed-overlay");
    overlay.addEventListener("click", function () {
      window.open(permalink, "_blank", "noopener");
    });

    if (window.instgrm && window.instgrm.Embeds) {
      window.instgrm.Embeds.process();
    }
  }

  function openModal(posts) {
    returnFocus = document.activeElement;
    globe.controls().autoRotate = false;
    currentPosts = posts;
    currentIndex = 0;
    modal.style.display = "flex";
    renderPost();
    closeBtn.focus();
  }

  function closeModal() {
    modal.style.display = "none";
    embedEl.innerHTML = "";
    if (returnFocus) returnFocus.focus();
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
    if (e.key === "Tab") {
      var buttons = Array.from(modal.querySelectorAll("button, a[href]")).filter(function (item) { return item.style.visibility !== "hidden"; });
      var first = buttons[0], last = buttons[buttons.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
    if (e.key === "Escape") closeModal();
    if (e.key === "ArrowLeft" && currentIndex > 0) { currentIndex -= 1; renderPost(); }
    if (e.key === "ArrowRight" && currentIndex < currentPosts.length - 1) { currentIndex += 1; renderPost(); }
  });
})();
</script>

{% assign visited_parks = '' | split: ',' %}
{% for place in site.data.travel_places %}
  {% if place.national_parks %}{% assign visited_parks = visited_parks | concat: place.national_parks %}{% endif %}
{% endfor %}
{% assign visited_parks = visited_parks | uniq | sort %}

<section class="travel-stats" aria-labelledby="travel-stats-title">
  <header class="travel-stats-heading">
    <span class="section-index">STILL EXPLORING</span>
    <h2 id="travel-stats-title">The journey so far</h2>
  </header>
  <div class="travel-stats-grid">
    {% for stat in site.data.travel_stats %}
    {% assign stat_count = stat.count %}
    {% if stat.source == 'national_parks' %}{% assign stat_count = visited_parks | size %}{% endif %}
    {% if stat.total %}{% assign percent = stat_count | times: 100.0 | divided_by: stat.total %}{% endif %}
    <div class="travel-stat">
      <h3>{{ stat.title }}</h3>
      <p class="travel-stat-number">{{ stat_count }}{% if stat.total %} <span>/ {{ stat.total }}</span>{% endif %}</p>
      <div class="travel-stat-detail"><span>{{ stat.unit }}</span>{% if stat.total %}<span>{{ percent | round }}%</span>{% endif %}</div>
      {% if stat.total %}
      <div class="travel-stat-track" role="progressbar" aria-label="{{ stat.label }}" aria-valuemin="0" aria-valuemax="{{ stat.total }}" aria-valuenow="{{ stat_count }}" aria-valuetext="{{ stat_count }} of {{ stat.total }} {{ stat.unit }} visited">
        <div class="travel-stat-fill" style="width: {{ percent }}%"></div>
      </div>
      {% endif %}
    </div>
    {% endfor %}
  </div>
  <a class="text-link" href="/100_things/">More to explore: my list of 100 things <span aria-hidden="true">→</span></a>
</section>

<blockquote class="travel-quote">
  <p>“How can I leave my mark on the world, I thought, unless I get out there first and see it?”</p>
  <cite>Phil Knight, <em>Shoe Dog</em></cite>
</blockquote>
