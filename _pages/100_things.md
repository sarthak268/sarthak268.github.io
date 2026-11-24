---
layout:     page
title:      100 Things
permalink:  /100_things/
---

{% assign visited_parks = '' | split: ',' %}
{% for place in site.data.travel_places %}
  {% if place.national_parks %}{% assign visited_parks = visited_parks | concat: place.national_parks %}{% endif %}
{% endfor %}
{% assign park_count = visited_parks | uniq | size %}

{% capture goals_markup %}
<span class="list-item goal-item" id="goal-1" tabindex="-1">1. Trek the Himalayas</span><br>
<span class="list-item goal-item" id="goal-2" tabindex="-1">2. Hot air balloon in Cappadocia</span><br>
<span class="list-item goal-item" id="goal-3" tabindex="-1">3. <s>Broadway show in New York</s></span><br>
<span class="list-item goal-item" id="goal-4" tabindex="-1">4. See the Big Five on an African safari</span><br>
<span class="list-item goal-item" id="goal-5" tabindex="-1">5. Visit the Pyramids of Giza</span><br>
<span class="list-item goal-item" id="goal-6" tabindex="-1">6. Get scuba certified</span><br>
<span class="list-item goal-item" id="goal-7" tabindex="-1">7. <s>Learn skiing</s> (first runs at Summit at Snoqualmie, WA) <s>and snowboarding</s> (fell a lot at Sierra at Tahoe, CA)</span><br>
<span class="list-item goal-item" id="goal-8" tabindex="-1">8. Get a pilot's license</span><br>
<span class="list-item goal-item" id="goal-9" tabindex="-1">9. <s>Visit Eiffel Tower</s> (ICCV'23 brought me to Paris)</span><br>
<span class="list-item goal-item" id="goal-10" tabindex="-1">10. Cherry blossoms in Japan</span><br>
<span class="list-item goal-item" id="goal-11" tabindex="-1">11. Fall foliage in Vermont / Maine</span><br>
<span class="list-item goal-item" id="goal-12" tabindex="-1">12. Visit the North Pole</span><br>
<span class="list-item goal-item" id="goal-13" tabindex="-1">13. Visit the South Pole</span><br>
<span class="list-item goal-item" id="goal-14" tabindex="-1">14. Stay in a tree house</span><br>
<span class="list-item goal-item" id="goal-15" tabindex="-1">15. <s>Watch Aurora with someone I love</s> (went for red rocks, got northern lights — Arches National Park)</span><br>
<span class="list-item goal-item" id="goal-16" tabindex="-1">16. Experience zero gravity</span><br>
<span class="list-item goal-item" id="goal-17" tabindex="-1">17. Attend a football game in Europe</span><br>
<span class="list-item goal-item" id="goal-18" tabindex="-1">18. <s>Solo backpacking in another country</s> (wandered through Heidelberg, Germany)</span><br>
<span class="list-item goal-item" id="goal-19" tabindex="-1">19. <s>Foreign internship</s> (summer in Singapore during undergrad)</span><br>
<span class="list-item goal-item" id="goal-20" tabindex="-1">20. Attend a Coldplay concert</span><br>
<span class="list-item goal-item" id="goal-21" tabindex="-1">21. Hike Amazon rainforest</span><br>
<span class="list-item goal-item" id="goal-22" tabindex="-1">22. Skii in Switzerland</span><br>
<span class="list-item goal-item" id="goal-23" tabindex="-1">23. Hike Grand Canyon</span><br>
<span class="list-item goal-item" id="goal-24" tabindex="-1">24. Sky diving</span><br>
<span class="list-item goal-item" id="goal-25" tabindex="-1">25. <s>Bungee Jumping</s> (160m drop in Pokhara, Nepal)</span><br>
<span class="list-item goal-item" id="goal-26" tabindex="-1">26. Write a biography</span><br>
<span class="list-item goal-item" id="goal-27" tabindex="-1">27. <s>Publish in a top-tier conference</s> (ECCV'20, virtual but still counts)</span><br>
<span class="list-item goal-item" id="goal-28" tabindex="-1">28. Omakase in Tokyo</span><br>
<span class="list-item goal-item" id="goal-29" tabindex="-1">29. Authentic pizza in Naples</span><br>
<span class="list-item goal-item" id="goal-30" tabindex="-1">30. Oktoberfest in Munich</span><br>
<span class="list-item goal-item" id="goal-31" tabindex="-1">31. Watch a show at Sydney Opera House</span><br>
<span class="list-item goal-item" id="goal-32" tabindex="-1">32. Learn to play an instrument</span><br>
<span class="list-item goal-item" id="goal-33" tabindex="-1">33. Read 1000 books</span><br>
<span class="list-item goal-item" id="goal-34" tabindex="-1">34. Visit all continents (3 / 10)</span><br>
<span class="list-item goal-item" id="goal-35" tabindex="-1">35. Cruise on the Nile</span><br>
<span class="list-item goal-item" id="goal-36" tabindex="-1">36. <s>Route 66 East to West Coast</s> (Pittsburgh to San Francisco, 8 days on the road)</span><br>
<span class="list-item goal-item" id="goal-37" tabindex="-1">37. Visit all US states</span><br>
<span class="list-item goal-item" id="goal-38" tabindex="-1">38. Visit all Indian states</span><br>
<span class="list-item goal-item" id="goal-39" tabindex="-1">39. Dine in the sky on Burj Khalifa</span><br>
<span class="list-item goal-item" id="goal-40" tabindex="-1">40. Cave kayaking</span><br>
<span class="list-item goal-item" id="goal-41" tabindex="-1">41. Hike Machu Picchu</span><br>
<span class="list-item goal-item" id="goal-42" tabindex="-1">42. Climb Mount Fuji</span><br>
<span class="list-item goal-item" id="goal-43" tabindex="-1">43. Paragliding</span><br>
<span class="list-item goal-item" id="goal-44" tabindex="-1">44. Buy a Tesla (a dumb childhood dream)</span><br>
<span class="list-item goal-item" id="goal-45" tabindex="-1">45. Walk the Great Wall of China</span><br>
<span class="list-item goal-item" id="goal-46" tabindex="-1">46. <s>Sunset at Taj Mahal</s></span><br>
<span class="list-item goal-item" id="goal-47" tabindex="-1">47. Attend a traditional tea ceremony</span><br>
<span class="list-item goal-item" id="goal-48" tabindex="-1">48. <s>Watch magic in Vegas</s> (David Copperfield — some of us never stopped believing in magic)</span><br>
<span class="list-item goal-item" id="goal-49" tabindex="-1">49. Stay in an overwater bungalow</span><br>
<span class="list-item goal-item" id="goal-50" tabindex="-1">50. Go dog sledding in Lapland </span><br>
<span class="list-item goal-item" id="goal-51" tabindex="-1">51. <s>Go whale watching</s> (spotted humpbacks at Channel Islands NP, CA)</span><br>
<span class="list-item goal-item" id="goal-52" tabindex="-1">52. Party at Rio carnival</span><br>
<span class="list-item goal-item" id="goal-53" tabindex="-1">53. Float in the Dead Sea</span><br>
<span class="list-item goal-item" id="goal-54" tabindex="-1">54. Swim in the Great Barrier Reef</span><br>
<span class="list-item goal-item" id="goal-55" tabindex="-1">55. <s>Attend a rave</s> (Hocus Pocus, Miami — now I get it)</span><br>
<span class="list-item goal-item" id="goal-56" tabindex="-1">56. Give a TED talk</span><br>
<span class="list-item goal-item" id="goal-57" tabindex="-1">57. <s>Desert safari in Dubai</s></span><br>
<span class="list-item goal-item" id="goal-58" tabindex="-1">58. Explore the caves in Vietnam</span><br>
<span class="list-item goal-item" id="goal-59" tabindex="-1">59. Visit Banff National Park</span><br>
<span class="list-item goal-item" id="goal-60" tabindex="-1">60. Guest lecture at a university</span><br>
<span class="list-item goal-item" id="goal-61" tabindex="-1">61. {% if park_count >= 20 %}<s>Visit 20 national parks in the US</s> (turns out 20 was just the beginning){% else %}Visit 20 national parks in the US ({{ park_count }} / 20){% endif %}</span><br>
<span class="list-item goal-item" id="goal-62" tabindex="-1">62. Go on a solo hike</span><br>
<span class="list-item goal-item" id="goal-63" tabindex="-1">63. Go shark cage diving</span><br>
<span class="list-item goal-item" id="goal-64" tabindex="-1">64. <s>Wine at Napa Valley</s> (Castello di Amorosa — turns out I'm a wine person now)</span><br>
<span class="list-item goal-item" id="goal-65" tabindex="-1">65. Visit 10+ ski resorts (3 / 10)</span><br>
<span class="list-item goal-item" id="goal-66" tabindex="-1">66. <s>Visit a tulip farm</s> (endless colors at Roozengaarde, WA)</span><br>
<span class="list-item goal-item" id="goal-67" tabindex="-1">67. Tour the Colosseum</span><br>
<span class="list-item goal-item" id="goal-68" tabindex="-1">68. <s>Tour the Louvre museum</s></span><br>
<span class="list-item goal-item" id="goal-69" tabindex="-1">69. Michelin star date</span><br>
<span class="list-item goal-item" id="goal-70" tabindex="-1">70. Psychedlic or mind expanding retreats</span><br>
<span class="list-item goal-item" id="goal-71" tabindex="-1">71. Try sandboarding</span><br>
<span class="list-item goal-item" id="goal-72" tabindex="-1">72. Sleep on the beach under the stars</span><br>
<span class="list-item goal-item" id="goal-73" tabindex="-1">73. Author a patent</span><br>
<span class="list-item goal-item" id="goal-74" tabindex="-1">74. Camp under the stars in a desert</span><br>
<span class="list-item goal-item" id="goal-75" tabindex="-1">75. See a comet with the naked eye</span><br>
<span class="list-item goal-item" id="goal-76" tabindex="-1">76. <s>Watch a meteor shower</s> (Geminids on a freezing night near Pittsburgh)</span><br>
<span class="list-item goal-item" id="goal-77" tabindex="-1">77. Run a marathon</span><br>
<span class="list-item goal-item" id="goal-78" tabindex="-1">78. Watch a rocket launch in person</span><br>
<span class="list-item goal-item" id="goal-79" tabindex="-1">79. Stargazing in Hawaii</span><br>
<span class="list-item goal-item" id="goal-80" tabindex="-1">80. Watch a football game in Spain</span><br>
<span class="list-item goal-item" id="goal-81" tabindex="-1">81. Get featured in a news channel or newspaper</span><br>
<span class="list-item goal-item" id="goal-82" tabindex="-1">82. <s>Have a centibillionaire come see your work</s> (Jeff Bezos — can't say more)</span><br>
<span class="list-item goal-item" id="goal-83" tabindex="-1">83. See Earth from space</span><br>
<span class="list-item goal-item" id="goal-84" tabindex="-1">84. Northern Lights in Alaska</span><br>
<span class="list-item goal-item" id="goal-85" tabindex="-1">85. Meet Elon Musk</span><br>
<span class="list-item goal-item" id="goal-86" tabindex="-1">86. Meet Demis Hassabis</span><br>
<span class="list-item goal-item" id="goal-87" tabindex="-1">87. Party in Ibiza</span><br>
<span class="list-item goal-item" id="goal-88" tabindex="-1">88. Watch a volcano in Guatemala</span><br>
<span class="list-item">89. </span><br>
<span class="list-item">90. </span><br>
<span class="list-item">91. </span><br>
<span class="list-item">92. </span><br>
<span class="list-item">93. </span><br>
<span class="list-item">94. </span><br>
<span class="list-item">95. </span><br>
<span class="list-item">96. </span><br>
<span class="list-item">97. </span><br>
<span class="list-item">98. </span><br>
<span class="list-item">99. </span><br>
<span class="list-item">100. </span><br>
{% endcapture %}
{% assign goals = goals_markup | split: 'class="list-item goal-item"' %}
{% assign goal_count = goals.size | minus: 1 %}
{% assign completed_count = 0 %}
{% for goal in goals offset:1 %}
  {% assign goal_content = goal | split: '</span>' | first %}
  {% if goal_content contains '<s>' %}{% assign completed_count = completed_count | plus: 1 %}{% endif %}
{% endfor %}
{% assign completion_percent = completed_count | times: 100.0 | divided_by: goal_count | round %}

<section class="things-progress" aria-label="100 Things completion chart">
  <div class="things-progress-summary">
    <p class="things-progress-count"><span class="things-progress-number">{{ completed_count }}</span><span class="things-progress-total">/ {{ goal_count }}</span><span class="things-progress-caption">goals completed</span></p>
    <span class="things-progress-percent">{{ completion_percent }}%</span>
  </div>
  <p class="things-grid-hint">One square, one experience. A little more green with every adventure.</p>
  <div class="things-grid" aria-label="Goal completion: {{ completed_count }} completed, {{ goal_count | minus: completed_count }} still to do, {{ 100 | minus: goal_count }} yet to dream up">
    {% for goal in goals offset:1 %}
      {% assign goal_content = goal | split: '</span>' | first %}
      {% assign goal_label = goal_content | prepend: '<span ' | strip_html | strip %}
      {% assign goal_status = 'Still to do' %}
      {% if goal_content contains '<s>' %}{% assign goal_status = 'Completed' %}{% endif %}
      <a class="things-cell{% if goal_status == 'Completed' %} is-complete{% endif %}" href="#goal-{{ forloop.index }}" title="{{ goal_label | escape }} — {{ goal_status }}" aria-label="{{ goal_label | escape }} — {{ goal_status }}"></a>
    {% endfor %}
    {% assign next_goal = goal_count | plus: 1 %}
    {% if next_goal <= 100 %}
      {% for number in (next_goal..100) %}
      <span class="things-cell is-empty" title="{{ number }}. Yet to dream up" aria-label="{{ number }}. Yet to dream up"></span>
      {% endfor %}
    {% endif %}
  </div>
  <div class="things-grid-footer">
    <span>Choose a square to explore the list</span>
    <div class="things-grid-legend" aria-label="Chart legend">
      <span><i class="things-cell is-complete" aria-hidden="true"></i>Done</span>
      <span><i class="things-cell" aria-hidden="true"></i>To do</span>
      <span><i class="things-cell is-empty" aria-hidden="true"></i>Yet to dream up</span>
    </div>
  </div>
</section>

<span class="list-item">Inspired by <a href="https://huyenchip.com/list-100/">Chip Huyen's List 100</a>. Life's short - here's what I want to do with it.</span>

{{ goals_markup }}
