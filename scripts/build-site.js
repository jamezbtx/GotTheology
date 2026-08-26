import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const CONTENT = path.join(ROOT, "content");
const BOOKS_DIR = path.join(CONTENT, "books");
const PUBLIC = path.join(ROOT, "public");
const BIBLE_OUT = path.join(PUBLIC, "bible");
const VOICES_PATH = path.join(CONTENT, "voices.json");
const YEAR = new Date().getFullYear();
const SITE_ORIGIN = "https://got-theology.com";


const CANONICAL_BOOKS = [
  // Old Testament (39)
  { name: "Genesis", slug: "genesis", testament: "ot" },
  { name: "Exodus", slug: "exodus", testament: "ot" },
  { name: "Leviticus", slug: "leviticus", testament: "ot" },
  { name: "Numbers", slug: "numbers", testament: "ot" },
  { name: "Deuteronomy", slug: "deuteronomy", testament: "ot" },
  { name: "Joshua", slug: "joshua", testament: "ot" },
  { name: "Judges", slug: "judges", testament: "ot" },
  { name: "Ruth", slug: "ruth", testament: "ot" },
  { name: "1 Samuel", slug: "1-samuel", testament: "ot" },
  { name: "2 Samuel", slug: "2-samuel", testament: "ot" },
  { name: "1 Kings", slug: "1-kings", testament: "ot" },
  { name: "2 Kings", slug: "2-kings", testament: "ot" },
  { name: "1 Chronicles", slug: "1-chronicles", testament: "ot" },
  { name: "2 Chronicles", slug: "2-chronicles", testament: "ot" },
  { name: "Ezra", slug: "ezra", testament: "ot" },
  { name: "Nehemiah", slug: "nehemiah", testament: "ot" },
  { name: "Esther", slug: "esther", testament: "ot" },
  { name: "Job", slug: "job", testament: "ot" },
  { name: "Psalms", slug: "psalms", testament: "ot" },
  { name: "Proverbs", slug: "proverbs", testament: "ot" },
  { name: "Ecclesiastes", slug: "ecclesiastes", testament: "ot" },
  { name: "Song of Solomon", slug: "song-of-solomon", testament: "ot" },
  { name: "Isaiah", slug: "isaiah", testament: "ot" },
  { name: "Jeremiah", slug: "jeremiah", testament: "ot" },
  { name: "Lamentations", slug: "lamentations", testament: "ot" },
  { name: "Ezekiel", slug: "ezekiel", testament: "ot" },
  { name: "Daniel", slug: "daniel", testament: "ot" },
  { name: "Hosea", slug: "hosea", testament: "ot" },
  { name: "Joel", slug: "joel", testament: "ot" },
  { name: "Amos", slug: "amos", testament: "ot" },
  { name: "Obadiah", slug: "obadiah", testament: "ot" },
  { name: "Jonah", slug: "jonah", testament: "ot" },
  { name: "Micah", slug: "micah", testament: "ot" },
  { name: "Nahum", slug: "nahum", testament: "ot" },
  { name: "Habakkuk", slug: "habakkuk", testament: "ot" },
  { name: "Zephaniah", slug: "zephaniah", testament: "ot" },
  { name: "Haggai", slug: "haggai", testament: "ot" },
  { name: "Zechariah", slug: "zechariah", testament: "ot" },
  { name: "Malachi", slug: "malachi", testament: "ot" },
  // New Testament (27)
  { name: "Matthew", slug: "matthew", testament: "nt" },
  { name: "Mark", slug: "mark", testament: "nt" },
  { name: "Luke", slug: "luke", testament: "nt" },
  { name: "John", slug: "john", testament: "nt" },
  { name: "Acts", slug: "acts", testament: "nt" },
  { name: "Romans", slug: "romans", testament: "nt" },
  { name: "1 Corinthians", slug: "1-corinthians", testament: "nt" },
  { name: "2 Corinthians", slug: "2-corinthians", testament: "nt" },
  { name: "Galatians", slug: "galatians", testament: "nt" },
  { name: "Ephesians", slug: "ephesians", testament: "nt" },
  { name: "Philippians", slug: "philippians", testament: "nt" },
  { name: "Colossians", slug: "colossians", testament: "nt" },
  { name: "1 Thessalonians", slug: "1-thessalonians", testament: "nt" },
  { name: "2 Thessalonians", slug: "2-thessalonians", testament: "nt" },
  { name: "1 Timothy", slug: "1-timothy", testament: "nt" },
  { name: "2 Timothy", slug: "2-timothy", testament: "nt" },
  { name: "Titus", slug: "titus", testament: "nt" },
  { name: "Philemon", slug: "philemon", testament: "nt" },
  { name: "Hebrews", slug: "hebrews", testament: "nt" },
  { name: "James", slug: "james", testament: "nt" },
  { name: "1 Peter", slug: "1-peter", testament: "nt" },
  { name: "2 Peter", slug: "2-peter", testament: "nt" },
  { name: "1 John", slug: "1-john", testament: "nt" },
  { name: "2 John", slug: "2-john", testament: "nt" },
  { name: "3 John", slug: "3-john", testament: "nt" },
  { name: "Jude", slug: "jude", testament: "nt" },
  { name: "Revelation", slug: "revelation", testament: "nt" },
];


function absoluteUrl(pathname) {
  if (!pathname) return SITE_ORIGIN + "/";
  if (/^https?:\/\//i.test(pathname)) return pathname;
  return SITE_ORIGIN + (pathname.startsWith("/") ? pathname : "/" + pathname);
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function escapeHtml(str) {
  return String(str ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function paragraphsHtml(text) {
  const raw = String(text ?? "").trim();
  if (!raw) return "<p></p>";
  const parts = raw
    .split(/\n\s*\n/)
    .map((p) => p.replace(/\s*\n\s*/g, " ").trim())
    .filter(Boolean);
  return parts.map((p) => "<p>" + escapeHtml(p) + "</p>").join("\n            ");
}

function enDashRange(start, end) {
  if (start === end || end == null) return String(start);
  return start + "\u2013" + end;
}

function verseFileStem(verseStart, verseEnd) {
  if (verseEnd == null || verseEnd === verseStart) return String(verseStart);
  return verseStart + "-" + verseEnd;
}

function passageUrl(bookSlug, chapter, verseStart, verseEnd) {
  return "/bible/" + bookSlug + "/" + chapter + "/" + verseFileStem(verseStart, verseEnd) + ".html";
}


function resolveVerseBounds(data, fileStem) {
  let verseStart = data.verseStart;
  let verseEnd = data.verseEnd;
  if (verseStart == null && Array.isArray(data.verses) && data.verses.length) {
    const nums = data.verses.map((v) => Number(v.number)).filter((n) => !Number.isNaN(n));
    verseStart = Math.min(...nums);
    verseEnd = Math.max(...nums);
  }
  if (verseStart == null && fileStem) {
    const m = String(fileStem).match(/^(\d+)(?:-(\d+))?$/);
    if (m) {
      verseStart = Number(m[1]);
      verseEnd = m[2] ? Number(m[2]) : verseStart;
    }
  }
  if (verseEnd == null) verseEnd = verseStart;
  return { verseStart, verseEnd };
}

function validatePassage(data, relPath) {
  const errors = [];
  if (!data.book) errors.push("missing book");
  if (!data.bookSlug) errors.push("missing bookSlug");
  if (data.chapter == null) errors.push("missing chapter");
  if (!Array.isArray(data.verses) || data.verses.length === 0) errors.push("missing verses[]");
  if (errors.length) throw new Error(relPath + ": " + errors.join("; "));
}

function loadVoicesDefault() {
  if (!fs.existsSync(VOICES_PATH)) return null;
  return JSON.parse(fs.readFileSync(VOICES_PATH, "utf8"));
}

function findPassageFiles(dir, acc = []) {
  if (!fs.existsSync(dir)) return acc;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) findPassageFiles(full, acc);
    else if (entry.isFile() && entry.name.endsWith(".json")) acc.push(full);
  }
  return acc;
}

function truncate(s, n) {
  const t = String(s).trim();
  if (t.length <= n) return t;
  return t.slice(0, n - 1).trimEnd() + "\u2026";
}

function buildSearchText(data) {
  const parts = [];
  const title =
    data.title ||
    data.book + " " + data.chapter + ":" + enDashRange(data.verseStart, data.verseEnd);
  parts.push(title);
  parts.push(data.book || "");
  if (data.context) parts.push(data.context);
  for (const v of data.verses || []) {
    if (v && v.text) parts.push(String(v.text));
    if (v && v.number != null) {
      parts.push(data.book + " " + data.chapter + ":" + v.number);
    }
  }
  return parts.join(" ").replace(/\s+/g, " ").trim();
}

function renderVoicesSection(voices) {
  if (!voices) return "";
  const quoteCards = (list) =>
    (list || [])
      .map(
        (q) => `
            <div class="quote-card">
              <blockquote>\u201c${escapeHtml(q.quote)}\u201d</blockquote>
              <cite><strong>${escapeHtml(q.cite)}</strong> \u00b7 ${escapeHtml(q.source || "")}</cite>
            </div>`
      )
      .join("");
  const arm = quoteCards(voices.arminian);
  const ref = quoteCards(voices.reformed);
  return `
      <section class="voices" id="voices" aria-labelledby="voices-heading">
        <div class="reader">
          <div class="voices-intro">
            <p class="eyebrow">${escapeHtml(voices.eyebrow || "From the tradition")}</p>
            <h2 id="voices-heading">${escapeHtml(voices.heading || "Voices from both camps")}</h2>
            <p>${escapeHtml(voices.intro || "")}</p>
          </div>
          <div class="voices-grid">
            <div class="voices-col arminian">
              <h3><span class="dual-label label-arminian" style="margin:0">Arminian</span> Notable voices</h3>
              ${arm}
            </div>
            <div class="voices-col reformed">
              <h3><span class="dual-label label-reformed" style="margin:0">Reformed</span> Notable voices</h3>
              ${ref}
            </div>
          </div>
          ${voices.note ? `<p class="voices-note">${escapeHtml(voices.note)}</p>` : ""}
        </div>
      </section>`;
}

function renderVerseCard(book, chapter, verse) {
  const n = verse.number;
  const contrast = verse.keyContrast
    ? `
        <p class="key-contrast">
          <strong>Key contrast</strong>
          ${escapeHtml(verse.keyContrast)}
        </p>`
    : "";
  return `
      <article class="verse-card" id="v${escapeHtml(n)}">
        <div class="verse-text-block">
          <p class="verse-ref">${escapeHtml(book)} ${escapeHtml(chapter)}:${escapeHtml(n)}</p>
          <p class="verse-scripture">
            <span class="vnum">${escapeHtml(n)}</span>${escapeHtml(verse.text)}
          </p>
        </div>
        <div class="dual-cols">
          <div class="dual-col">
            <span class="dual-label label-arminian">Arminian</span>
            ${paragraphsHtml(verse.arminianNotes)}
          </div>
          <div class="dual-col">
            <span class="dual-label label-reformed">Reformed</span>
            ${paragraphsHtml(verse.reformedNotes)}
          </div>
        </div>${contrast}
      </article>`;
}

function renderPassagePage(data, opts) {
  const book = data.book;
  const bookSlug = data.bookSlug;
  const chapter = data.chapter;
  const verseStart = data.verseStart;
  const verseEnd = data.verseEnd;
  const translation = data.translation || "ESV";
  const context = data.context || "";
  const verses = data.verses;
  const eyebrow = data.eyebrow || "Passage";
  const rangeLabel = enDashRange(verseStart, verseEnd);
  const pageTitle = data.title || (book + " " + chapter + ":" + rangeLabel);
  const desc =
    data.description ||
    (context
      ? truncate(
          "Arminian and Reformed commentary on " + pageTitle + ". " + context,
          160
        )
      : "Verse-by-verse Arminian and Reformed commentary on " +
        pageTitle +
        ". Free to read on GotTheology.");
  const displayDisclaimer =
    data.disclaimer ||
    `<strong>About these notes.</strong>
        Commentary here is pastoral and educational. It is not a substitute for reading
        primary sources, confessions, or trusted teachers in either tradition. Both Arminian and
        Reformed families contain internal diversity (Wesleyan, classical Remonstrant, confessional
        Calvinist, and more). GotTheology aims for fair representation\u2014not a final verdict.`;

  const verseCards = verses.map((v) => renderVerseCard(book, chapter, v)).join("\n");
  const voicesHtml = opts.voices ? renderVoicesSection(opts.voices) : "";
  const canonicalPath = absoluteUrl(
    opts.canonicalPath || passageUrl(bookSlug, chapter, verseStart, verseEnd)
  );
  const ogTitle = pageTitle + " \u2014 GotTheology";

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <title>${escapeHtml(pageTitle)} \u2014 GotTheology</title>
  <meta name="description" content="${escapeHtml(desc)}" />
  <link rel="canonical" href="${escapeHtml(canonicalPath)}" />
  <meta property="og:title" content="${escapeHtml(ogTitle)}" />
  <meta property="og:description" content="${escapeHtml(desc)}" />
  <meta property="og:url" content="${escapeHtml(canonicalPath)}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="GotTheology" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/gottheology.css" />
</head>
<body>
  <header class="site-header">
    <div class="container nav">
      <a href="/index.html" class="wordmark">Got<span>-Theology</span>.com</a>
      <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" id="navToggle">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path d="M4 7h16M4 12h16M4 17h16"/>
        </svg>
      </button>
      <nav class="nav-links" id="navLinks" aria-label="Primary">
        <a href="/index.html">Home</a>
        <a href="/bible/index.html">Bible</a>
        <a href="/index.html#perspectives">Perspectives</a>
        <a href="/bible/index.html" class="btn btn-primary btn-nav nav-cta">Browse Bible</a>
      </nav>
    </div>
  </header>

  <main>
    <header class="passage-header">
      <div class="reader">
        <p class="eyebrow">${escapeHtml(eyebrow)}</p>
        <h1>${escapeHtml(book)} ${escapeHtml(chapter)}</h1>
        <div class="passage-meta">
          <span>Verse${verseStart === verseEnd ? "" : "s"} ${escapeHtml(rangeLabel)}</span>
          <span aria-hidden="true">\u00b7</span>
          <span class="pill">${escapeHtml(translation)}</span>
        </div>
        ${context ? `<p class="passage-context">${escapeHtml(context)}</p>` : ""}
      </div>
    </header>

    <div class="reader verse-list">
${verseCards}

      <aside class="ad-slot ad-slot-narrow" aria-label="Advertisement">
        <span class="ad-label">Advertisement</span>
        <div class="ad-frame ad-frame--leader" data-ad-slot="verse-after-notes">
          <span>Ad slot \u00b7 kept below the verse notes \u00b7 <strong>728\u00d790</strong></span>
        </div>
      </aside>

      <aside class="disclaimer" role="note">
        ${displayDisclaimer}
      </aside>
    </div>
${voicesHtml}

      <aside class="ad-slot ad-slot-narrow" aria-label="Advertisement">
        <span class="ad-label">Advertisement</span>
        <div class="ad-frame ad-frame--rect" data-ad-slot="verse-before-cta">
          <span>Ad slot \u00b7 <strong>300\u00d7250</strong></span>
        </div>
      </aside>

    <section class="bottom-cta" aria-labelledby="cta-heading">
      <div class="reader">
        <div class="cta-box">
          <p class="eyebrow" style="color: var(--gold-soft);">Keep reading</p>
          <h2 id="cta-heading">Matthew, Colossians, and Genesis are live</h2>
          <p>Browse verse-by-verse notes\u2014Arminian and Reformed, side by side\u2014kept fair and close to the text.</p>
          <a href="/bible/index.html" class="btn btn-gold">Browse the Bible</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-inner">
        <div class="footer-brand">
          <a href="/index.html" class="wordmark">Got<span>-Theology</span>.com</a>
          <p>Verse-by-verse theology from the Bible\u2014Arminian and Reformed, side by side. Free to read, supported by ads.</p>
        </div>
        <nav class="footer-links" aria-label="Footer">
          <a href="/index.html">Home</a>
          <a href="/bible/index.html">Bible</a>
          <a href="/index.html#perspectives">Perspectives</a>
          <a href="/index.html#updates">Updates</a>
        </nav>
      </div>
      <div class="footer-bottom">
        <span>\u00a9 ${YEAR} Got-Theology.com. All rights reserved.</span>
        <span>${escapeHtml(pageTitle)}</span>
      </div>
    </div>
  </footer>

  <script>
    (function () {
      var toggle = document.getElementById("navToggle");
      var links = document.getElementById("navLinks");
      var header = document.querySelector(".site-header");
      if (!toggle || !links) return;
      toggle.addEventListener("click", function () {
        var open = links.classList.toggle("open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        header.classList.toggle("is-open", open);
      });
      links.querySelectorAll("a").forEach(function (a) {
        a.addEventListener("click", function () {
          links.classList.remove("open");
          header.classList.remove("is-open");
          toggle.setAttribute("aria-expanded", "false");
        });
      });
    })();
  </script>
</body>
</html>
`;
}

function renderBibleIndex(passages) {
  const bySlug = new Map();
  for (const p of passages) {
    const key = p.bookSlug || String(p.book || "").toLowerCase().replace(/\s+/g, "-");
    if (!bySlug.has(key)) bySlug.set(key, []);
    bySlug.get(key).push(p);
  }

  function renderBookBlock(book) {
    const items = bySlug.get(book.slug) || [];
    const live = items.length > 0;
    if (live) {
      const sorted = [...items].sort((a, b) => {
        if (a.chapter !== b.chapter) return a.chapter - b.chapter;
        return a.verseStart - b.verseStart;
      });
      const lis = sorted
        .map((item) => {
          const range = enDashRange(item.verseStart, item.verseEnd);
          const label = item.book + " " + item.chapter + ":" + range;
          const meta = [item.translation, item.context ? truncate(item.context, 90) : null]
            .filter(Boolean)
            .join(" \u00b7 ");
          const metaHtml = meta
            ? '<span class="meta">' + escapeHtml(meta) + "</span>"
            : "";
          return (
            '<li><a href="' +
            escapeHtml(item.url) +
            '"><span class="ref">' +
            escapeHtml(label) +
            "</span>" +
            metaHtml +
            "</a></li>"
          );
        })
        .join("\n          ");
      return (
        '\n      <section class="book-block book-block--live" data-book="' +
        escapeHtml(book.slug) +
        '">\n        <h2>' +
        escapeHtml(book.name) +
        '</h2>\n        <ul class="passage-list">\n          ' +
        lis +
        "\n        </ul>\n      </section>"
      );
    }
    return (
      '\n      <section class="book-block book-block--soon" data-book="' +
      escapeHtml(book.slug) +
      '">\n        <h2>' +
      escapeHtml(book.name) +
      '</h2>\n        <p class="coming-soon">Coming soon</p>\n      </section>'
    );
  }

  function renderTestament(id, title, books) {
    const blocks = books.map(renderBookBlock).join("\n");
    return (
      '\n      <section class="testament" id="' +
      id +
      '" aria-labelledby="' +
      id +
      '-heading">\n        <h2 class="testament-heading" id="' +
      id +
      '-heading">' +
      escapeHtml(title) +
      "</h2>\n        " +
      blocks +
      "\n      </section>"
    );
  }

  const ot = CANONICAL_BOOKS.filter((b) => b.testament === "ot");
  const nt = CANONICAL_BOOKS.filter((b) => b.testament === "nt");
  const body =
    renderTestament("old-testament", "Old Testament", ot) +
    "\n" +
    renderTestament("new-testament", "New Testament", nt);

  return [
    "<!DOCTYPE html>",
    '<html lang="en">',
    "<head>",
    '  <meta charset="UTF-8" />',
    '  <meta name="viewport" content="width=device-width, initial-scale=1.0" />',
    '  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />',
    "  <title>Bible Index \u2014 GotTheology</title>",
    '  <meta name="description" content="Browse free verse-by-verse Arminian and Reformed commentary on GotTheology." />',
    '  <link rel="canonical" href="' + absoluteUrl("/bible/") + '" />',
    '  <meta property="og:title" content="Bible Index \u2014 GotTheology" />',
    '  <meta property="og:description" content="Browse free verse-by-verse Arminian and Reformed commentary on GotTheology." />',
    '  <meta property="og:url" content="' + absoluteUrl("/bible/") + '" />',
    '  <meta property="og:type" content="website" />',
    '  <meta property="og:site_name" content="GotTheology" />',
    '  <link rel="preconnect" href="https://fonts.googleapis.com" />',
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />',
    '  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet" />',
    '  <link rel="stylesheet" href="/assets/gottheology.css" />',
    "</head>",
    "<body>",
    '  <header class="site-header">',
    '    <div class="container nav">',
    '      <a href="/index.html" class="wordmark">Got<span>-Theology</span>.com</a>',
    '      <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" id="navToggle">',
    '        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">',
    '          <path d="M4 7h16M4 12h16M4 17h16"/>',
    "        </svg>",
    "      </button>",
    '      <nav class="nav-links" id="navLinks" aria-label="Primary">',
    '        <a href="/index.html">Home</a>',
    '        <a href="/bible/index.html">Bible</a>',
    '        <a href="/index.html#perspectives">Perspectives</a>',
    '        <a href="/bible/index.html" class="btn btn-primary btn-nav nav-cta">Browse Bible</a>',
    "      </nav>",
    "    </div>",
    "  </header>",
    '  <main class="bible-index">',
    '    <div class="reader">',
    '      <div class="page-intro">',
    '        <p class="eyebrow">Free to read</p>',
    "        <h1>Bible passages</h1>",
    "        <p>Arminian and Reformed notes side by side\u2014supported by ads, never paywalled.</p>",
    "      </div>",
    '      <div class="search-panel" data-search-panel>',
    '        <label class="search-label" for="siteSearch">Search passages</label>',
    '        <div class="search-field">',
    '          <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
    '          <input type="search" id="siteSearch" name="q" data-search-input placeholder="Search by book, verse, or wording\u2026" autocomplete="off" enterkeyhint="search" />',
    "        </div>",
    '        <div class="search-results" data-search-results hidden></div>',
    "      </div>",
    '      <div data-search-catalog>',
    body,
    "      </div>",
    "    </div>",
    "  </main>",
    '  <footer class="site-footer">',
    '    <div class="container">',
    '      <div class="footer-inner">',
    '        <div class="footer-brand">',
    '          <a href="/index.html" class="wordmark">Got<span>-Theology</span>.com</a>',
    "          <p>Verse-by-verse theology from the Bible\u2014Arminian and Reformed, side by side. Free to read, supported by ads.</p>",
    "        </div>",
    '        <nav class="footer-links" aria-label="Footer">',
    '          <a href="/index.html">Home</a>',
    '          <a href="/bible/index.html">Bible</a>',
    "        </nav>",
    "      </div>",
    '      <div class="footer-bottom">',
    "        <span>\u00a9 " + YEAR + " Got-Theology.com. All rights reserved.</span>",
    "        <span>Bible index</span>",
    "      </div>",
    "    </div>",
    "  </footer>",
    "  <script>",
    "    (function () {",
    '      var toggle = document.getElementById("navToggle");',
    '      var links = document.getElementById("navLinks");',
    '      var header = document.querySelector(".site-header");',
    "      if (!toggle || !links) return;",
    '      toggle.addEventListener("click", function () {',
    '        var open = links.classList.toggle("open");',
    '        toggle.setAttribute("aria-expanded", open ? "true" : "false");',
    '        header.classList.toggle("is-open", open);',
    "      });",
    '      links.querySelectorAll("a").forEach(function (a) {',
    '        a.addEventListener("click", function () {',
    '          links.classList.remove("open");',
    '          header.classList.remove("is-open");',
    '          toggle.setAttribute("aria-expanded", "false");',
    "        });",
    "      });",
    "    })();",
    "  </script>",
    '  <script src="/assets/search.js" defer></script>',
    "</body>",
    "</html>",
    "",
  ].join("\n");
}

function writeRobotsTxt() {
  const body =
    "User-agent: *\n" +
    "Allow: /\n" +
    "\n" +
    "Sitemap: " +
    SITE_ORIGIN +
    "/sitemap.xml\n";
  const outPath = path.join(PUBLIC, "robots.txt");
  fs.writeFileSync(outPath, body, "utf8");
  console.log("  wrote " + path.relative(ROOT, outPath));
}

function writeSitemap(passages) {
  const urls = ["/", "/bible/", ...passages.map((p) => p.url)];
  const seen = new Set();
  const unique = [];
  for (const u of urls) {
    const abs = absoluteUrl(u);
    if (seen.has(abs)) continue;
    seen.add(abs);
    unique.push(abs);
  }
  const urlEntries = unique
    .map((loc) => "  <url>\n    <loc>" + escapeHtml(loc) + "</loc>\n  </url>")
    .join("\n");
  const xml =
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    urlEntries +
    "\n</urlset>\n";
  const outPath = path.join(PUBLIC, "sitemap.xml");
  fs.writeFileSync(outPath, xml, "utf8");
  console.log("  wrote " + path.relative(ROOT, outPath) + " (" + unique.length + " URLs)");
}

function cleanGeneratedBibleTree() {
  if (fs.existsSync(BIBLE_OUT)) {
    fs.rmSync(BIBLE_OUT, { recursive: true, force: true });
  }
  ensureDir(BIBLE_OUT);
}

function main() {
  ensureDir(path.join(PUBLIC, "assets"));
  if (!fs.existsSync(path.join(PUBLIC, "assets", "gottheology.css"))) {
    console.warn("Warning: public/assets/gottheology.css missing.");
  }

  cleanGeneratedBibleTree();

  const siteVoices = loadVoicesDefault();
  const files = findPassageFiles(BOOKS_DIR).sort();
  const passages = [];
  let sampleAliasHtml = null;

  console.log("Found " + files.length + " passage file(s).");

  for (const file of files) {
    const rel = path.relative(ROOT, file);
    let data;
    try {
      data = JSON.parse(fs.readFileSync(file, "utf8"));
    } catch (err) {
      throw new Error(rel + ": invalid JSON (" + err.message + ")");
    }

    validatePassage(data, rel);
    const fileStem = path.basename(file, ".json");
    const bounds = resolveVerseBounds(data, fileStem);
    data.verseStart = bounds.verseStart;
    data.verseEnd = bounds.verseEnd;

    let voices = null;
    if (data.voices) voices = data.voices;
    else if (data.showVoices === false) voices = null;
    else voices = siteVoices;

    const url = passageUrl(data.bookSlug, data.chapter, data.verseStart, data.verseEnd);
    const outPath = path.join(PUBLIC, url.replace(/^\//, ""));
    ensureDir(path.dirname(outPath));

    const html = renderPassagePage(data, { voices, canonicalPath: url });
    fs.writeFileSync(outPath, html, "utf8");
    console.log("  wrote " + path.relative(ROOT, outPath));

    const title =
      data.title ||
      data.book + " " + data.chapter + ":" + enDashRange(data.verseStart, data.verseEnd);
    passages.push({
      book: data.book,
      bookSlug: data.bookSlug,
      chapter: Number(data.chapter),
      verseStart: data.verseStart,
      verseEnd: data.verseEnd,
      translation: data.translation || "ESV",
      title,
      context: data.context || "",
      url,
      text: buildSearchText({ ...data, title }),
    });

    if (
      data.bookSlug === "ephesians" &&
      Number(data.chapter) === 1 &&
      Number(data.verseStart) === 3 &&
      Number(data.verseEnd) === 6
    ) {
      sampleAliasHtml = html;
    }
  }

  const indexPath = path.join(BIBLE_OUT, "index.html");
  fs.writeFileSync(indexPath, renderBibleIndex(passages), "utf8");
  console.log("  wrote " + path.relative(ROOT, indexPath));

  const searchIndexPath = path.join(PUBLIC, "assets", "search-index.json");
  const searchIndex = passages.map((p) => ({
    book: p.book,
    bookSlug: p.bookSlug,
    chapter: p.chapter,
    verseStart: p.verseStart,
    verseEnd: p.verseEnd,
    title: p.title,
    context: p.context,
    url: p.url,
    text: p.text,
  }));
  fs.writeFileSync(searchIndexPath, JSON.stringify(searchIndex, null, 2) + "\n", "utf8");
  console.log("  wrote " + path.relative(ROOT, searchIndexPath) + " (" + searchIndex.length + " entries)");

  if (sampleAliasHtml) {
    const aliasPath = path.join(PUBLIC, "verse.html");
    fs.writeFileSync(aliasPath, sampleAliasHtml, "utf8");
    console.log("  wrote " + path.relative(ROOT, aliasPath) + " (Ephesians alias)");
  } else {
    console.warn("  note: no Ephesians 1:3-6; left public/verse.html unchanged");
  }

  writeRobotsTxt();
  writeSitemap(passages);

  console.log("Done. " + passages.length + " passage page(s) + bible index + search index + SEO files.");
}

try {
  main();
} catch (err) {
  console.error("Build failed:", err.message || err);
  process.exit(1);
}
