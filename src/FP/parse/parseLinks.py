'''
Created on Sep 19, 2016

@author: seeunoh
'''
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import formatter
import htmllib
import os
from gi.overrides.keysyms import prescription

HOME=os.path.expanduser('~')
def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"


def parseDOM(gb):
    w = formatter.DumbWriter() # plain text
    f = formatter.AbstractFormatter(w)

    for ff in os.listdir(os.path.join(hPATH)):
        
        command='python parser.py {} > {}'\
        .format(shellquote(os.path.join(hPATH,ff)),shellquote(os.path.join(HOME,'html',gb+'_parsed','parsed_'+os.path.splitext(os.path.basename(os.path.join(hPATH,ff)))[0]+".txt")))
        
        print command
        
        result=os.system(command)

                
def extractLinks(gb):
    for ff in os.listdir(os.path.join(hPATH)): # iterate all html files under hPATH

        print ff
        fw=open(os.path.join(HOME,'html',gb+'_links',os.path.splitext(os.path.basename(os.path.join(hPATH,ff)))[0]+'.txt'),'w+')

        fw_removed=open(os.path.join(hPATH,ff),'r')
        p = htmllib.HTMLParser(f)
        p.feed(fw_removed.read())
        p.close()
        
        fw_removed.close()
        
        # print links
        
        i = 1
        for link in p.anchorlist:
            #print i, "=>", link
            fw.write(str(i)+"=>"+link) ## extract all links carried in HTML
            fw.write('\n')
            i = i + 1

if __name__ == "__main__":
    """
    Create links and parsed folder based on html files
    """
    gb='' # html folder name, it should be under ~/html
    hPATH=os.path.join(HOME,'html',gb)
    if not os.path.exists(os.path.join(HOME,'html',gb+'_links')):
        os.makedirs(os.path.join(HOME,'html',gb+'_links'))
    if not os.path.exists(os.path.join(HOME,'html',gb+'_parsed')):
        os.makedirs(os.path.join(HOME,'html',gb+'_parsed'))


    parseDOM(gb)
    extractLinks(gb)
        
