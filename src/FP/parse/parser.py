from bs4 import BeautifulSoup
import os
import re
import sys
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
root_gb='part2'
gb='google'
HOME=os.path.expanduser('~')
hPATH=os.path.join(HOME,'Trace',root_gb,'html',gb)
if not os.path.exists(os.path.join(HOME,'Trace',root_gb,'html',gb+'_parsed')):
    os.makedirs(os.path.join(HOME,'Trace',root_gb,'html',gb+'_parsed'))
    

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Start tag:", tag
        for attr in attrs:
            print "     attr:", attr
           
    def handle_endtag(self, tag):
        print "End tag  :", tag
       
    def handle_data(self, data):
        print "Data     :", data
        
    def handle_comment(self, data):
        print "Comment  :", data
        
    def handle_entityref(self, name):
        print name
        c = unichr(name2codepoint[name])
        print "Named ent:", c
        
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print "Num ent  :", c
        
    def handle_decl(self, data):
        print "Decl     :", data
        
parser = MyHTMLParser()

target_path= sys.argv[1].split(' ')[0]

print target_path
f=open(target_path,'r')
a=f.read()
data=re.sub(r'\<!--[0-9][0-9][0-9]\-->','',re.sub(r'\<!--[0-9][0-9]\-->','',re.sub(r'\<!--[0-9]\-->','',a)))
parser.feed(data)
    