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
    domain = ''
    try:
        from urllib.parse import urlparse
        domain = urlparse(item['url']).hostname.replace('www.', '')
    except:
        pass
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
<style>
*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{
  --bg: #ffffff; --text: #1a1a1a; --text-secondary: #6b6b6b;
  --border: #e8e5e1; --hover: #f5f4f2; --active-tag: #eeebe7; --badge: #c5c0b8;
}}
[data-theme="dark"] {{
  --bg: #141312; --text: #e8e6e2; --text-secondary: #8a8680;
  --border: #2a2826; --hover: #1f1e1c; --active-tag: #2a2826; --badge: #5a5650;
}}
body {{
  background: var(--bg); color: var(--text);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  line-height: 1.7; letter-spacing: -0.01em;
  -webkit-font-smoothing: antialiased;
}}
.container {{ max-width: 640px; margin: 0 auto; padding: 80px 24px 120px; }}
.back {{
  color: var(--text-secondary); text-decoration: none; font-size: 13px;
  display: inline-flex; align-items: center; gap: 6px;
  margin-bottom: 40px; transition: color 150ms;
}}
.back:hover {{ color: var(--text); }}
h1 {{
  font-size: 28px; font-weight: 600; letter-spacing: -0.02em;
  line-height: 1.2; margin-bottom: 12px;
}}
.meta {{
  display: flex; align-items: center; gap: 12px;
  color: var(--text-secondary); font-size: 13px; margin-bottom: 32px;
}}
.meta-dot {{ color: var(--badge); }}
.visit {{
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 16px; border: 1px solid var(--border); border-radius: 6px;
  color: var(--text); text-decoration: none; font-size: 13px; font-weight: 450;
  margin-bottom: 32px; transition: background 150ms, border-color 150ms;
  font-family: inherit; letter-spacing: -0.01em;
}}
.visit:hover {{ background: var(--hover); border-color: var(--badge); }}
.summary {{
  color: var(--text); font-size: 15px; line-height: 1.8; margin-bottom: 32px;
}}
.divider {{ width: 32px; height: 1px; background: var(--border); margin-bottom: 20px; }}
.tags {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.pill {{
  background: var(--hover); color: var(--text-secondary);
  font-size: 12px; font-weight: 450; padding: 4px 10px; border-radius: 4px;
  text-decoration: none; transition: background 150ms; letter-spacing: -0.01em;
}}
.pill:hover {{ background: var(--active-tag); color: var(--text); }}
.theme-toggle {{
  position: fixed; top: 20px; right: 20px; background: none; border: none;
  font-size: 14px; cursor: pointer; color: var(--text-secondary);
  opacity: 0.5; transition: opacity 150ms;
}}
.theme-toggle:hover {{ opacity: 1; }}
@media (max-width: 480px) {{
  .container {{ padding: 60px 16px 80px; }}
  h1 {{ font-size: 22px; }}
}}
</style>
</head>
<body>
<button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">☀️</button>
<div class="container">
  <a class="back" href="../index.html">← Back</a>
  <h1>{title}</h1>
  <div class="meta">
    <span>{date}</span>
    <span class="meta-dot">·</span>
    <span>{html.escape(domain)}</span>
  </div>
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
