whew
====

whew is for people who think that CMSes suck. Needs python and one or two python packages, and converts your collection of markdown files (with codehilite plugin) into a static webpage.

Because encoding sucks, too, source files must be UTF-8, target files will be UTF-8. No discussion.

Btw, whew is ideal if you want to convert all your [stackoverflow](http://stackoverflow.com)-posts into a 
self-praising website, which is actually the reason why I wrote this.


Basic Usage
===========

Have a source-directory ...


    my_pointless_website/
        image_of_how_i_make_a_fool_of_me.jpg
        brabble.md
        chunter.md
        absurd_stuff/
           SmatterAndPiffle.md

then run the script ...


    whew my_pointless_website  generated_html


and you get ...

    generated_html/
        image_of_how_i_make_a_fool_of_me.jpg
        index.html
        brabble.html
        chunter.html
        absurd_stuff/
            index.html
            SmatterAndPiffle.html

Details
=======

Each subdirectory contains a file 'index.html', with all your stuff concatenated into it. 
Within index.html, each article will have a link to a standalone version.

Titles of articles are their filenames, with a space-character inserted before inner uppercase letters:

    cat SmatterAndPiffle.html
    ...
       <h1>Smatter And Piffle</h1>
    ...

The titles of index.html files are based on the folder name, and transformed similarly.

Every index.html file containing more than one entry will get a navigational directory for free.
