# Travel globe boundaries

`travel-boundaries.geojson` combines Natural Earth's public-domain 1:50m layers:

- https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_50m_admin_0_boundary_lines_land.geojson
- https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_50m_admin_1_states_provinces_lines.geojson

Downloaded November 13, 2026. Geometry is unchanged except for rounding coordinates
to three decimal places. Unused source properties are removed. `kind` distinguishes
country borders from state/province borders, and `country` preserves the latter's
ADM0_A3 identifier. This scale's subdivision coverage includes USA, India, Canada,
Australia, Brazil, China, Russia, Indonesia, and South Africa. Natural Earth uses
de facto boundaries; this is an illustrative travel map, not a legal boundary map.

Data terms: https://www.naturalearthdata.com/about/terms-of-use/
