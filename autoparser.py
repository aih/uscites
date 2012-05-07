#!/usr/bin/python<2.7>
# -*- coding: utf-8 -*-

import string, os, sys
from splithtml import *
import codecs
try:
    import re2 as re
except:
    import re

regfile = os.path.abspath(os.path.dirname(__file__))+'/usc-regex.txt'
divider="<!-- documentid:"
_DEBUG = False

#   To parse the html in data/, documentid:26_12 = 26usc12


def makergxlist(regfile):
    rfile = codecs.open(regfile, 'r', 'utf-8')
    findreplace = []
    for eachline in rfile.readlines():
        if (not eachline.isspace()) & (eachline[0] <> '#'):
            pattern_replace = unicode(eachline).strip().split('#')
            findreplace.append(pattern_replace)
    rfile.close()
    findreplace = [(re.compile(pattern, re.U|re.M), replacement) for pattern, replacement in findreplace]
    return findreplace

def subfile(inputfile, findreplace):
    outtext = inputfile
    if inputfile is None:
        return outtext

    for counter, pattern_replace in enumerate(findreplace):
        try:
            outtext, subs = re.subn(pattern_replace[0], pattern_replace[1], outtext)
            if _DEBUG and subs > 0:
                print pattern_replace[0].pattern
                print pattern_replace[1]
                print "=" * 30
        except KeyboardInterrupt:
            print counter, ' substituted: ', subs 
            print pattern_replace[0], "||||", pattern_replace[1], outtext
    return outtext 

# Dynamically replace references with links 
def parsesections(pattern, pattern_replace, section):
    sectionsref = re.search(pattern, section)
    while sectionsref:
        i1 = sectionsref.start(1)
        i2 = sectionsref.end(2)
        #print "found multiple secs at", i1, "-", i2
        section = section[:i1]+re.sub(pattern_replace[0], pattern_replace[1] % sectionsref.group(2), section[i1:i2]) + section[1+i2:]
        sectionsref = re.search(pattern, section)
    return section 

def parsenamedacts(pattern, intext):
    namedacts = re.findall(pattern, intext)
    namedacts = list(set(namedacts))
    outtext = intext
    for namedact in namedacts:
       #outtext =  outtext.replace(namedact+r'@/', encode_act(namedact)+r'@/')
       outtext =  outtext.replace(r'ref-namedact-'+namedact,r'ref-namedact-'+encode_act(namedact))
    return outtext

def encode_act(namedact):
    #encoding = namedact.translate(None, string.punctuation)  # removed because it is fails with unicode objects
    encoding = ''.join([char if char not in string.punctuation else '' for char in namedact]) 
    encodelen = str(len(encoding))
    encoding = [char if char not in string.lowercase+" " else '' for char in encoding]  #[encoding.translate(None, string.lowercase + r' ')]
    encoding.append('-' + encodelen)
    out = "".join(encoding)
    return out

# Loop through sections with various parsing passes 
def parsers(uscfiles, findreplace):
    parsedfiles = []
    for counter, section in enumerate(uscfiles):

        #print ""
        #print "File", counter
        parsedfile = subfile(section, findreplace)
        #print parsedfile
        # Replace Multiple Section references with links
        #   Include [^<] to make sure no group is transformed twice
        pattern =  r'@@@\s[Ss]ections?\s([^<]*?)@@@@@(.*?)@@'
        pattern_replace = [r'%s' % u'(\d+\w*(?:\(\w+\))*[-|–]?\d*)([, @])', r'<a href="/laws/target/%s/\1" class="sec">\1</a>\2']  
        parsedfile = parsesections(pattern, pattern_replace, parsedfile)
        #parsedfile = re.sub(r'@of-ref@', r'ref-Title-'+title, parsedfile)
        parsedfile = re.sub(r'@@ref-.*?@', r'', parsedfile)
        #parsedfile = re.sub(r'ref-title-this', r'ref-title-'+title, parsedfile)



        # Encode Named Acts by removing lowercase and non-word characters, and appending the length of the name w/o non-word characters
        #pattern =  r'@@ref-namedact-(.*?)@@'
        pattern =  r'/ref-namedact-(.*?)/'
        parsedfile = parsenamedacts(pattern, parsedfile)

        parsedfile = re.sub(r'@of-ref@', r'ref-title-this', parsedfile)
        parsedfile = re.sub(r'@@ref-.*?@', r'', parsedfile)
        
        # Remove remaining @
        parsedfile = parsedfile.replace('@','')#.translate(None, '@')
        parsedfiles.append(parsedfile)
    return parsedfiles 

def parse(data=False):
    uscfiles = [data, ]#.split(divider)#splithtml()
    findreplace = makergxlist(regfile)
    parsedfiles = parsers(uscfiles, findreplace)
    
    return parsedfiles

