# Modern LaTeX is not as bad as you think

This post is for you if your advisor/coworker/inner masochist is insisting that you should really try using LaTeX. My goal here is not to convert you to the Church of [Knuth](https://en.wikipedia.org/wiki/Donald_Knuth), but to make it as painless as possible to evaluate what modern LaTeX has to offer, avoiding antiquated nonsense such as DVI files and backslash-escaped umlauts.

The sad truth is that all word-processing software sucks to some extent. [WYSIWYG](https://en.wikipedia.org/wiki/WYSIWYG) appears nice and simple but you pay the price as soon as you require moderate amounts of referencing (equations, figures, tables, sections, page numbers, bibliographic citations...) and/or automation (macros, getting arbitrary content from other software). Markup languages such as LaTeX clearly separate content from format, but LaTeX itself is pretty long in the tooth (over 40 years now), does not follow modern software conventions, and rests on a rickety pile of packages upon packages.

To make matters worse, many LaTeX tutorials fail to take into account crucial modern improvements, such as the ability to directly generate pdf files, type text using unicode encoding (`ambiguïté` instead of `ambigu\"it\'e`), use any font installed on your system, and insert pictures in modern vector and/or raster formats (pdf, jpg, png).

Here is a simple set of instructions to get you started writing mostly painless LaTeX, along with a minimal template that offers the following basic features:

* use any font installed on your system
* type regular unicode text, including with accents or using other scripts than the Latin alphabet
* insert external pdf plots into figures
* automatically number and refer to specific pages, sections, figures, equations
* insert bibliographic citations and automatically collect the corresponding references at the end of your document

[Here](/ramblings/modern-latex/minxelatex.zip) is a zip file with the full template, along with the fonts used in this template (`STIX2` directory) which you will have to install on your system. To compile this source file, I recommend installing the [TeX Live](https://www.tug.org/texlive) distribution. If you are on macOS, aim for the [MacTeX](https://www.tug.org/mactex) distribution, which includes Mac-specific software.

Compiling the `minxelatex.tex` source file is done with XeLaTeX, a modern reimplementation of LaTeX. On the command line, this is simply a matter of issuing `xelatex minimal-xelatex.tex`, but on a Mac I recommend opening the source file in TeXShop (bundled with MacTeX). The first two lines of the source file are special comments that let TeXShop know to compile using XeLaTeX.

Preparing all of the bibliographic references is done in a second step, using another program named `biber` (also included in TeX Live). This can be done by issuing `biber minimal-xelatex`, or by specifying `biber` in TeXShop's preferences (Preferences -> Engine -> BibTeX Engine). After running biber successfully, run XeLaTeX once again to update the document accordingly:

<p align="center">
<img align="center" src="/ramblings/modern-latex/minxelatex.jpg" style="border:1px solid #dddddd; width:80%;">
</p>

Hopefully, these instructions should allow anyone to start writing actual sentences in a document within minutes of downloading everything. You will most certainly want to adjust some settings, and will have to dive in to do so. At that point, [TeX Stack Exchange](https://tex.stackexchange.com) is your best friend, but at least you'll be starting from a reasonably good place.