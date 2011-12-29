## Engine 

# What Works

All the main views - home page, subject list, subject index, section
including displaying comments.

# What Doesn't

Templates are incomplete / non-existent.

Comments cannot be added. Comments jQuery code is incomplete.

The timestamp format used for comments needs to be changed.

Paragraphs reference their sections by ForeignKey on id column of sections
table. It's inconvenient to add paragraphs this way - the section ids are
less transparent than, say, a composite key on the section's subject name
and short (url) name. Don't know whether it's better to change the key,
or add paragraphs using some new interface..

No tests have been written.

Routing URLs with trailing slashes is not working - /subjects goes to
the subjects page, while /subjects/ gives 404.

Probably other stuff.

## Texparser

Our pipeline will make use of [TeX4ht]( http:tug.org/tex4ht ). It can
convert .tex files in various ways; for example, it can render maths
using either jsMathor MathML.

Our goal is to get TeX4ht to ignore all of
the LaTeX that could be processed by MathJax ([here](
http://research.microsoft.com/en-us/um/people/eyal/mathjax/docs/html/tex.html#environments
)).

Current idea:

LaTeX input -> script that replaces MathJax environments with sentinel
values -> TeX4ht ?in MathML/XHTML mode or jsMath mode? -> script that
replaces sentinels -> script that cleans up html for insertion into
Engine template -> output.
