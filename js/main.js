(function () {
  "use strict";

  var root = document.documentElement;
  var THEME_KEY = "vm-portfolio-theme";

  /* ---------- Theme toggle ---------- */
  function applyTheme(theme) {
    if (theme === "dark" || theme === "light") {
      root.setAttribute("data-theme", theme);
    } else {
      root.removeAttribute("data-theme");
    }
  }

  try {
    var saved = localStorage.getItem(THEME_KEY);
    if (saved) applyTheme(saved);
  } catch (e) {}

  var themeToggle = document.getElementById("themeToggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      var current = root.getAttribute("data-theme");
      var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
      var effectiveCurrent = current || (prefersDark ? "dark" : "light");
      var next = effectiveCurrent === "dark" ? "light" : "dark";
      applyTheme(next);
      try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
    });
  }

  /* ---------- Mobile nav ---------- */
  var navToggle = document.getElementById("navToggle");
  var navLinks = document.getElementById("navLinks");
  if (navToggle && navLinks) {
    navToggle.addEventListener("click", function () {
      var isOpen = navLinks.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
    navLinks.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navLinks.classList.remove("open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ---------- Sticky header + scroll progress ---------- */
  var header = document.getElementById("siteHeader");
  var progressBar = document.getElementById("progressBar");

  function onScroll() {
    if (header) header.classList.toggle("scrolled", window.scrollY > 8);
    if (progressBar) {
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      var pct = docHeight > 0 ? (window.scrollY / docHeight) * 100 : 0;
      progressBar.style.width = pct + "%";
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Active nav link on scroll ---------- */
  var sections = Array.prototype.slice.call(document.querySelectorAll("main section[id], main > .hero[id]"));
  var navAnchors = document.querySelectorAll('a[data-nav]');

  if (sections.length && navAnchors.length && "IntersectionObserver" in window) {
    var navObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            navAnchors.forEach(function (a) {
              a.classList.toggle("active", a.getAttribute("href") === "#" + entry.target.id);
            });
          }
        });
      },
      { rootMargin: "-45% 0px -50% 0px" }
    );
    sections.forEach(function (s) { navObserver.observe(s); });
  }

  /* ---------- Reveal on scroll ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var revealObserver = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealEls.forEach(function (el) { revealObserver.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in-view"); });
  }

  /* ---------- Animated stat counters ---------- */
  var statNumbers = document.querySelectorAll(".stat-number");
  function animateCount(el) {
    var target = parseInt(el.getAttribute("data-count"), 10) || 0;
    var prefix = el.getAttribute("data-prefix") || "";
    var suffix = el.getAttribute("data-suffix") || "";
    var duration = 1200;
    var start = null;

    function step(ts) {
      if (start === null) start = ts;
      var progress = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      var value = Math.round(eased * target);
      el.textContent = prefix + value + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  if (statNumbers.length && "IntersectionObserver" in window) {
    var statObserver = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCount(entry.target);
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    statNumbers.forEach(function (el) { statObserver.observe(el); });
  }

  /* ---------- Experience timeline expand/collapse ---------- */
  var timelineItems = document.querySelectorAll(".timeline-item");
  timelineItems.forEach(function (item, idx) {
    var toggle = item.querySelector(".timeline-toggle");
    if (!toggle) return;
    toggle.addEventListener("click", function () {
      var isOpen = item.classList.toggle("open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
    if (idx === 0) {
      item.classList.add("open");
      toggle.setAttribute("aria-expanded", "true");
    }
  });

  /* ---------- Skill category filter ---------- */
  var filterChips = document.querySelectorAll(".filter-chip");
  var skillTags = document.querySelectorAll(".skill-tag");

  filterChips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      filterChips.forEach(function (c) { c.classList.remove("active"); });
      chip.classList.add("active");
      var filter = chip.getAttribute("data-filter");

      skillTags.forEach(function (tag) {
        var cat = tag.getAttribute("data-cat");
        tag.classList.toggle("hidden", filter !== "all" && cat !== filter);
      });

      timelineItems.forEach(function (item) { item.classList.remove("dimmed"); });
    });
  });

  /* ---------- Hover a role's tags to highlight matching skills ---------- */
  timelineItems.forEach(function (item) {
    var tagsAttr = item.getAttribute("data-tags");
    if (!tagsAttr) return;
    var tags = tagsAttr.split(",").map(function (t) { return t.trim().toLowerCase(); });

    item.addEventListener("mouseenter", function () {
      skillTags.forEach(function (tag) {
        var text = tag.textContent.trim().toLowerCase();
        var match = tags.some(function (t) { return t === text || t.indexOf(text) !== -1 || text.indexOf(t) !== -1; });
        tag.classList.toggle("hidden", !match);
      });
    });
    item.addEventListener("mouseleave", function () {
      var activeFilter = document.querySelector(".filter-chip.active");
      var filter = activeFilter ? activeFilter.getAttribute("data-filter") : "all";
      skillTags.forEach(function (tag) {
        var cat = tag.getAttribute("data-cat");
        tag.classList.toggle("hidden", filter !== "all" && cat !== filter);
      });
    });
  });

  /* ---------- Back to top ---------- */
  var backToTop = document.getElementById("backToTop");
  if (backToTop) {
    backToTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------- Footer year ---------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

})();
