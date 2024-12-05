# Get BibTeX from a DOI

You probably know that [doi.org](https://doi.org) will redirect any DOI you throw at it to the current URL of the corresponding document. For example: [https://doi.org/10.1016/j.chemgeo.2024.122148](https://doi.org/10.1016/j.chemgeo.2024.122148) will send you to Elsevier.

But you can use something called [HTTP headers](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields) to specify that, instead of a simple redirect, you want to get back the bibliographic information for that reference in BibTeX format. A simple way to do so is to use a command-line utility such as `curl`:

```
curl -LH "Accept: text/bibliography; style=bibtex" https://doi.org/10.1016/j.chemgeo.2024.122148
```

Which will yield something like:

```
 @article{Pesnin_2024, title={Mineralogical and environmental effects on the δ13C, δ18O, and clumped isotope composition of modern bryozoans}, volume={662}, ISSN={0009-2541}, url={http://dx.doi.org/10.1016/j.chemgeo.2024.122148}, DOI={10.1016/j.chemgeo.2024.122148}, journal={Chemical Geology}, publisher={Elsevier BV}, author={Pesnin, Marie and Thaler, Caroline and Daëron, Mathieu and Nomade, Sébastien and Rollion-Bard, Claire}, year={2024}, month=sep, pages={122148} }
```

### Streamlining the process

Let's make our lives easier by automating the process further, so that (a) there is no need to add the header format and prefix the DOI with `https://doi.org/`, and (b) sending the output directly to the clipboard. Unsuprisingly, this is easy to achieve with Python:

```py
#! /usr/bin/env python

import sys, requests, pyperclip

doi = sys.argv[1]              # DOI is the first command-line argument
url = f'http://doi.org/{doi}'  # construct the URL

# HTTP header to get BibTeX format back
headers = {'Accept': 'text/bibliography; style=bibtex'}

# send out the HTTP request
r = requests.get(url, headers = headers)

r.encoding = 'utf-8'  # specify that the response is UTF8-encoded
bib = r.text[1:-1]    # shave of the first and last characters of the response
pyperclip.copy(bib)   # copy the result to the clipboard
print(bib)            # and print it out as an indicator of success
```

Save the above as `doi2bibtex`, make it executable (this should require something like `chmod +x doi2bibtex` assuming you are on a [POSIX](https://en.wikipedia.org/wiki/POSIX) system), move it to somewhere on your [path](https://en.wikipedia.org/wiki/PATH_(variable)), and voilà, now you can simply type `doi2bibtex` followed by any valid DOI, wait to the response to print out, and immediately copy the results into your favorite bibliographic piece of software.

For now, the Python code above requires a functional Python installation, along with the `requests` and `pyperclip` dependencies, which is [no fun at all](https://xkcd.com/1987). See [here](/ramblings/uv-shebang) for a painless solution to this problem.