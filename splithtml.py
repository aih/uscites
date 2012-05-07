#Python

try:
    import re2 as re
except:
    import re
import autoparser

# path =  [insert path to uscode html files]
uschtml = '2010usc26.htm'
divider="<!-- documentid:"

def splithtml():
    with open(path+uschtml,'r') as uscfile:
        #Split documents between <documentid:> references
        uscfile = uscfile.read()
        uscfiles = uscfile.split(divider)

    return uscfiles

