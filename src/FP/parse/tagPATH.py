'''
Created on Dec 20, 2016

@author: seeunoh
'''
from lxml import etree
import os
import re
HOME=os.path.expanduser('~')



def extract_tag_path(folder):
    hPATH=os.path.join(HOME,'html',folder)
    hwPATH=os.path.join(HOME,'html',folder+'_tagpath')

    for file in os.listdir(hPATH):
        print file
        if (file[:2]!='m_') and '_removed.html' not in file:

            f=open(os.path.join(hPATH,file),'r')
            fw=open(os.path.join(hwPATH,os.path.splitext(os.path.basename(os.path.join(hPATH,file)))[0]+'_tagpath.txt'),'w+')
            data=f.read()

            root = etree.HTML(data)
            tree = etree.ElementTree(root)
            for e in root.iter():
                fw.write(tree.getpath(e))
                fw.write('\n')
                #print tree.getpath(e)

if __name__ == "__main__":
    '''
    Create tagpath directory based on html files
    '''

    folder='facebook'#'mon_new_300'
    if not os.path.exists(os.path.join(HOME,'html',folder+'_tagpath')):
        os.makedirs(os.path.join(HOME,'html',folder+'_tagpath'))
    
    
    extract_tag_path(folder)
