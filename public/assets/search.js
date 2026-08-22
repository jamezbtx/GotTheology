(function () {
  "use strict";

  var INDEX_URL = "/assets/search-index.json";
  var indexPromise = null;
  var indexData = null;

  function loadIndex() {
    if (indexPromise) return indexPromise;
    indexPromise = fetch(INDEX_URL)
      .then(function (res) {
        if (!res.ok) throw new Error("Failed to load search index");
        return res.json();
      })
      .then(function (data) {
        indexData = Array.isArray(data) ? data : [];
        return indexData;
      })
      .catch(function (err) {
        indexPromise = null;
        throw err;
      });
    return indexPromise;
  }

  function normalize(s) {
    return String(s || "")
      .toLowerCase()
      .normalize("NFKD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[–—−]/g, "-")
      .replace(/\s+/g, " ")
      .trim();
  }

  function tokenize(q) {
    return normalize(q)
      .split(/[^a-z0-9:.-]+/)
      .filter(Boolean);
  }

  function scoreEntry(entry, tokens) {
    if (!tokens.length) return 0;
    var hay =
      normalize(entry.title) +
      " " +
      normalize(entry.book) +
      " " +
      normalize(entry.context) +
      " " +
      normalize(entry.text);
    var score = 0;
    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i];
      if (!hay.includes(t)) return 0;
      if (normalize(entry.title).includes(t)) score += 8;
      else if (normalize(entry.book).includes(t)) score += 5;
      else if (normalize(entry.context).includes(t)) score += 3;
      else score += 1;
    }
    return score;
  }

  function search(query, limit) {
    var tokens = tokenize(query);
    if (!tokens.length || !indexData) return [];
    var scored = [];
    for (var i = 0; i < indexData.length; i++) {
      var s = scoreEntry(indexData[i], tokens);
      if (s > 0) scored.push({ entry: indexData[i], score: s });
    }
    scored.sort(function (a, b) {
      if (b.score !== a.score) return b.score - a.score;
      if (a.entry.book !== b.entry.book) return a.entry.book.localeCompare(b.entry.book);
      if (a.entry.chapter !== b.entry.chapter) return a.entry.chapter - b.entry.chapter;
      return a.entry.verseStart - b.entry.verseStart;
    });
    return scored.slice(0, limit || 50).map(function (x) {
      return x.entry;
    });
  }

  function escapeHtml(str) {
    return String(str ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function snippet(text, max) {
    var t = String(text || "").trim().replace(/\s+/g, " ");
    if (t.length <= max) return t;
    return t.slice(0, max - 1).trimEnd() + "\u2026";
  }

  function renderResults(container, results, query) {
    if (!container) return;
    var q = String(query || "").trim();
    if (!q) {
      container.innerHTML = "";
      container.hidden = true;
      container.removeAttribute("data-has-results");
      return;
    }
    container.hidden = false;
    if (!results.length) {
      container.setAttribute("data-has-results", "0");
      container.innerHTML =
        '<p class="search-empty">No passages match \u201c' +
        escapeHtml(q) +
        "\u201d.</p>";
      return;
    }
    container.setAttribute("data-has-results", "1");
    var items = results
      .map(function (r) {
        var ctx = snippet(r.context || r.text || "", 140);
        return (
          '<li><a href="' +
          escapeHtml(r.url) +
          '"><span class="search-result-title">' +
          escapeHtml(r.title) +
          '</span><span class="search-result-snippet">' +
          escapeHtml(ctx) +
          "</span></a></li>"
        );
      })
      .join("");
    container.innerHTML =
      '<p class="search-status" role="status">' +
      results.length +
      (results.length === 1 ? " passage" : " passages") +
      "</p><ul class=\"search-results-list\">" +
      items +
      "</ul>";
  }

  function setCatalogVisibility(hidden) {
    document.querySelectorAll("[data-search-catalog]").forEach(function (el) {
      el.hidden = !!hidden;
    });
  }

  function bindFullSearch(root) {
    var input = root.querySelector("[data-search-input]");
    var resultsEl = root.querySelector("[data-search-results]");
    if (!input || !resultsEl) return;

    var params = new URLSearchParams(window.location.search);
    var initial = params.get("q") || "";
    if (initial) input.value = initial;

    function run() {
      var q = input.value;
      loadIndex()
        .then(function () {
          var results = search(q, 40);
          renderResults(resultsEl, results, q);
          setCatalogVisibility(String(q).trim().length > 0);
        })
        .catch(function () {
          resultsEl.hidden = false;
          resultsEl.innerHTML =
            '<p class="search-empty">Search is unavailable right now.</p>';
        });
    }

    var timer = null;
    input.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(run, 80);
      var url = new URL(window.location.href);
      var q = input.value.trim();
      if (q) url.searchParams.set("q", q);
      else url.searchParams.delete("q");
      window.history.replaceState({}, "", url.pathname + url.search + url.hash);
    });

    loadIndex().then(run).catch(function () {
      /* ignore until user types */
    });
    if (initial) run();
  }

  function bindCompactForms() {
    document.querySelectorAll("form[data-search-compact]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        var input = form.querySelector('input[name="q"]');
        var q = input ? String(input.value || "").trim() : "";
        if (!q) {
          e.preventDefault();
          window.location.href = form.getAttribute("action") || "/bible/";
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-search-panel]").forEach(bindFullSearch);
    bindCompactForms();
  });
})();
