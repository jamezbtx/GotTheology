# Content conventions

Future verse pages will be generated from structured files in this tree—not hand-edited HTML forever.

## Layout

```
content/
  books/
    <book-slug>/        # e.g. ephesians, romans
      <chapter>/          # e.g. 1, 2
        <verse-range>.json  # e.g. 3-6.json, 1.json
```

- **One folder per book** (lowercase slug).
- **One folder per chapter** (numeric).
- **One JSON file per verse range** (or single verse) that a reader page will cover.

## JSON shape (seed)

See `books/ephesians/1/3-6.json` for the sample. Expected fields:

- Passage metadata: `book`, `chapter`, `verseStart`, `verseEnd`, `translation`, `title`, `context`
- `verses[]`: each with `number`, `text`, `arminianNotes`, `reformedNotes`, optional `keyContrast`

Pages under `public/` are the current prototypes; the long-term path is generate HTML (or hydrate a template) from these files.
