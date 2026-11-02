#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote,urljoin
import json
import argparse
parser = argparse.ArgumentParser(description='Check rendered workrole pages, navigation, assets, redirects, and anchors.')
parser.add_argument('site_dir', type=Path, help='Jekyll build destination')
site = parser.parse_args().site_dir.resolve()
if not (site / 'index.html').is_file():
 parser.error('site_dir must contain the built index.html')
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=set();self.links=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if 'id' in attrs:self.ids.add(attrs['id'])
  for key in ('href','src'):
   if key in attrs:self.links.append((tag,attrs[key]))
pages={p:Page(p.read_text()) for p in [site/'index.html',*site.glob('workrole/*/*.html'),*site.glob('classes/*/*.html')]}
errors=[];count=0
for file,page in pages.items():
 url='https://jboyce1.github.io/ppsCTF/'+str(file.relative_to(site))
 for tag,link in page.links:
  target=urlsplit(urljoin(url,link))
  if target.netloc!='jboyce1.github.io' or not target.path.startswith('/ppsCTF/'):continue
  rel=unquote(target.path.removeprefix('/ppsCTF/'))
  p=site/rel
  if p.is_dir():p=p/'index.html'
  if not p.exists() and not p.suffix:p=p.with_suffix('.html')
  count+=1
  if not p.is_file():errors.append((file.relative_to(site),link,'missing file'));continue
  if target.fragment and p.suffix=='.html':
   parsed=pages.get(p) or Page(p.read_text())
   if unquote(target.fragment) not in parsed.ids:errors.append((file.relative_to(site),link,'missing anchor'))
# Retain the heading IDs used by pre-migration lesson bookmarks.
legacy_file = Path(__file__).resolve().parents[1] / 'docs/workrole-legacy-anchors.json'
legacy = json.loads(legacy_file.read_text())
legacy_count = 0
for page_path, expected_ids in legacy.items():
 page = site / page_path
 if not page.is_file():
  errors.append((page_path, '', 'legacy bookmark destination missing'))
  continue
 parsed = pages.get(page) or Page(page.read_text())
 for anchor in expected_ids:
  legacy_count += 1
  if anchor not in parsed.ids:
   errors.append((page_path, '#' + anchor, 'legacy bookmark anchor missing'))
print(f'Legacy bookmark audit: {legacy_count} pre-migration anchors checked.')
print(f'Built-site audit: {len(pages)} pages, {count} local references, {len(errors)} errors.')
for error in errors:print(*error,sep=': ')
raise SystemExit(bool(errors))
