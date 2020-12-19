MAKE SURE THERE ARE NO WHITE SPACES IN ANY FILES! INCLUDING THE LATEX FILES!

The package natbib is automatically loaded by the achemso package. That's why you get those warnings from the natbib package.

Supposing that your .tex file is named test.tex, I suggest you first to delete the files test.aux and test.bbl.

After that, run, in the following sequence:

    pdflatex test

    bibtex test

    pdflatex test

    pdflatex test

You shouldn't have problems with the MWE you've provided.

Also remember that the achemso package automatically loads the achemso bibliography style, which is the same as inserting the line

\bibliographystyle{achemso}

so you don't have to add such a line in your document.
