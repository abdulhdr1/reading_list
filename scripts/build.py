#!/usr/bin/env python3
"""Generate dedicated pages for enriched links."""
import json, hashlib, os, html

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
DATA = os.path.join(ROOT, 'data', 'links.json')
PAGES = os.path.join(ROOT, 'pages')

def slug(url):
    return hashlib.md5(url.split('?')[0].encode()).hexdigest()[:10]

def build_page(item):
    s = slug(item['url'])
    title = html.escape(item['title'])
    summary = html.escape(item['summary'])
    date = html.escape(item.get('date', ''))
    url = html.escape(item['url'])
    pills = ''.join(
        f'<a class="pill" href="../index.html?tag={html.escape(t)}">{html.escape(t)}</a>'
        for t in item.get('tags', [])
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📚</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{
  --bg: #f5f5f5; --bg2: #ffffff; --fg: #111111; --fg2: #888888;
  --fg3: #aaaaaa; --border: #e0e0e0; --pill-bg: #e8e8e8; --pill-fg: #666666;
}}
[data-theme="dark"] {{
  --bg: #111111; --bg2: #1a1a1a; --fg: #e8e8e8; --fg2: #777777;
  --fg3: #555555; --border: #2a2a2a; --pill-bg: #2a2a2a; --pill-fg: #999999;
}}
body {{
  background: var(--bg); color: var(--fg);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  line-height: 1.6; transition: background .3s, color .3s;
}}
.container {{ max-width: 640px; margin: 0 auto; padding: 80px 24px 120px; }}
.back {{ color: var(--fg2); text-decoration: none; font-size: 0.9rem; display: inline-block; margin-bottom: 32px; transition: opacity .2s; }}
.back:hover {{ opacity: 0.6; }}
h1 {{
  font-family: 'Instrument Serif', Georgia, serif; font-size: 2.4rem;
  font-weight: 400; letter-spacing: -0.02em; line-height: 1.15; margin-bottom: 12px;
}}
.date {{ color: var(--fg2); font-size: 0.85rem; margin-bottom: 20px; }}
.visit {{
  display: inline-block; padding: 8px 20px; border: 1px solid var(--border);
  border-radius: 6px; color: var(--fg); text-decoration: none; font-size: 0.9rem;
  margin-bottom: 32px; transition: background .2s, border-color .2s;
}}
.visit:hover {{ background: var(--pill-bg); border-color: var(--fg3); }}
.summary {{ color: var(--fg2); font-size: 1rem; line-height: 1.7; margin-bottom: 24px; }}
.tags {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.pill {{
  background: var(--pill-bg); color: var(--pill-fg);
  font-size: 0.72rem; font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
  padding: 2px 8px; border-radius: 10px; white-space: nowrap;
  text-decoration: none; transition: background .2s, color .2s;
}}
.pill:hover {{ background: var(--fg); color: var(--bg); }}
.theme-toggle {{
  position: fixed; top: 24px; right: 24px; background: none; border: none;
  font-size: 1.3rem; cursor: pointer; opacity: 0.5; transition: opacity .2s; z-index: 10;
}}
.theme-toggle:hover {{ opacity: 1; }}
@media (max-width: 480px) {{ .container {{ padding: 48px 20px 80px; }} h1 {{ font-size: 1.8rem; }} }}
</style>
</head>
<body>
<button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">☀️</button>
<div class="container">
  <a class="back" href="../index.html">← Back</a>
  <h1>{title}</h1>
  <div class="date">{date}</div>
  <a class="visit" href="{url}" target="_blank" rel="noopener">Visit original ↗</a>
  <p class="summary">{summary}</p>
  <div class="tags">{pills}</div>
</div>
<script>
function toggleTheme() {{
  const d = document.documentElement;
  const next = d.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  d.setAttribute('data-theme', next);
  document.querySelector('.theme-toggle').textContent = next === 'dark' ? '🌙' : '☀️';
  localStorage.setItem('theme', next);
}}
(function() {{
  const saved = localStorage.getItem('theme') ||
    (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  if (saved === 'dark') {{
    document.documentElement.setAttribute('data-theme', 'dark');
    document.querySelector('.theme-toggle').textContent = '🌙';
  }}
}})();
</script>
</body>
</html>'''

def main():
    os.makedirs(PAGES, exist_ok=True)
    with open(DATA) as f:
        items = json.load(f)

    slug_map = {}
    for item in items:
        s = slug(item['url'])
        slug_map[item['url'].split('?')[0]] = s
        path = os.path.join(PAGES, f'{s}.html')
        with open(path, 'w') as f:
            f.write(build_page(item))
        print(f'  ✓ {s}.html — {item["title"][:50]}')

    with open(os.path.join(ROOT, 'data', 'slugs.json'), 'w') as f:
        json.dump(slug_map, f, indent=2)
    print(f'\nGenerated {len(items)} pages + slugs.json')

if __name__ == '__main__':
    main()
