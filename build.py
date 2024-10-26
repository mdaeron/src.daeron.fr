#! /usr/bin/env python3

from pathlib import Path
import markdown
import datetime
import http.server
import socketserver
import shutil
from os import makedirs
from os.path import getmtime

PORT = 8080            # the port to be used by the local server
SRC  = Path('.')       # the directory to read files from
DEST = '../daeron.fr'  # the directory to save files to

class Handler(http.server.SimpleHTTPRequestHandler):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, directory = DEST, **kwargs)

md = markdown.Markdown(
	extensions = [
		'pymdownx.tilde',
		'pymdownx.caret',
		'pymdownx.highlight',
		'pymdownx.superfences',
		],
	)

for p in Path(DEST).glob('*'):
	if not p.name.startswith('.'):
		if p.is_file():
			p.unlink()
		elif p.is_dir():
			shutil.rmtree(p)
		

with open('html/index.html') as fid:
	html = fid.read()

for p in SRC.glob('md/**/*.md'):

	with open(p) as fid:
		content = fid.read()
	
	last_modif = (
		'Last modified on '
		+ datetime.datetime.fromtimestamp(getmtime(p)).strftime('%d %b %Y')
		)
	
	
	try:
		title = [l for l in content.split('\n') if l.startswith('# ')][0].strip().replace('# ', '')
	except IndexError:
		title = 'daeron.fr'

	html_with_content = html.replace('__page__', p.stem)
	html_with_content = html_with_content.replace('__title__', title)
	html_with_content = html_with_content.replace('__last_modif__', last_modif)
	html_with_content = html_with_content.replace('__markdown_page__', md.convert(content))

	if p.stem == 'index':
		outfile = Path(f'{DEST}/index.html')
	else:
		loc = '/'.join(p.parts[1:-1])
		if loc:
			loc = loc + '/'
		outfile = Path(f'{DEST}/{loc}{p.stem}/index.html')
		makedirs(outfile.parent, exist_ok = True)

	with open(outfile, 'w') as fid:
		fid.write(html_with_content)

for p in SRC.glob('static/**/*'):
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


