#! /usr/bin/env python3

from pathlib import Path
import markdown
import datetime
import http.server
import socketserver
import shutil
from os import makedirs
from os.path import getmtime

PORT = 8080
DEST = '../daeron.fr'

class Handler(http.server.SimpleHTTPRequestHandler):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, directory = DEST, **kwargs)

here = Path('.')
md = markdown.Markdown(extensions=['pymdownx.tilde', 'pymdownx.caret', 'pymdownx.superfences'])


for p in Path(DEST).glob('*'):
	if not p.name.startswith('.'):
		if p.is_file():
			p.unlink()
		elif p.is_dir():
			shutil.rmtree(p)
		

with open('html/index.html') as fid:
	html = fid.read()

for p in here.glob('md/*.md'):

	with open(p) as fid:
		content = fid.read()
	
	if p.stem == 'index':
		outfile = Path(f'{DEST}/index.html')
		last_modif = ''
	else:
		outfile = Path(f'{DEST}/{p.stem}/index.html')
		makedirs(outfile.parent, exist_ok = True)
		last_modif = 'Last modified on ' + datetime.datetime.fromtimestamp(getmtime(p)).strftime('%d %b %Y')

	html_with_content = html.replace('__page__', p.stem)
	html_with_content = html_with_content.replace('__last_modif__', last_modif)
	html_with_content = html_with_content.replace('__markdown_page__', md.convert(content))

	with open(outfile, 'w') as fid:
		fid.write(html_with_content)

for p in here.glob('static/**/*'):
	if p.name.startswith('.'):
		continue
	if p.is_file():
		newfile = Path(f'{DEST}/' + '/'.join(p.parts[1:]))
		makedirs(newfile.parent, exist_ok = True)
		shutil.copy(p, newfile)		

Path(f'{DEST}/.nojekyll').touch()

with open(f'{DEST}/CNAME', 'w') as fid:
	fid.write('daeron.fr')

with socketserver.TCPServer(('', PORT), Handler) as httpd:
	try:
		print(f'Serving at http://127.0.0.1:{PORT}')
		httpd.serve_forever()

	except KeyboardInterrupt:
		pass


