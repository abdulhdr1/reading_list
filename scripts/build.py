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
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{
  --bg: #f7f5f2; --fg: #1a1a1a; --fg2: #8a8578;
  --fg3: #b5ae9e; --border: #e5e2dc; --pill-bg: #eae7e1; --pill-fg: #6b6560;
}}
[data-theme="dark"] {{
  --bg: #1a1917; --fg: #e8e6e2; --fg2: #8a8578;
  --fg3: #5a5650; --border: #2e2c28; --pill-bg: #2e2c28; --pill-fg: #a09a90;
}}
body {{
  background: var(--bg); color: var(--fg);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  line-height: 1.7; transition: background .3s, color .3s;
  -webkit-font-smoothing: antialiased;
}}
.container {{ max-width: 680px; margin: 0 auto; padding: 100px 24px 140px; }}
.back {{
  color: var(--fg2); text-decoration: none; font-size: 0.85rem;
  display: inline-block; margin-bottom: 48px; transition: opacity .2s;
  letter-spacing: 0.03em;
}}
.back:hover {{ opacity: 0.5; }}
h1 {{
  font-family: 'Playfair Display', Georgia, serif; font-size: 2.8rem;
  font-weight: 900; letter-spacing: -0.03em; line-height: 1.1; margin-bottom: 16px;
}}
.date {{ color: var(--fg2); font-size: 0.82rem; margin-bottom: 28px; letter-spacing: 0.03em; }}
.visit {{
  display: inline-block; padding: 10px 24px; border: 1.5px solid var(--border);
  border-radius: 24px; color: var(--fg); text-decoration: none; font-size: 0.88rem;
  margin-bottom: 40px; transition: all .2s; letter-spacing: 0.02em;
}}
.visit:hover {{ background: var(--pill-bg); border-color: var(--fg3); }}
.summary {{
  color: var(--fg); font-size: 1.05rem; line-height: 1.8; margin-bottom: 40px;
  font-family: 'Inter', -apple-system, sans-serif;
}}
.divider {{
  width: 40px; height: 1.5px; background: var(--border); margin-bottom: 24px;
}}
.tags {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.pill {{
  background: var(--pill-bg); color: var(--pill-fg);
  font-size: 0.7rem; font-family: 'Inter', sans-serif; font-weight: 500;
  padding: 4px 12px; border-radius: 14px; white-space: nowrap;
  text-decoration: none; transition: all .2s; letter-spacing: 0.02em;
}}
.pill:hover {{ background: var(--fg); color: var(--bg); }}
.theme-toggle {{
  position: fixed; top: 24px; right: 24px; background: none; border: none;
  font-size: 1.3rem; cursor: pointer; opacity: 0.4; transition: opacity .2s; z-index: 10;
}}
.theme-toggle:hover {{ opacity: 1; }}
@media (max-width: 480px) {{ .container {{ padding: 60px 20px 100px; }} h1 {{ font-size: 2rem; }} }}
</style>
</head>
<body>
<button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">☀️</button>
<div class="container">
  <a class="back" href="../index.html">← Back to list</a>
  <h1>{title}</h1>
  <div class="date">{date}</div>
  <a class="visit" href="{url}" target="_blank" rel="noopener">Visit original ↗</a>
  <p class="summary">{summary}</p>
  <div class="divider"></div>
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
