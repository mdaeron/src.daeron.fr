# Yet another static website engine

Let's face it, nobody wants to hand-code HTML tags using a stone chisel like it's 1995. When you wish to publish a couple of simple web pages, it's very convenient to write them up using plain text such as this:

````
My secret recipe

Based on Granny's blog (https://grannysblog.net)

Ingredients

- water
- sugar
- flour

Instructions

1. Mix the ingredients
2. Bake them for an hour
````

Some software (e.g., PHP) are able to perform “**dynamic**” serving of such text files, which means that every time someone uses their browser to load a certain URL, the server will read the corresponding file, convert it to HTML, and send the result back to the browser. This works well, and offers very powerful options such as reading some variables from the URL itself and adjusting the result accordingly (for example, by sending back the contents in another language, or by querying a database before returning the results). However setting up and debugging such systems can be challenging at first (though never underestimate your ability to learn), and they can be brittle (prone to failing in unexpected ways) and vulnerable to hacking. Also, unless you run your own server, you have to find a reliable hosting service, which may be free or not.

Another, increasingly popular option is to convert your text files to HTML offline and upload the resulting files to a “**static**” web server, which will only serve these pages as they are and never attempt to be clever about it. The drawback is that you are limited to a finite number of “dumb” pages (as opposed to something entirely dynamic such as [ClumpyCrunch](http://clumpycrunch.pythonanywhere.com)). But this means any bugs will show up offline, before you publish anything to the web, and the resulting bunch of files can be hosted nearly anywhere, generally for free. I'm using [Github Pages](https://pages.github.com) for now, but moving to another provider would be fast and painless.

There are many static website generators with bells and whistles. Popular ones currently include [Hugo](https://gohugo.io), [Jekyll](https://jekyllrb.com), and [Pelican](https://getpelican.com). They work well and require only a little bit of time to understand their internal logic (pages vs posts, tagging conventions, etc). Pretty much all of them understand [Markdown](https://www.markdownguide.org), a lightweight markup language designed to look like plain text but still allowing simple typographic formatting and linking to local or remote URLs. Converting our recipe to Markdown would require very few changes:

````
# My secret recipe

Based on [Granny's blog](https://grannysblog.net)

## Ingredients

- water
- sugar
- flour

## Instructions

1. Mix the ingredients
2. Bake them for an hour
````

I played with several static website generators over the years, but clearly my needs in that department are exceedingly basic and I always felt that they were doing something very simple with a little too much overhead. So I did the opiniated but throroughly unoriginal thing and wrote my own static website generator from scratch using Python. It's tiny because it does very few things:

1. Read a bunch of Markdown files from a folder
2. Convert this content to HTML
3. Insert this HTML in a template HTML file
4. Read the last modified date of the Markdown file and insert that in the HTML file
5. Copy each HTML file to another folder which I will eventually copy to the web server

Here's the main code. First, import the libraries we will need:

````
from pathlib import Path
import markdown
import datetime
import http.server
import socketserver
import shutil
from os import makedirs
from os.path import getmtime
````

Then define some settings. The local server will come in later so that we can check the final static website in a browser.

````
PORT = 8080            # the port to be used by the local server
SRC  = Path('.')       # the directory to read files from
DEST = '../daeron.fr'  # the directory to save files to
````

This class will be used by the local server:

````
class Handler(http.server.SimpleHTTPRequestHandler):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, directory = DEST, **kwargs)
````

Then create the Markdown parser with some extensions:

````
md = markdown.Markdown(
	extensions = [
		'pymdownx.tilde',
		'pymdownx.caret',
		'pymdownx.superfences',
		])
````

Erase any previous website in the `DEST` directory:

````
for p in Path(DEST).glob('*'):
	if not p.name.startswith('.'):
		if p.is_file():
			p.unlink()
		elif p.is_dir():
			shutil.rmtree(p)
````

Read the HTML template we will later use:

````
with open('html/index.html') as fid:
	html = fid.read()
````

For each Markdown file in the `md` directory, we read its content, convert it to HTML using the Markdown parser defined above, and insert the result into the HTML template, along with some info about when the Markdown file was last modified. We then create a website directory named after the Markdown file and save the resulting HTML file there:

````
for p in SRC.glob('md/*.md'):

	with open(p) as fid:
		content = fid.read()
	
	last_modif = (
		'Last modified on '
		+ datetime.datetime.fromtimestamp(getmtime(p)).strftime('%d %b %Y')
		)

	html_with_content = html.replace('__page__', p.stem)
	html_with_content = html_with_content.replace('__last_modif__', last_modif)
	html_with_content = html_with_content.replace('__markdown_page__', md.convert(content))

	if p.stem == 'index':
		outfile = Path(f'{DEST}/index.html')
	else:
		outfile = Path(f'{DEST}/{p.stem}/index.html')
		makedirs(outfile.parent, exist_ok = True)

	with open(outfile, 'w') as fid:
		fid.write(html_with_content)
````

We also copy a bunch of binary files (article PDFs) from the `static` directory to the website, along with a CSS file used to define the appearance of our final pages:

````
for p in SRC.glob('static/**/*'):
	if p.name.startswith('.'):
		continue
	if p.is_file():
		newfile = Path(f'{DEST}/' + '/'.join(p.parts[1:]))
		makedirs(newfile.parent, exist_ok = True)
		shutil.copy(p, newfile)		
````

We add two files needed by Github Pages:

````
Path(f'{DEST}/.nojekyll').touch()
with open(f'{DEST}/CNAME', 'w') as fid:
	fid.write('daeron.fr')
````

Finally, we start a local web server so that we can check out the result before uploading it to the actual remote server (this is done independently, not by the code shown here):

````
with socketserver.TCPServer(('', PORT), Handler) as httpd:
	try:
		print(f'Serving at http://127.0.0.1:{PORT}')
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
````

The whole thing is fewer than a hundred lines of code and this is what this website runs on. Although the actual content of the website is likely to change over time, that will only require editing a few Markdown files, and I expect that the site generator will pretty much remain as is. The complete source code is available [here](https://github.com/mdaeron/src.daeron.fr).