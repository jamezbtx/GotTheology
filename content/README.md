# Content conventions

Authors edit JSON under content/books/. Generated HTML lands in public/bible/.
See schema.json for the passage shape. Seed: books/ephesians/1/3-6.json.

## Layout

```
content/
  books/<book-slug>/<chapter>/<verse-range>.json
  voices.json
  schema.json
```

Filename stem becomes the URL stem: `3-6.json` maps to `/bible/ephesians/1/3-6.html`.

## How to add a passage

1. Create `content/books/<bookSlug>/<chapter>/<range>.json` (copy the Ephesians seed).
2. Fill required fields: `book`, `bookSlug`, `chapter`, `verses[]`.
3. Run the project build script from the repo root (`package.json` -> `build`).
4. Confirm the page under `public/bible/...`.
5. Commit the JSON (and generated HTML if you version `public/`).

## Required fields

- `book` (string), `bookSlug` (string), `chapter` (number), `verses` (non-empty array)
- Each verse: `number`, `text`, `arminianNotes`, `reformedNotes`; optional `keyContrast`

## Optional

`verseStart`, `verseEnd`, `translation`, `title`, `context`, `description`, `eyebrow`, `disclaimer`, `showVoices`, `voices`

## Output URLs

- `/bible/<bookSlug>/<chapter>/<start>-<end>.html` (or single number)
- `/bible/index.html`
- `public/verse.html` alias for Ephesians 1:3-6
- `/assets/gottheology.css`


## Doctrines and attributes

Hub JSON lives beside the books tree:

    content/doctrines/<slug>.json   ->  /doctrines/<slug>.html
    content/attributes/<slug>.json  ->  /attributes/<slug>.html
    /doctrines/   and  /attributes/ hubs

Required: kind, slug, title, summary. Typical fields match the first-wave files: context, showVoices, voices, arminianNotes, reformedNotes, keyContrast, scripture[].

Each scripture item: book, bookSlug, chapter, verseStart, verseEnd, title, href (/bible/<bookSlug>/<ch>/<start>-<end>.html), why. The builder drops hrefs that are not live.

Passage chips (max 3) are derived from those scripture lists during the project build. Greetings, Genesis 1 creation-day pages, and Titus 2:9-10 are never chipped.
