# Unleash the power of uv shebangs

A [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) is the character sequence `#!` used at the start of a text file in [POSIX](https://en.wikipedia.org/wiki/POSIX) systems to specify which piece of software should be used to execute the contents of the file, for example:

```py
#! python
print("Nobody expects the Spanish Inquisition!")
```

In theory, `#! python` is sufficient. In practice, to ensure that your operating system can find the `python` executable, one often uses `#! /usr/bin/env python` instead. The executable [`env`](https://en.wikipedia.org/wiki/Env) is used to locate `python`, wherever it might reside on your computer.

But this means that to use the above script, you need to have Python installed. Python is notorious for its [dependency hell](https://xkcd.com/1987), meaning that it is very easy to find yourself in a situation where several independent Python distributions coexit within the same operating system (so that your shebang might be calling the wrong Python version), or where updating the Python library needed by one script (“dependency”) will break another script.

All this messiness can be avoided by using [`uv`](https://docs.astral.sh/uv), a Python dependency manager with the following selling points:

* `uv` is a self-contained executable which is very unlikely to break down even if you do something wrong.
* `uv` uses independent “virtual environments”, sandboxing each script so that changing the dependencies for one script will not break another
* `uv` is extremely fast, so that python itself and all required dependencies can be reinstalled from scratch without any noticeable overhead.

To use `uv`, you first have to [install it](https://docs.astral.sh/uv/getting-started/installation), then modify your shebang accordingly. There is absolutely no need to install Python for this to work.

```py
#! /usr/bin/env uv run python
print("Nobody expects the Spanish Inquisition!")
```

The true power of `uv` shebangs lies in the ability to specify dependencies within the shebang line. For example, if your script needs `numpy`:

```py
#! /usr/bin/env uv run --with numpy python
from numpy import eye
print(eye(5))
```

One may require a specific version of `numpy`:

```py
#! /usr/bin/env uv run --with numpy==2.1.2 python
import numpy
print(numpy.__version__)
```

One may also require more than one dependency:

```py
#! /usr/bin/env uv run --with matplotlib==3.9.2 --with scipy==1.14.1 python
```

Finally, one may require a specific version of Python:

```py
#! /usr/bin/env uv run --with matplotlib --with scipy --python 3.11.6 python
```

As a fully functional example, here is a version of the `doi2bibtex` script described [here](/ramblings/doi2bibtex) which only requires `uv` to work properly:

```py
#! /usr/bin/env uv run --with requests==2.32.3 --with pyperclip==1.9.0 python

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
