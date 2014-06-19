clingo 
===========

`Currently works on: Python 2.7 only`

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


What I wish to integrate in future
====================================

   - writing plug-ins for indexing different kind of data files   (text files are supported, mp3 files and pdf are must have).
   - pdf's can be indexed using `pdftotext` tool and indexing the obtained text file.  (might encounter some glitches)
   - Index mp3 files and content should be searchable with mp3 metadata.   (should be really cool !!)
   - GUI for tagging files, or maybe unity scope.   (awesome !!) 
   


Installation
================

1. Install xapian core libraries and python bindings for xapian.
   They are available in official Ubuntu repositories as well as in Arch package database.
   Most probably they should be available for Fedora as well.

2. Install fusepy which is available here. https://github.com/terencehonles/fusepy

3. Create a virtual environment and install there using

        virtualenv venv
        source venv/bin/activate
        python <source_to_clingo_dir> setup.py install
    


Steps for running and indexing files via mountpoint
=====================================================

1. Mounting a directory to a mountpoint and create a Virtual File System in Userspace.
        
        runFS /path-to-dir-to-be-mounted /path-to-the-mount-point
        runFS /home/khirod/Public/dir /home/khirod/mnt

2. Open a new terminal window and cd to the mountpoint. The contents of `/home/khirod/Public/dir` should now be mounted at mnt:
        
        cd /home/khirod/mnt
        nano Hello.txt
        
3. The content of this text file should have automatically been indexed when this file was created. Now you may want to add tags and description to this file.

        clingo -t Hello.txt     # for adding tags
        clingo -d Hello.txt     # for adding description

        
4. Now to search your files, just do a clingosearch

        clingosearch -t         # for tags based search
        clingosearch -d         # for description based search
        clingosearch -c         # for content based search (currently text files only)
        clingosearch -n         # simple search using name of file
