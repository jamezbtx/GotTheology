import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const CONTENT = path.join(ROOT, "content");
const BOOKS_DIR = path.join(CONTENT, "books");
const PUBLIC = path.join(ROOT, "public");
const BIBLE_OUT = path.join(PUBLIC, "bible");
const DOCTRINES_DIR = path.join(CONTENT, "doctrines");
const ATTRIBUTES_DIR = path.join(CONTENT, "attributes");
const DOCTRINES_OUT = path.join(PUBLIC, "doctrines");
const ATTRIBUTES_OUT = path.join(PUBLIC, "attributes");
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

const DOCTRINE_ORDER = ["election", "atonement", "justification", "regeneration", "perseverance"];
const ATTRIBUTE_ORDER = ["holiness", "love", "justice", "mercy", "faithfulness", "omnipotence", "omniscience", "omnipresence", "immutability", "eternity", "sovereignty"];
const CHIP_SKIP_KEYS = new Set([
  "titus/2/9-10",
  "titus/1/1-4",
  "ephesians/1/1-2",
  "colossians/1/1-2",
  "1-timothy/1/1-2",
  "2-timothy/1/1-2",
]);

function topicFolder(kind) {
  return kind === "attribute" ? "attributes" : "doctrines";
}

function topicUrl(kind, slug) {
  return "/" + topicFolder(kind) + "/" + slug + ".html";
}

function topicHubUrl(kind) {
  return "/" + topicFolder(kind) + "/";
}

function passageChipKey(bookSlug, chapter, verseStart, verseEnd) {
  return bookSlug + "/" + chapter + "/" + verseFileStem(verseStart, verseEnd);
}

function shouldSkipChips(data) {
  if (String(data.bookSlug) === "genesis" && Number(data.chapter) === 1) return true;
  if (String(data.bookSlug) === "genesis" && Number(data.chapter) === 2) {
    const start = Number(data.verseStart);
    const end = Number(data.verseEnd ?? data.verseStart);
    if (start === 1 && end <= 3) return true;
  }
  return CHIP_SKIP_KEYS.has(
    passageChipKey(data.bookSlug, data.chapter, data.verseStart, data.verseEnd)
  );
}

function primaryNavHtml(opts) {
  const extra = opts && opts.extra ? opts.extra : "";
  return (
    '        <a href="/index.html">Home</a>\n' +
    '        <a href="/bible/">Bible</a>\n' +
    '        <a href="/doctrines/">Doctrines</a>\n' +
    '        <a href="/index.html#perspectives">Perspectives</a>\n' +
    extra +
    '        <a href="/bible/" class="btn btn-primary btn-nav nav-cta">Browse Bible</a>'
  );
}

function footerNavHtml() {
  return (
    '          <a href="/index.html">Home</a>\n' +
    '          <a href="/bible/">Bible</a>\n' +
    '          <a href="/doctrines/">Doctrines</a>\n' +
    '          <a href="/index.html#perspectives">Perspectives</a>\n' +
    '          <a href="mailto:info.got.theology@gmail.com">Contact</a>\n' +
    '          <a href="/privacy.html">Privacy</a>\n' +
    '          <a href="https://x.com/got_theology" target="_blank" rel="noopener noreferrer me">@got_theology</a>\n' +
    '          <a href="/index.html#updates">Updates</a>'
  );
}

function siteDisclaimerHtml() {
  return `<strong>About these notes.</strong>
        Commentary here is pastoral and educational. It is not a substitute for reading
        primary sources, confessions, or trusted teachers in either tradition. Both Arminian and
        Reformed families contain internal diversity (Wesleyan, classical Remonstrant, confessional
        Calvinist, and more). GotTheology aims for fair representation\u2014not a final verdict.`;
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
          <div class="voices-panel">
            <div class="voices-intro">
              <p class="voices-pill">Historic quotes</p>
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
  const chipsHtml = renderTopicChips(opts.topicChips);
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
  <meta property="og:image" content="${SITE_ORIGIN}/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="Got-Theology.com — Arminian and Reformed, side by side" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="${SITE_ORIGIN}/og-image.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/gottheology.css" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7106052656127997" crossorigin="anonymous"></script>
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
${primaryNavHtml({ extra: opts.voices ? '        <a href="#voices">Voices</a>\n' : "" })}
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
          ${opts.voices ? `<span aria-hidden="true">\u00b7</span>
          <a class="voices-jump" href="#voices">Voices</a>` : ""}
        </div>
        ${context ? `<p class="passage-context">${escapeHtml(context)}</p>` : ""}
      </div>
    </header>

    <div class="reader verse-list">
${verseCards}

      <aside class="ad-slot ad-slot-narrow" aria-label="Advertisement">
        <span class="ad-label">Advertisement</span>
        <div class="ad-frame ad-frame--leader">
          <ins class="adsbygoogle"
               style="display:block"
               data-ad-client="ca-pub-7106052656127997"
               data-ad-format="auto"
               data-full-width-responsive="true"></ins>
        </div>
      </aside>
      <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>

      <aside class="disclaimer" role="note">
        ${displayDisclaimer}
      </aside>
    </div>
${chipsHtml}
${voicesHtml}

      <aside class="ad-slot ad-slot-narrow" aria-label="Advertisement">
        <span class="ad-label">Advertisement</span>
        <div class="ad-frame ad-frame--rect">
          <ins class="adsbygoogle"
               style="display:block"
               data-ad-client="ca-pub-7106052656127997"
               data-ad-format="auto"
               data-full-width-responsive="true"></ins>
        </div>
      </aside>
      <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>

    <section class="bottom-cta" aria-labelledby="cta-heading">
      <div class="reader">
        <div class="cta-box">
          <p class="eyebrow" style="color: var(--gold-soft);">Keep reading</p>
          <h2 id="cta-heading">Genesis, Isaiah, Daniel, Matthew, John, Romans, Ephesians, Colossians, 1–2 Timothy, Titus, and 1–3 John are live</h2>
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
${footerNavHtml()}
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

function groupPassagesBySlug(passages) {
  const bySlug = new Map();
  for (const p of passages) {
    const key = p.bookSlug || String(p.book || "").toLowerCase().replace(/\s+/g, "-");
    if (!bySlug.has(key)) bySlug.set(key, []);
    bySlug.get(key).push(p);
  }
  for (const items of bySlug.values()) {
    items.sort((a, b) => {
      if (a.chapter !== b.chapter) return a.chapter - b.chapter;
      return (a.verseStart || 0) - (b.verseStart || 0);
    });
  }
  return bySlug;
}

function groupByChapter(items) {
  const byChapter = new Map();
  for (const item of items) {
    const ch = Number(item.chapter);
    if (!byChapter.has(ch)) byChapter.set(ch, []);
    byChapter.get(ch).push(item);
  }
  return byChapter;
}

function bookHubPath(slug) {
  return "/bible/" + slug + "/";
}

function chapterHubPath(slug, chapter) {
  return "/bible/" + slug + "/" + chapter + "/";
}

function navToggleScript() {
  return [
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
  ].join("\n");
}

function renderTopicChips(chips) {
  if (!chips || !chips.length) return "";
  const items = chips
    .slice(0, 3)
    .map((c) => {
      const href = topicUrl(c.kind, c.slug);
      const kindLabel = c.kind === "attribute" ? "Attribute" : "Doctrine";
      return (
        '<a class="topic-chip topic-chip--' +
        escapeHtml(c.kind) +
        '" href="' +
        escapeHtml(href) +
        '"><span class="topic-chip-kind">' +
        kindLabel +
        "</span>" +
        escapeHtml(c.title) +
        "</a>"
      );
    })
    .join("\n          ");
  return `
    <div class="reader">
      <nav class="topic-chips" aria-label="Related doctrines and attributes">
        <p class="topic-chips-label">Related</p>
        <div class="topic-chips-row">
          ${items}
        </div>
      </nav>
    </div>`;
}

function sortTopics(list, order) {
  const idx = new Map(order.map((s, i) => [s, i]));
  return list.slice().sort((a, b) => {
    const d = (idx.has(a.slug) ? idx.get(a.slug) : 99) - (idx.has(b.slug) ? idx.get(b.slug) : 99);
    if (d !== 0) return d;
    return String(a.slug).localeCompare(String(b.slug));
  });
}

function validateTopic(data, relPath) {
  const errors = [];
  if (data.kind !== "doctrine" && data.kind !== "attribute") errors.push("kind must be doctrine or attribute");
  if (!data.slug) errors.push("missing slug");
  if (!data.title) errors.push("missing title");
  if (!data.summary) errors.push("missing summary");
  if (errors.length) throw new Error(relPath + ": " + errors.join("; "));
}

function loadTopicDir(dir, expectedKind) {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const name of fs.readdirSync(dir).sort()) {
    if (!name.endsWith(".json")) continue;
    const full = path.join(dir, name);
    const rel = path.relative(ROOT, full);
    let data;
    try {
      data = JSON.parse(fs.readFileSync(full, "utf8"));
    } catch (err) {
      throw new Error(rel + ": invalid JSON (" + err.message + ")");
    }
    if (!data.kind) data.kind = expectedKind;
    if (!data.slug) data.slug = path.basename(name, ".json");
    validateTopic(data, rel);
    if (data.kind !== expectedKind) {
      throw new Error(rel + ": kind " + data.kind + " does not match folder " + expectedKind);
    }
    out.push(data);
  }
  return out;
}

function loadTopics() {
  const doctrines = sortTopics(loadTopicDir(DOCTRINES_DIR, "doctrine"), DOCTRINE_ORDER);
  const attributes = sortTopics(loadTopicDir(ATTRIBUTES_DIR, "attribute"), ATTRIBUTE_ORDER);
  return { doctrines, attributes, all: doctrines.concat(attributes) };
}

function liveHrefSet(passages) {
  return new Set(passages.map((p) => p.url));
}

function filterLiveScripture(scripture, live) {
  return (scripture || []).filter((s) => s && s.href && live.has(s.href));
}

function buildChipIndex(topics) {
  const map = new Map();
  for (const t of topics) {
    for (const s of t.scripture || []) {
      if (!s || !s.bookSlug || s.chapter == null) continue;
      const key = passageChipKey(s.bookSlug, s.chapter, s.verseStart, s.verseEnd);
      if (!map.has(key)) map.set(key, []);
      const list = map.get(key);
      if (list.length >= 3) continue;
      if (list.some((c) => c.kind === t.kind && c.slug === t.slug)) continue;
      list.push({ kind: t.kind, slug: t.slug, title: t.title });
    }
  }
  return map;
}

function chipsForPassage(data, chipIndex) {
  if (shouldSkipChips(data)) return [];
  const key = passageChipKey(data.bookSlug, data.chapter, data.verseStart, data.verseEnd);
  return (chipIndex.get(key) || []).slice(0, 3);
}

function renderScriptureList(items) {
  if (!items || !items.length) return "";
  const lis = items
    .map((s) => {
      const range = enDashRange(s.verseStart, s.verseEnd);
      const label = (s.title || s.book + " " + s.chapter + ":" + range).trim();
      const why = s.why ? '<span class="meta">' + escapeHtml(s.why) + "</span>" : "";
      return (
        '<li><a href="' +
        escapeHtml(s.href) +
        '"><span class="ref">' +
        escapeHtml(label) +
        "</span>" +
        why +
        "</a></li>"
      );
    })
    .join("\n            ");
  return (
    '      <section class="topic-scripture" aria-labelledby="scripture-heading">\n' +
    '        <h2 id="scripture-heading">Start with the verses</h2>\n' +
    '        <ul class="passage-list">\n            ' +
    lis +
    "\n        </ul>\n" +
    "      </section>"
  );
}

function renderTopicPage(data, opts) {
  const kind = data.kind;
  const kindLabel = kind === "attribute" ? "Attribute of God" : "Doctrine";
  const pageTitle = data.title;
  const desc = truncate(
    (data.summary || "") + (data.context ? " " + data.context : ""),
    160
  );
  const voices = data.showVoices === false ? null : data.voices || opts.siteVoices || null;
  const voicesHtml = voices ? renderVoicesSection(voices) : "";
  const scriptureHtml = renderScriptureList(opts.scripture || []);
  const contrast = data.keyContrast
    ? `
        <p class="key-contrast">
          <strong>Key contrast</strong>
          ${escapeHtml(data.keyContrast)}
        </p>`
    : "";
  const canonicalPath = topicUrl(kind, data.slug);
  const canonical = absoluteUrl(canonicalPath);
  const otherHub = kind === "attribute" ? topicHubUrl("doctrine") : topicHubUrl("attribute");
  const otherLabel = kind === "attribute" ? "Doctrines" : "Attributes of God";
  const hub = topicHubUrl(kind);
  const hubLabel = kind === "attribute" ? "Attributes" : "Doctrines";
  const ogTitle = pageTitle + " \u2014 GotTheology";

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <title>${escapeHtml(pageTitle)} \u2014 GotTheology</title>
  <meta name="description" content="${escapeHtml(desc)}" />
  <link rel="canonical" href="${escapeHtml(canonical)}" />
  <meta property="og:title" content="${escapeHtml(ogTitle)}" />
  <meta property="og:description" content="${escapeHtml(desc)}" />
  <meta property="og:url" content="${escapeHtml(canonical)}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="GotTheology" />
  <meta property="og:image" content="${SITE_ORIGIN}/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="Got-Theology.com — Arminian and Reformed, side by side" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="${SITE_ORIGIN}/og-image.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/gottheology.css" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7106052656127997" crossorigin="anonymous"></script>
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
${primaryNavHtml({ extra: voices ? '        <a href="#voices">Voices</a>\n' : "" })}
      </nav>
    </div>
  </header>

  <main class="topic-page">
    <header class="passage-header">
      <div class="reader">
        <p class="browse-crumbs"><a href="${escapeHtml(hub)}">${escapeHtml(hubLabel)}</a></p>
        <p class="eyebrow">${escapeHtml(kindLabel)}</p>
        <h1>${escapeHtml(pageTitle)}</h1>
        ${data.summary ? `<p class="topic-summary">${escapeHtml(data.summary)}</p>` : ""}
        ${data.context ? `<p class="passage-context">${escapeHtml(data.context)}</p>` : ""}
      </div>
    </header>

    <div class="reader verse-list">
${scriptureHtml}

      <article class="verse-card topic-notes">
        <div class="dual-cols">
          <div class="dual-col">
            <span class="dual-label label-arminian">Arminian</span>
            ${paragraphsHtml(data.arminianNotes)}
          </div>
          <div class="dual-col">
            <span class="dual-label label-reformed">Reformed</span>
            ${paragraphsHtml(data.reformedNotes)}
          </div>
        </div>${contrast}
      </article>

      <aside class="disclaimer" role="note">
        ${siteDisclaimerHtml()}
      </aside>
    </div>
${voicesHtml}

    <section class="bottom-cta" aria-labelledby="cta-heading">
      <div class="reader">
        <div class="cta-box">
          <p class="eyebrow" style="color: var(--gold-soft);">Keep reading</p>
          <h2 id="cta-heading">The verses stay first</h2>
          <p>Open the passages above, or browse ${escapeHtml(otherLabel.toLowerCase())} beside these notes.</p>
          <a href="/bible/" class="btn btn-gold">Browse the Bible</a>
          <a href="${escapeHtml(otherHub)}" class="btn btn-primary" style="margin-left:0.5rem">${escapeHtml(otherLabel)}</a>
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
${footerNavHtml()}
        </nav>
      </div>
      <div class="footer-bottom">
        <span>\u00a9 ${YEAR} Got-Theology.com. All rights reserved.</span>
        <span>${escapeHtml(pageTitle)}</span>
      </div>
    </div>
  </footer>

${navToggleScript()}
</body>
</html>
`;
}

function renderTopicHub(kind, items, otherItems) {
  const isAttr = kind === "attribute";
  const title = isAttr ? "Attributes of God" : "Doctrines";
  const hubPath = topicHubUrl(kind);
  const otherPath = topicHubUrl(isAttr ? "doctrine" : "attribute");
  const otherTitle = isAttr ? "Doctrines" : "Attributes of God";
  const intro = isAttr
    ? "Who God is\u2014holy, loving, sovereign\u2014read first in the verses, then in Arminian and Reformed notes side by side."
    : "Election, atonement, justification, regeneration, perseverance\u2014read first in the verses, then in Arminian and Reformed notes side by side.";
  const cards = items
    .map((t) => {
      return (
        '<li><a href="' +
        escapeHtml(topicUrl(t.kind, t.slug)) +
        '"><span class="ref">' +
        escapeHtml(t.title) +
        '</span><span class="meta">' +
        escapeHtml(t.summary || "") +
        "</span></a></li>"
      );
    })
    .join("\n            ");
  const otherLine =
    '<p class="topic-hub-alt">Also: <a href="' +
    escapeHtml(otherPath) +
    '">' +
    escapeHtml(otherTitle) +
    "</a> \u00b7 <a href=\"/bible/\">Bible</a></p>";

  const body =
    '    <div class="reader">\n' +
    '      <p class="browse-crumbs"><a href="/bible/">Bible</a></p>\n' +
    '      <div class="page-intro page-intro--hub">\n' +
    '        <p class="eyebrow">Verse-first</p>\n' +
    "        <h1>" +
    escapeHtml(title) +
    "</h1>\n" +
    "        <p>" +
    escapeHtml(intro) +
    "</p>\n" +
    "      </div>\n" +
    otherLine +
    '\n      <ul class="passage-list topic-hub-list">\n            ' +
    cards +
    "\n      </ul>\n" +
    "    </div>";

  return renderBrowseDocument({
    title,
    description: intro,
    canonicalPath: hubPath,
    mainClass: "bible-index topic-hub",
    footerLabel: title,
    body,
  });
}

function cleanGeneratedTopicTrees() {
  for (const dir of [DOCTRINES_OUT, ATTRIBUTES_OUT]) {
    if (fs.existsSync(dir)) fs.rmSync(dir, { recursive: true, force: true });
    ensureDir(dir);
  }
}

function writeTopics(topics, passages) {
  const live = liveHrefSet(passages);
  const siteVoices = loadVoicesDefault();
  let pageCount = 0;
  for (const t of topics.all) {
    const scripture = filterLiveScripture(t.scripture, live);
    const html = renderTopicPage(t, { scripture, siteVoices });
    const outPath = path.join(PUBLIC, topicUrl(t.kind, t.slug).replace(/^\//, ""));
    ensureDir(path.dirname(outPath));
    fs.writeFileSync(outPath, html, "utf8");
    console.log("  wrote " + path.relative(ROOT, outPath));
    pageCount += 1;
  }
  const docHub = path.join(DOCTRINES_OUT, "index.html");
  fs.writeFileSync(docHub, renderTopicHub("doctrine", topics.doctrines, topics.attributes), "utf8");
  console.log("  wrote " + path.relative(ROOT, docHub));
  const attrHub = path.join(ATTRIBUTES_OUT, "index.html");
  fs.writeFileSync(attrHub, renderTopicHub("attribute", topics.attributes, topics.doctrines), "utf8");
  console.log("  wrote " + path.relative(ROOT, attrHub));
  return { pageCount, hubCount: 2, chipIndex: buildChipIndex(topics.all) };
}

function topicSearchEntries(topics) {
  return topics.all.map((t) => {
    const title = t.title;
    const summary = t.summary || "";
    return {
      kind: t.kind,
      book: t.kind === "attribute" ? "Attributes" : "Doctrines",
      bookSlug: t.kind,
      chapter: 0,
      verseStart: 0,
      verseEnd: 0,
      title,
      context: summary,
      url: topicUrl(t.kind, t.slug),
      text: [title, summary, t.context || "", t.keyContrast || ""].join(" ").replace(/\s+/g, " ").trim(),
    };
  });
}


function renderBrowseDocument(opts) {
  const title = opts.title;
  const desc = opts.description;
  const canonical = absoluteUrl(opts.canonicalPath);
  const extraScripts = opts.extraScripts || [];
  const footerLabel = opts.footerLabel || "";
  const mainClass = opts.mainClass || "bible-index";
  const ogTitle = title + " \u2014 GotTheology";

  const parts = [
    "<!DOCTYPE html>",
    '<html lang="en">',
    "<head>",
    '  <meta charset="UTF-8" />',
    '  <meta name="viewport" content="width=device-width, initial-scale=1.0" />',
    '  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />',
    "  <title>" + escapeHtml(title) + " \u2014 GotTheology</title>",
    '  <meta name="description" content="' + escapeHtml(desc) + '" />',
    '  <link rel="canonical" href="' + escapeHtml(canonical) + '" />',
    '  <meta property="og:title" content="' + escapeHtml(ogTitle) + '" />',
    '  <meta property="og:description" content="' + escapeHtml(desc) + '" />',
    '  <meta property="og:url" content="' + escapeHtml(canonical) + '" />',
    '  <meta property="og:type" content="website" />',
    '  <meta property="og:site_name" content="GotTheology" />',
    '  <meta property="og:image" content="' + SITE_ORIGIN + '/og-image.png" />',
    '  <meta property="og:image:width" content="1200" />',
    '  <meta property="og:image:height" content="630" />',
    '  <meta property="og:image:alt" content="Got-Theology.com — Arminian and Reformed, side by side" />',
    '  <meta name="twitter:card" content="summary_large_image" />',
    '  <meta name="twitter:image" content="' + SITE_ORIGIN + '/og-image.png" />',
    '  <link rel="preconnect" href="https://fonts.googleapis.com" />',
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />',
    '  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet" />',
    '  <link rel="stylesheet" href="/assets/gottheology.css" />',
    '  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7106052656127997" crossorigin="anonymous"></script>',
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
    primaryNavHtml({ extra: opts.navExtra || "" }),
    "      </nav>",
    "    </div>",
    "  </header>",
    '  <main class="' + mainClass + '">',
    opts.body,
    "  </main>",
    '  <footer class="site-footer">',
    '    <div class="container">',
    '      <div class="footer-inner">',
    '        <div class="footer-brand">',
    '          <a href="/index.html" class="wordmark">Got<span>-Theology</span>.com</a>',
    "          <p>Verse-by-verse theology from the Bible\u2014Arminian and Reformed, side by side. Free to read, supported by ads.</p>",
    "        </div>",
    '        <nav class="footer-links" aria-label="Footer">',
    footerNavHtml(),
    "        </nav>",
    "      </div>",
    '      <div class="footer-bottom">',
    "        <span>\u00a9 " + YEAR + " Got-Theology.com. All rights reserved.</span>",
    "        <span>" + escapeHtml(footerLabel) + "</span>",
    "      </div>",
    "    </div>",
    "  </footer>",
    navToggleScript(),
  ];
  if (extraScripts.length) parts.push(extraScripts.join("\n"));
  parts.push("</body>", "</html>", "");
  return parts.join("\n");
}

function renderPassageListItems(items) {
  return items
    .map((item) => {
      const range = enDashRange(item.verseStart, item.verseEnd);
      const label = item.chapter + ":" + range;
      const meta = [item.translation, item.context ? truncate(item.context, 90) : null]
        .filter(Boolean)
        .join(" \u00b7 ");
      const metaHtml = meta ? '<span class="meta">' + escapeHtml(meta) + "</span>" : "";
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
    .join("\n            ");
}

function renderBibleIndex(passages) {
  const bySlug = groupPassagesBySlug(passages);

  function renderBookTile(book) {
    const items = bySlug.get(book.slug) || [];
    const live = items.length > 0;
    if (live) {
      return (
        '<a class="book-tile book-tile--live" href="' +
        escapeHtml(bookHubPath(book.slug)) +
        '">' +
        escapeHtml(book.name) +
        "</a>"
      );
    }
    return (
      '<span class="book-tile book-tile--soon">' +
      '<span class="book-tile-name">' +
      escapeHtml(book.name) +
      '</span><span class="book-tile-status">Coming</span></span>'
    );
  }

  function renderTestament(id, title, books) {
    const tiles = books.map(renderBookTile).join("\n          ");
    return (
      '<section class="testament" id="' +
      id +
      '" aria-labelledby="' +
      id +
      '-heading">\n        <h2 class="testament-heading" id="' +
      id +
      '-heading">' +
      escapeHtml(title) +
      '</h2>\n        <div class="book-grid">\n          ' +
      tiles +
      "\n        </div>\n      </section>"
    );
  }

  const ot = CANONICAL_BOOKS.filter((b) => b.testament === "ot");
  const nt = CANONICAL_BOOKS.filter((b) => b.testament === "nt");
  const catalog =
    '      <nav class="canon-jump" aria-label="Testament">\n' +
    '        <a href="#old-testament">Old Testament</a>\n' +
    '        <a href="#new-testament">New Testament</a>\n' +
    "      </nav>\n      " +
    renderTestament("old-testament", "Old Testament", ot) +
    "\n      " +
    renderTestament("new-testament", "New Testament", nt);

  const body =
    '    <div class="reader">\n' +
    '      <div class="page-intro">\n' +
    '        <p class="eyebrow">Free to read</p>\n' +
    "        <h1>Browse the Bible</h1>\n" +
    "        <p>Search any live verse, or pick a book. Arminian and Reformed notes sit side by side, plus historic quotes from both camps\u2014supported by ads, never paywalled.</p>\n" +
    "      </div>\n" +
    '      <div class="search-panel" data-search-panel>\n' +
    '        <label class="search-label" for="siteSearch">Search any live verse</label>\n' +
    '        <div class="search-field">\n' +
    '          <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>\n' +
    '          <input type="search" id="siteSearch" name="q" data-search-input placeholder="Book, chapter:verse, or wording\u2026" autocomplete="off" enterkeyhint="search" />\n' +
    "        </div>\n" +
    '        <div class="search-results" data-search-results hidden></div>\n' +
    "      </div>\n" +
    "    </div>\n" +
    '    <div class="container catalog-wrap" data-search-catalog>\n' +
    catalog +
    "\n    </div>";

  return renderBrowseDocument({
    title: "Bible Index",
    description: "Browse free verse-by-verse Arminian and Reformed commentary on GotTheology.",
    canonicalPath: "/bible/",
    mainClass: "bible-index",
    footerLabel: "Bible index",
    extraScripts: ['  <script src="/assets/search.js" defer></script>'],
    body,
  });
}

function renderBookHub(book, items) {
  const byChapter = groupByChapter(items);
  const chapters = [...byChapter.keys()];
  const jump = chapters
    .map((ch) => {
      return '<a href="' + escapeHtml(chapterHubPath(book.slug, ch)) + '">' + ch + "</a>";
    })
    .join("\n          ");

  const body =
    '    <div class="reader">\n' +
    '      <p class="browse-crumbs"><a href="/bible/index.html">Bible</a></p>\n' +
    '      <div class="page-intro page-intro--hub">\n' +
    '        <p class="eyebrow">Book</p>\n' +
    "        <h1>" +
    escapeHtml(book.name) +
    "</h1>\n" +
    "        <p>Chapters with notes. Pick a chapter\u2014Arminian and Reformed, side by side.</p>\n" +
    "      </div>\n" +
    '      <nav class="chapter-jump" aria-label="' +
    escapeHtml(book.name) +
    ' chapters">\n          ' +
    jump +
    "\n      </nav>\n" +
    "    </div>";

  return renderBrowseDocument({
    title: book.name,
    description:
      "Browse " + book.name + " chapter by chapter. Arminian and Reformed commentary on GotTheology.",
    canonicalPath: bookHubPath(book.slug),
    mainClass: "bible-index book-hub",
    footerLabel: book.name,
    body,
  });
}

function renderChapterHub(book, chapter, items) {
  const lis = renderPassageListItems(items);
  const body =
    '    <div class="reader">\n' +
    '      <p class="browse-crumbs"><a href="/bible/index.html">Bible</a> \u00b7 <a href="' +
    escapeHtml(bookHubPath(book.slug)) +
    '">' +
    escapeHtml(book.name) +
    "</a></p>\n" +
    '      <div class="page-intro page-intro--hub">\n' +
    '        <p class="eyebrow">Chapter</p>\n' +
    "        <h1>" +
    escapeHtml(book.name) +
    " " +
    escapeHtml(chapter) +
    "</h1>\n" +
    "      </div>\n" +
    '      <ul class="passage-list">\n            ' +
    lis +
    "\n      </ul>\n" +
    "    </div>";

  const label = book.name + " " + chapter;
  return renderBrowseDocument({
    title: label,
    description:
      "Passages in " +
      label +
      ". Verse-by-verse Arminian and Reformed commentary on GotTheology.",
    canonicalPath: chapterHubPath(book.slug, chapter),
    mainClass: "bible-index chapter-hub",
    footerLabel: label,
    body,
  });
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

function writeSitemap(passages, topics) {
  const bySlug = groupPassagesBySlug(passages);
  const urls = ["/", "/bible/", "/doctrines/", "/attributes/"];
  for (const book of CANONICAL_BOOKS) {
    const items = bySlug.get(book.slug);
    if (!items || !items.length) continue;
    urls.push(bookHubPath(book.slug));
    const byChapter = groupByChapter(items);
    for (const ch of byChapter.keys()) {
      urls.push(chapterHubPath(book.slug, ch));
    }
  }
  for (const p of passages) urls.push(p.url);
  if (topics && topics.all) {
    for (const t of topics.all) urls.push(topicUrl(t.kind, t.slug));
  }

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

function writeBookAndChapterHubs(passages) {
  const bySlug = groupPassagesBySlug(passages);
  let bookCount = 0;
  let chapterCount = 0;
  for (const book of CANONICAL_BOOKS) {
    const items = bySlug.get(book.slug);
    if (!items || !items.length) continue;

    const hubPath = path.join(BIBLE_OUT, book.slug, "index.html");
    ensureDir(path.dirname(hubPath));
    fs.writeFileSync(hubPath, renderBookHub(book, items), "utf8");
    console.log("  wrote " + path.relative(ROOT, hubPath));
    bookCount += 1;

    const byChapter = groupByChapter(items);
    for (const [ch, chItems] of byChapter) {
      const chPath = path.join(BIBLE_OUT, book.slug, String(ch), "index.html");
      ensureDir(path.dirname(chPath));
      fs.writeFileSync(chPath, renderChapterHub(book, ch, chItems), "utf8");
      console.log("  wrote " + path.relative(ROOT, chPath));
      chapterCount += 1;
    }
  }
  return { bookCount, chapterCount };
}

function main() {
  ensureDir(path.join(PUBLIC, "assets"));
  if (!fs.existsSync(path.join(PUBLIC, "assets", "gottheology.css"))) {
    console.warn("Warning: public/assets/gottheology.css missing.");
  }

  cleanGeneratedBibleTree();
  cleanGeneratedTopicTrees();

  const siteVoices = loadVoicesDefault();
  const topics = loadTopics();
  const chipIndex = buildChipIndex(topics.all);
  let chipPassages = 0;
  let chipTotal = 0;
  let chipPassagesApplied = 0;
  let chipLinksApplied = 0;
  for (const list of chipIndex.values()) {
    chipPassages += 1;
    chipTotal += list.length;
  }
  console.log(
    "Loaded " +
      topics.doctrines.length +
      " doctrine(s) + " +
      topics.attributes.length +
      " attribute(s); chip map covers " +
      chipPassages +
      " passage(s) (" +
      chipTotal +
      " chip links before skip)."
  );

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

    const topicChips = chipsForPassage(data, chipIndex);
    if (topicChips.length) {
      chipPassagesApplied += 1;
      chipLinksApplied += topicChips.length;
    }
    const html = renderPassagePage(data, { voices, canonicalPath: url, topicChips });
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

  const hubs = writeBookAndChapterHubs(passages);

  const topicStats = writeTopics(topics, passages);

  const searchIndexPath = path.join(PUBLIC, "assets", "search-index.json");
  const searchIndex = passages
    .map((p) => ({
      kind: "passage",
      book: p.book,
      bookSlug: p.bookSlug,
      chapter: p.chapter,
      verseStart: p.verseStart,
      verseEnd: p.verseEnd,
      title: p.title,
      context: p.context,
      url: p.url,
      text: p.text,
    }))
    .concat(topicSearchEntries(topics));
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
  writeSitemap(passages, topics);

  console.log(
    "Done. " +
      passages.length +
      " passage page(s) + bible index + " +
      hubs.bookCount +
      " book hub(s) + " +
      hubs.chapterCount +
      " chapter hub(s) + " +
      topicStats.pageCount +
      " topic page(s) + " +
      topicStats.hubCount +
      " topic hub(s) + " +
      chipLinksApplied +
      " chip link(s) on " +
      chipPassagesApplied +
      " passage(s) + search index + SEO files."
  );
}

try {
  main();
} catch (err) {
  console.error("Build failed:", err.message || err);
  process.exit(1);
}
