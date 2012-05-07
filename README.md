uscites
=======

Library to parse internal citations in the U.S. Code

License: MIT (http://www.opensource.org/licenses/mit-license.php)

This library is used to parse the internal citations within the U.S. Code on tax26.com, a site for tax law professionals to navigate the Code and regulations.

The regex are in the file usc-regex.txt, and are used by the file autoparse.py in a number of passes through each section, to identify many kinds of citations in the Code.  

The .pkl files contain a list of all of the Named Acts, since many of the Code citations are to acts (e.g. section XXX of the Internal Revenue Act of 1986).  We do not have a comprehensive solution to linking these references to their sources yet.

If you have questions on this library, or are passionate about linked legislative data, feel free to contact aih at tabulaw dot com.  No guarantees I remember how any given regex works, however.
