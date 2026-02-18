# reading list

things i've read that stuck with me.

→ [abdulhdr1.github.io/reading_list](https://abdulhdr1.github.io/reading_list/)

---

a personal collection of articles, tweets, essays, and videos about building things, startups, engineering, design, and whatever else catches my attention.

not everything here is something i agree with. some of it changed how i think. some of it i just found interesting. all of it was worth the time.

## how it works

links live in [`links.md`](./links.md) as a simple markdown table. an ai agent enriches them with summaries, tags, and dedicated pages. the site is static html — no framework, no build step, just `fetch` and `parse`.

the enrichment pipeline:
- new links get added to `links.md`
- [`data/links.json`](./data/links.json) holds enriched metadata (summaries, tags)
- [`scripts/build.py`](./scripts/build.py) generates dedicated pages
- github actions deploys to pages on push

## adding links

i save links throughout the day. my agent ([openclaw](https://github.com/openclaw/openclaw)) captures them from whatsapp, processes them, and commits here automatically.

## local

```
open index.html
```

that's it. no `npm install`, no dependencies, no build.

---

*curated by [@abdulhdr1](https://x.com/abdulhdr1)*
