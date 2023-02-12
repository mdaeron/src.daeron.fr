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

I played with several static website generators over the years but always felt (clearly because my needs in that department are exceedingly simple) that they were doing something very simple with a little too much overhead. So I did the opiniated but throroughly unoriginal thing and wrote my own static website generator from scratch using Python. It's tiny because it does very few things:

1. Read a bunch of Markdown files from a folder
2. Convert this content to HTML
3. Insert this HTML in a template HTML file
4. Read the last modified date of the Markdown file and insert that in the HTML file
5. Copy each HTML file to another folder which I will eventually copy to the web server

