# GotTheology

> **Canonical deploy root:** `public/` (root `index.html` / `verse.html` are prototype copies kept for now).

Free verse-by-verse Arminian + Reformed theology, side by side—ad-supported, never paywalled.

## Local

```bash
cd gottheology
npm start
# → http://localhost:4173
```

Use the package build script to generate bible pages from `content/` into `public/bible/`.

## Deploy

Connect this repo to **Netlify** or **Vercel**. Set the publish / output directory to **`public/`**. Netlify runs the package build script and publishes `public/`.

### After GitHub auth

```bash
git init
git add .
git commit -m "Scaffold GotTheology static site"
# Push to GitHub, then:
# Netlify UI: publish directory = public  (or: netlify deploy --prod --dir=public)
# Vercel UI: Output Directory = public  (or: vercel --prod)
```

## Next steps

- Waitlist backend (email capture + confirmation)
- Ad slots / network integration
- Content pipeline: author JSON under `content/books/`, then run the build script
