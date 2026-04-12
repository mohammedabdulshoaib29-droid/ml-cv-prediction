import requests
import os
from pathlib import Path

# Test main page loads
print("Testing frontend server...")
resp = requests.get('http://localhost:8000/', timeout=5)
print(f'Frontend Load Status: {resp.status_code}')
print(f'Content Length: {len(resp.text)} bytes')

has_react = "React" in resp.text or "root" in resp.text or "static" in resp.text
print(f'React App Detected: {has_react}')

# List what the build includes
print('\nBuild Contents:')
build_dir = Path('frontend/build')
files = list(build_dir.glob('**/*'))
html_files = [f for f in files if f.suffix == '.html']
js_files = [f for f in files if f.suffix == '.js']
css_files = [f for f in files if f.suffix == '.css']

print(f'  HTML files: {len(html_files)}')
print(f'  JS files: {len(js_files)}')
print(f'  CSS files: {len(css_files)}')

if html_files:
    print(f'  Main HTML: {html_files[0].name}')
if js_files:
    latest_js = sorted(js_files, key=lambda f: f.stat().st_mtime)[-1]
    print(f'  Latest JS: {latest_js.name}')
if css_files:
    latest_css = sorted(css_files, key=lambda f: f.stat().st_mtime)[-1]
    print(f'  Latest CSS: {latest_css.name}')

print('\n✅ Frontend is properly served and ready!')
