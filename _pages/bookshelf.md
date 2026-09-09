---
layout:     page
title:      Bookshelf
permalink:  /bookshelf/
---

> "A reader lives a thousand lives before he dies... The man who never reads lives only one."
> – George R.R. Martin

<span class="list-item">Immersed in the enchanting world of words, I find solace and inspiration, my mind liberated as I embark on literary journeys.
Here lies a cherished collection (a subset) of the books that have captivated my heart and nourished my soul. My favorites are marked with <span class="shelf-fav-inline">★</span>.</span><br>

<br>

<div id="shelf-root"></div>

<style>
.shelf-section { margin-bottom: 34px; }
.shelf-section-head { font-size: 105%; font-weight: 600; margin-bottom: 4px; }
.shelf-section-desc { font-size: 90%; color: var(--text-secondary); margin-bottom: 12px; }
.shelf-row-wrap { position: relative; display: flex; align-items: center; }
.shelf-row {
  display: flex;
  gap: 14px;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 4px 2px 12px;
  scrollbar-width: thin;
}
.shelf-row::-webkit-scrollbar { height: 6px; }
.shelf-row::-webkit-scrollbar-thumb { background: var(--border-medium); border-radius: 3px; }
.shelf-arrow {
  flex: none;
  background: var(--bg-secondary);
  border: 1px solid var(--border-medium);
  color: var(--text-primary);
  border-radius: 50%;
  width: 30px;
  height: 30px;
  cursor: pointer;
  font-size: 90%;
  line-height: 1;
  z-index: 2;
}
.shelf-arrow:hover { color: var(--accent-blue); border-color: var(--accent-blue); }
.shelf-arrow.left { margin-right: 6px; }
.shelf-arrow.right { margin-left: 6px; }
.book-card {
  flex: none;
  width: 108px;
  text-decoration: none;
  display: block;
}
.book-cover-frame {
  position: relative;
  width: 108px;
  height: 160px;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0,0,0,0.35);
  background: var(--bg-secondary);
  transition: transform 0.15s ease;
}
.book-card:hover .book-cover-frame { transform: translateY(-3px); box-shadow: 0 6px 14px rgba(0,0,0,0.45); }
.book-cover-frame img { width: 100%; height: 100%; object-fit: cover; display: block; }
.book-cover-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 8px;
  font-size: 78%;
  line-height: 1.3;
  color: var(--text-primary);
  background: linear-gradient(160deg, var(--bg-secondary), var(--bg-primary));
}
.book-fav-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  font-size: 80%;
  color: #f4b942;
  text-shadow: 0 1px 2px rgba(0,0,0,0.6);
}
.book-fav-ring { box-shadow: inset 0 0 0 2px #f4b942; border-radius: 4px; }
.book-card-title {
  font-size: 76%;
  color: var(--text-secondary);
  margin-top: 6px;
  line-height: 1.25;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.shelf-fav-inline { color: #f4b942; }
.shelf-toggle-bar { display: flex; justify-content: flex-end; margin-bottom: 18px; }
.shelf-toggle {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 85%;
  color: var(--text-secondary);
  cursor: pointer;
  user-select: none;
}
.shelf-toggle-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}
.shelf-toggle-track {
  position: relative;
  flex: none;
  width: 34px;
  height: 18px;
  background: var(--border-medium);
  border-radius: 999px;
  transition: background 0.2s ease;
}
.shelf-toggle-thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 14px;
  height: 14px;
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 1px 2px rgba(0,0,0,0.4);
  transition: transform 0.2s ease;
}
.shelf-toggle-input:checked + .shelf-toggle-track { background: #f4b942; }
.shelf-toggle-input:checked + .shelf-toggle-track .shelf-toggle-thumb { transform: translateX(16px); }
.shelf-toggle-input:focus-visible + .shelf-toggle-track { outline: 2px solid var(--accent-blue); outline-offset: 2px; }
.shelf-toggle-text { color: var(--text-secondary); }
.shelf-favonly .book-card { display: none; }
.shelf-favonly .book-card.is-fav { display: block; }
.shelf-favonly .shelf-section.no-fav { display: none; }
</style>

<script>
(function () {
  var SECTIONS = [
    {
      key: "science", emoji: "🔬", title: "Science & History",
      desc: "Exploring the cosmos, evolution, and the forces that shaped our world. I get endlessly lost in these — most of them I've re-read, and I'm always re-reading something from this shelf.",
      books: [
        { slug: "sapiens", title: "Sapiens", author: "Yuval Noah Harari", cover: 8634250 },
        { slug: "theory_of_everything", title: "The Theory of Everything", author: "Stephen W. Hawking", cover: 942436 },
        { slug: "21_lessons", title: "21 Lessons for the 21st Century", author: "Yuval Noah Harari", cover: 10108277 },
        { slug: "fabric_of_reality", title: "The Fabric of Reality", author: "David Deutsch", cover: 452204, fav: true },
        { slug: "pale_blue_dot", title: "Pale Blue Dot", author: "Carl Sagan", cover: 14417175 },
        { slug: "cosmos", title: "Cosmos", author: "Carl Sagan", cover: 8283901 },
        { slug: "beginning_of_infinity", title: "The Beginning of Infinity", author: "David Deutsch", cover: 8622269, fav: true },
        { slug: "reality_rovelli", title: "Reality is not what it seems", author: "Carlo Rovelli", cover: 10866486, fav: true },
        { slug: "red_queen", title: "The Red Queen", author: "Matt Ridley", cover: 29174 },
        { slug: "aliens", title: "The Little Book of Aliens", author: "Adam Frank", cover: 14601430 },
        { slug: "selfish_gene", title: "The Selfish Gene", author: "Richard Dawkins", cover: 133936, fav: true },
        { slug: "cycles_of_time", title: "Cycles of Time", author: "Roger Penrose", cover: 7889572 },
        { slug: "life_assembly", title: "Life As No One Knows It", author: "Sara Imari Walker", cover: 15121306, fav: true },
        { slug: "moon_shot", title: "Moon Shot", author: "Alan Shepard and Deke Slayton", cover: 11682298 },
        { slug: "space_to_grow", title: "Space to Grow", author: "Weinzierl and Rosseau", coverGoogle: "d2jwEAAAQBAJ" },
        { slug: "lords_of_cosmos", title: "Lords of the Cosmos", author: "Khemani and Chipkin", coverDirect: "https://www.lordsofcosmos.com/lordsofcosmos.png", fav: true },
        { slug: "space_time_motion", title: "Space, Time, and Motion", author: "Sean Carroll", cover: 12933717, fav: true },
        { slug: "brief_history_of_intelligence", title: "A Brief History of Intelligence", author: "Max Bennett", coverGoogle: "tymCEAAAQBAJ" }
      ]
    },
    {
      key: "mindset", emoji: "🧠", title: "Mindset & Wisdom",
      desc: "Books that rewired how I think, decide, and live. Haven't been reading too many of these lately.",
      books: [
        { slug: "naval", title: "The Almanack of Naval Ravikant", author: "Eric Jorgenson", cover: 10449931, fav: true },
        { slug: "anthology_of_balaji", title: "The Anthology of Balaji", author: "Eric Jorgenson", cover: 15178491 },
        { slug: "subtle_art", title: "The Subtle Art of Not Giving a F*ck", author: "Mark Manson", cover: 8231990 },
        { slug: "compound_effect", title: "The Compound Effect", author: "Darren Hardy", cover: 7115046 },
        { slug: "ikigai", title: "Ikigai", author: "Miralles and Garcia", cover: 11300391 },
        { slug: "courage_to_be_disliked", title: "The Courage to be Disliked", author: "Koga and Kishimi", cover: 10873626 },
        { slug: "12_rules", title: "12 Rules for Life", author: "Jordan B. Peterson", cover: 8131760 },
        { slug: "give_and_take", title: "Give and Take", author: "Adam Grant", cover: 7391212 },
        { slug: "winner_effect", title: "The Winner Effect", author: "Ian Robertson", cover: 9076261 },
        { slug: "principles", title: "Principles", author: "Ray Dalio", cover: 8315355 },
        { slug: "art_of_thinking_clearly", title: "The Art of Thinking Clearly", author: "Rolf Dobelli", cover: 8270423 }
      ]
    },
    {
      key: "bio", emoji: "📖", title: "Biographies & Memoirs",
      desc: "Lives worth studying — from athletes to astronauts to entrepreneurs. My favourite section, and I'm always looking for more recommendations.",
      books: [
        { slug: "shoe_dog", title: "Shoe Dog", author: "Phil Knight", cover: 8858487, fav: true },
        { slug: "steve_jobs", title: "Steve Jobs", author: "Walter Isaacson", cover: 12374726 },
        { slug: "cant_hurt_me", title: "Can't Hurt Me", author: "David Goggins", coverIsbn: "9781544512280" },
        { slug: "becoming", title: "Becoming", author: "Michelle Obama", cover: 8824664 },
        { slug: "born_a_crime", title: "Born A Crime", author: "Trevor Noah", cover: 8294078 },
        { slug: "limitless", title: "Limitless", author: "Radhika Gupta", coverGoogle: "iu5mEAAAQBAJ" },
        { slug: "elon_musk", title: "Elon Musk", author: "Ashlee Vance", cover: 8463846 },
        { slug: "starbucks", title: "Pour Your Heart Into It", author: "Howard Schultz", cover: 545501 },
        { slug: "when_breath_becomes_air", title: "When Breath Becomes Air", author: "Paul Kalanithi", cover: 11463139, fav: true },
        { slug: "mind_master", title: "Mind Master", author: "Viswanathan Anand", cover: 10845864 },
        { slug: "shot_at_history", title: "A Shot at History", author: "Abhinav Bindra", coverGoogle: "IlJLDQAAQBAJ" },
        { slug: "charlie", title: "Poor Charlie's Almanack", author: "Charlie Munger", cover: 8337563 },
        { slug: "no_dream_too_high", title: "No Dream Is Too High", author: "Buzz Aldrin", cover: 12803742 },
        { slug: "my_journey_kalam", title: "My Journey", author: "A.P.J Abdul Kalam", cover: 10899260 },
        { slug: "einstein", title: "Einstein", author: "Steven Gimbel", cover: 9168994 },
        { slug: "unseen", title: "Unseen", author: "Megha Vishwanath", coverGoogle: "rsCREQAAQBAJ" },
        { slug: "surely_youre_joking", title: "Surely You're Joking, Mr. Feynman!", author: "Richard P. Feynman", cover: 14766391 }
      ]
    },
    {
      key: "fiction", emoji: "✨", title: "Fiction",
      desc: "Stories that stretched my imagination beyond the real. I don't read fiction too often, but these were worth it.",
      books: [
        { slug: "alchemist", title: "The Alchemist", author: "Paulo Coelho", cover: 7414780 },
        { slug: "life_3", title: "Life 3.0", author: "Max Tegmark", cover: 10239283 },
        { slug: "three_body_problem", title: "The Three-Body Problem", author: "Cixin Liu", cover: 9157544 }
      ]
    },
    {
      key: "startups", emoji: "🚀", title: "Entrepreneurship",
      desc: "Lessons from the builders — on starting, scaling, and surviving. These inspired me on how to build, and to build something.",
      books: [
        { slug: "hard_things", title: "Hard Things about Hard Things", author: "Ben Horowitz", cover: 7279515 },
        { slug: "zero_to_one", title: "Zero to One", author: "Peter Thiel", cover: 9002334 },
        { slug: "radical_candor", title: "Radical Candor", author: "Kim Scott", cover: 11457329 },
        { slug: "five_moves_ahead", title: "Your Next Five Moves", author: "Patrick Bet-David", cover: 10961423 },
        { slug: "paul_graham", title: "Essays", author: "Paul Graham", cover: 388913 },
        { slug: "no_rules_rules", title: "No Rules Rules", author: "Hastings and Meyer", cover: 10524294 },
        { slug: "that_will_never_work", title: "That Will Never Work", author: "Marc Randolph", cover: 10663066, fav: true }
      ]
    },
    {
      key: "finance", emoji: "💰", title: "Finance & Investing",
      desc: "Understanding money, markets, and the psychology behind both.",
      books: [
        { slug: "intelligent_investor", title: "The Intelligent Investor", author: "Benjamin Graham", cover: 36434 },
        { slug: "think_and_grow_rich", title: "Think and Grow Rich", author: "Napoleon Hill", cover: 14542536 },
        { slug: "coffee_can_investing", title: "Coffee Can Investing", author: "Saurabh Mukherjee", cover: 10848634 },
        { slug: "just_keep_buying", title: "Just Keep Buying", author: "Nick Maggiulli", cover: 14561679 },
        { slug: "psychology_of_money", title: "The Psychology of Money", author: "Morgan Housel", cover: 10389354 },
        { slug: "rich_dad_poor_dad", title: "Rich Dad Poor Dad", author: "Robert T. Kiyosaki", cover: 8315603 }
      ]
    },
    {
      key: "eclectic", emoji: "🎲", title: "Eclectic Picks",
      desc: "A mix of everything else that left a mark.",
      books: [
        { slug: "think_again", title: "Think Again", author: "Adam Grant", cover: 10470266 },
        { slug: "what_i_know_for_sure", title: "What I Know For Sure", author: "Oprah Winfrey", cover: 7414838 },
        { slug: "make_your_own_luck", title: "Make Your Own Luck", author: "Miglani and Khan", coverGoogle: "tIhFzQEACAAJ" },
        { slug: "factfulness", title: "Factfulness", author: "Hans Rosling et al.", cover: 8186237 },
        { slug: "do_epic_shit", title: "Do Epic Shit", author: "Ankur Warikoo", cover: 12550538 },
        { slug: "mans_search_for_meaning", title: "Man's Search for Meaning", author: "Victor E. Frankl", cover: 8513458 },
        { slug: "rational_optimist", title: "The Rational Optimist", author: "Matt Ridley", cover: 7024445, fav: true },
        { slug: "antifragile", title: "Antifragile", author: "Nassim Taleb", cover: 9180157 },
        { slug: "stardust", title: "We Are All Stardust", author: "Stefan Klein", cover: 11327789 },
        { slug: "when_heavens_went_on_sale", title: "When the Heavens Went on Sale", author: "Ashlee Vance", cover: 13234791, fav: true },
        { slug: "moonwalking_with_einstein", title: "Moonwalking with Einstein", author: "Joshua Foer", cover: 14426425 }
      ]
    }
  ];

  function coverUrl(id) {
    return "https://covers.openlibrary.org/b/id/" + id + "-M.jpg";
  }

  function coverUrlByIsbn(isbn) {
    return "https://covers.openlibrary.org/b/isbn/" + isbn + "-M.jpg";
  }

  function coverUrlByGoogleId(id) {
    return "https://books.google.com/books/content?id=" + id + "&printsec=frontcover&img=1&zoom=1";
  }

  function bookCard(book) {
    var a = document.createElement("a");
    a.className = "book-card";
    if (book.fav) a.classList.add("is-fav");
    a.href = "/bookshelf/" + book.slug + "/";

    var frame = document.createElement("div");
    frame.className = "book-cover-frame";
    if (book.fav) frame.classList.add("book-fav-ring");

    if (book.cover || book.coverIsbn || book.coverGoogle || book.coverDirect) {
      var img = document.createElement("img");
      img.src = book.cover
        ? coverUrl(book.cover)
        : book.coverIsbn
        ? coverUrlByIsbn(book.coverIsbn)
        : book.coverGoogle
        ? coverUrlByGoogleId(book.coverGoogle)
        : book.coverDirect;
      img.alt = book.title;
      img.loading = "lazy";
      frame.appendChild(img);
    } else {
      var fb = document.createElement("div");
      fb.className = "book-cover-fallback";
      fb.textContent = book.title;
      frame.appendChild(fb);
    }

    if (book.fav) {
      var star = document.createElement("span");
      star.className = "book-fav-badge";
      star.textContent = "★";
      frame.appendChild(star);
    }

    var caption = document.createElement("div");
    caption.className = "book-card-title";
    caption.textContent = book.title;

    a.appendChild(frame);
    a.appendChild(caption);
    return a;
  }

  var root = document.getElementById("shelf-root");

  var toggleBar = document.createElement("div");
  toggleBar.className = "shelf-toggle-bar";
  var toggleLabel = document.createElement("label");
  toggleLabel.className = "shelf-toggle";
  var toggleInput = document.createElement("input");
  toggleInput.type = "checkbox";
  toggleInput.id = "shelf-fav-toggle";
  toggleInput.className = "shelf-toggle-input";
  var toggleTrack = document.createElement("span");
  toggleTrack.className = "shelf-toggle-track";
  var toggleThumb = document.createElement("span");
  toggleThumb.className = "shelf-toggle-thumb";
  toggleTrack.appendChild(toggleThumb);
  var toggleText = document.createElement("span");
  toggleText.className = "shelf-toggle-text";
  toggleText.textContent = "★ Favorites only";
  toggleLabel.appendChild(toggleInput);
  toggleLabel.appendChild(toggleTrack);
  toggleLabel.appendChild(toggleText);
  toggleBar.appendChild(toggleLabel);
  root.appendChild(toggleBar);

  toggleInput.addEventListener("change", function () {
    root.classList.toggle("shelf-favonly", toggleInput.checked);
  });

  SECTIONS.forEach(function (section) {
    var wrap = document.createElement("div");
    wrap.className = "shelf-section";
    if (!section.books.some(function (b) { return b.fav; })) {
      wrap.classList.add("no-fav");
    }

    var head = document.createElement("div");
    head.className = "shelf-section-head";
    head.textContent = section.emoji + " " + section.title;
    wrap.appendChild(head);

    var desc = document.createElement("div");
    desc.className = "shelf-section-desc";
    desc.textContent = section.desc;
    wrap.appendChild(desc);

    var rowWrap = document.createElement("div");
    rowWrap.className = "shelf-row-wrap";

    var leftBtn = document.createElement("button");
    leftBtn.className = "shelf-arrow left";
    leftBtn.setAttribute("aria-label", "Scroll left");
    leftBtn.textContent = "←";

    var row = document.createElement("div");
    row.className = "shelf-row";
    section.books.forEach(function (book) {
      row.appendChild(bookCard(book));
    });

    var rightBtn = document.createElement("button");
    rightBtn.className = "shelf-arrow right";
    rightBtn.setAttribute("aria-label", "Scroll right");
    rightBtn.textContent = "→";

    leftBtn.addEventListener("click", function () {
      if (row.scrollLeft <= 1) {
        row.scrollTo({ left: row.scrollWidth, behavior: "smooth" });
      } else {
        row.scrollBy({ left: -300, behavior: "smooth" });
      }
    });
    rightBtn.addEventListener("click", function () {
      if (row.scrollLeft + row.clientWidth >= row.scrollWidth - 1) {
        row.scrollTo({ left: 0, behavior: "smooth" });
      } else {
        row.scrollBy({ left: 300, behavior: "smooth" });
      }
    });

    rowWrap.appendChild(leftBtn);
    rowWrap.appendChild(row);
    rowWrap.appendChild(rightBtn);
    wrap.appendChild(rowWrap);

    root.appendChild(wrap);
  });
})();
</script>

<details class="bookshelf-section">
<summary>🎙️ Podcasts & Talks</summary>
<span class="list-item">When I'm not reading, I'm probably listening to one of these podcasts or talks:</span>
<p>
<span class="book-entry">1. <a href="https://open.spotify.com/episode/6nE2aDcXQye5R402hYIbGI">David Deutsch and Naval Ravikant - The Tim Ferriss Show</a></span>
<span class="book-entry">2. <a href="https://open.spotify.com/episode/3ijkVfaht5kcFPvHcCbYYD">Joe Rogan Experience #1309 - Naval Ravikant</a></span>
<span class="book-entry">3. <a href="https://open.spotify.com/episode/2f1cO0R0P2UOTI5rCcg0qH">Why Rejection is Awesome - Talks at Google (Ep369)</a></span>
<span class="book-entry">4. <a href="https://open.spotify.com/episode/1DW2fkyEkgZaEP40Mj6H9m">How To Get Rich: Every Episode - Naval</a></span>
<span class="book-entry">5. <a href="https://open.spotify.com/episode/1ikGgmQzkw1OsCxKcHwlxq">Sara Imari Walker #2184 - Joe Rogan</a></span>
<span class="book-entry">6. <a href="https://open.spotify.com/episode/1hGNQQhkuoewA6TNK3KOAc">Naval Ravikant: The Beginning of Infinity - Arjun Khemani</a></span>
<span class="book-entry">7. <a href="https://open.spotify.com/episode/67fjltTOUn6ypGqXHcPRXi">Joe Rogan Experience #2217 - Brian Cox</a></span>
<span class="book-entry">8. Brian Cox: Why black holes could hold the secret to time and space - Big Think</span>
<span class="book-entry">9. <a href="https://sarthak268.github.io/bookshelf/lex_elon_252/">Lex Fridman Podcast #252 - Elon Musk</a></span>
<span class="book-entry">10. <a href="https://open.spotify.com/episode/3KSOxrjalScxHFQF9u8M46">Lex Fridman Podcast #468 - Janna Levin</a></span>
<span class="book-entry">11. <a href="https://open.spotify.com/episode/2lqNevhLx08QPmvCLjhS4g">Hardcore History: Supernova in the East - Dan Carlin</a></span>
<span class="book-entry">12. <a href="https://open.spotify.com/episode/3CUzPLZC4OEj9aROCEiEAe">Joe Rogan Experience #1003 - Sean Carroll</a></span>
</p>
</details>

<details class="bookshelf-section">
<summary>🎬 Documentaries</summary>
<span class="list-item">And a few documentaries that left a mark:</span>
<p>
<span class="book-entry">1. <a href="https://youtu.be/d95J8yzvjbQ?si=rX04eGo_SIrlgyZZ">The Thinking Game</a>: the story of DeepMind and Demis Hassabis 🧠</span>
</p>
</details>

<br>
<span class="list-item">Got a book I should read? [I'm all ears.](//twitter.com/@sarthak__bhagat)</span><br>
