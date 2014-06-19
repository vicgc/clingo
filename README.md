clingo
=================

clingo is a tool which I am writing to help me manage my files 
efficiently.

For that, I am writing a virtual filesystem which would automatically 
index files into a xapian index at the time of their creation or any update.

It is the xapian index which would help in searching a file by name, by 
tags or by their description. Since files are indexed instantaneously on 
their creation, searching a file name shouldn't require searching 
recursively over a directory. It's just a simple lookup into the 
database and you will be presented with results instantaneously. 
Similarly when any file is deleted its data is removed from xapian index 
at that very instant.


Installation
================

        virtualenv venv
        source venv/bin/activate
        python <source_to_clingo_dir> setup.py install


Running 
==================
