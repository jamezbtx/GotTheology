# GotTheology

> **Canonical deploy root:** `public/` (root `index.html` / `verse.html` are prototype copies kept for now).

Free verse-by-verse Arminian + Reformed theology, side by side—ad-supported, never paywalled.

## Local

```bash
cd gottheology
npm start
# → http://localhost:4173
```

`nmp run build` is a no-op; the site is already static under `public/`.

## Deploy

Connect this repo to **Netlify** or **Vercel**. Set the publish / output directory to **`public/`**. No build command is required (Netlify `netlify.toml` already sets `publish = "public"`).

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
- Content pipeline: author JSON under `content/`, generate HTML pages from it
