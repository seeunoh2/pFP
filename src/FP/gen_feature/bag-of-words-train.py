'''
Created on Jan 16, 2017

@author: tpdms1209
'''
import os
import numpy
import math
import re
import csv
import time
import pandas as pd
import numpy as np
from statsmodels.iolib.table import Row
import ranks
HOME=os.path.expanduser('~')

#1 linkAnalysis: \target_SE_links\
# - all: m_*.txt
# - body: m_*_removed.txt
# - template
def link_fextract(folder,keyword,html_file):
    html_path=os.path.join(HOME,'html',folder+'_links')
    website=keyword
    if 'www' in keyword:
        keyword=keyword.split('www')[1].split('.')[1]
    else:
        keyword=keyword.split('.')[1]
    f=open(os.path.join(html_path,html_file.split('.html')[0]+'.txt'),'r')
    #f_body=open(os.path.join(html_path,'m_'+keyword+'_'+str(instance)+'_removed.txt'),'r')
    
    n_links=0 # number of links
    n_glinks=0 # number of google links
    domains=[]
    udomains=set()
    
    n_body_links=0 # number of links
    n_body_glinks=0 # number of google links
    body_domains=[]
    body_udomains=set()
    for line in f:
        if line.split('=>')[1].strip() == 'http://':
            continue
        if line.split('=>')[1].startswith('http:xgames')  or line.split('=>')[1].startswith('calendar') or line.split('=>')[1].startswith('c/') or line.split('=>')[1].startswith('%20/') or line.split('=>')[1].startswith('images/') or (line.split('=>')[1].startswith('http') and (keyword in line.split('=>')[1])) or line.split('=>')[1].startswith('/') or line.split('=>')[1].startswith('javascript') or line.split('=>')[1].startswith('#') or 'mailto:' in line:
            n_glinks += 1
        #if line.split('=>')[1].startswith('images/') or line.split('=>')[1].startswith('/') or line.split('=>')[1].startswith('javascript') or line.split('=>')[1].startswith('#') or 'mailto:' in line:
            domains.append(website)
            udomains.add(website)
        else:
           #print line
           if '/' in line:
               if 'http' in line:
                   print line
                   domains.append(line.split('=>')[1].split('/')[2].split('.')[-2]+'.'+line.split('=>')[1].split('/')[2].split('.')[-1])
                   udomains.add(line.split('=>')[1].split('/')[2].split('.')[-2]+'.'+line.split('=>')[1].split('/')[2].split('.')[-1])
               else:
                    print line
                    domains.append(line.split('=>')[1].split('.')[-2]+'.'+line.split('=>')[1].split('.')[-1])
                    udomains.add(line.split('=>')[1].split('.')[-2]+'.'+line.split('=>')[1].split('.')[-1])
        n_links += 1
    
            
    print '[all]number of links:',n_links
    print '[all]number of google links:',n_glinks
    print '[all]number of third party links:',n_links-n_glinks
    print '[all]number of domains:',len(domains)
    print '[all]number of unique domains:',len(udomains)
    
    
    return (n_links,n_glinks,n_links-n_glinks,len(domains),len(udomains))
    #5 features

    
#3 tagPath
def tagpath_fextract(SE,html_file):
    if 'ext' in SE:
        html_path = os.path.join(HOME, 'html', 'mon_ext_html_tagpath')
    else:
        html_path=os.path.join(HOME,'html',SE+'_tagpath')#'tagpath')
    
    f=open(os.path.join(html_path,html_file.split('.html')[0]+'_tagpath.txt'),'r')
    
    total_cnt=0
    upath_list=set()
    depths_list=[]
    total_body_cnt=0
    upath_body_list=set()
    depths_body_list=[]
    target_depths=[]
    target_tags=[]
    target_changes=[]
    counts_depth=[]
    tag_list=[]
    p_chg=0
    n_chg=0
    cnt_chg=0
    cnt_nchg=0
    pre_depth=0
    direction=0
    pre_dir=0
    lines=f.readlines()
    for line in lines:
        line=re.sub(r'\[.*?\]', '', line)
        upath_list.add(line)
        temp=set()
        for tag in line.split('/'):
            if tag == '':
                continue
            temp.add(tag)
        tag_list.append(len(temp)) # number of unique tags per each line
        
        depth=len(line.split('/'))-1
        depths_list.append(depth)
        if depth-pre_depth >0:
            p_chg += 1
            direction=1
        else:
            n_chg += 1
            direction=-1
        
        if direction*pre_dir == 1:
            cnt_nchg += 1
        else:
            cnt_chg += 1
        total_cnt += 1
        pre_depth=depth
        pre_dir=direction
    target_tags.append(sum(tag_list))
    target_tags.append(numpy.median(tag_list))
    target_tags.append(numpy.mean(tag_list))
    target_tags.append(numpy.std(tag_list))
    
    target_changes.append(cnt_chg)
    target_changes.append(cnt_nchg)
    target_changes.append(p_chg)
    target_changes.append(n_chg)
    
    target_depths.append(max(depths_list))
    target_depths.append(min(depths_list))
    target_depths.append(numpy.median(depths_list))
    target_depths.append(numpy.round(numpy.mean(depths_list)))
    target_depths.append(numpy.percentile(depths_list,30))
    target_depths.append(numpy.percentile(depths_list,70))
    #print target_depths
    #print len(target_depths)
    
    
    cnt1=0
    cnt2=0
    cnt3=0
    cnt4=0
    cnt5=0
    cnt6=0
    
    for line in lines:
        if len(line.split('/'))-1 == target_depths[0]:
            cnt1 += 1
        if len(line.split('/'))-1 == target_depths[1]:
            cnt2 += 1
        if len(line.split('/'))-1 == target_depths[2]:
            cnt3 += 1
        if len(line.split('/'))-1 == target_depths[3]:
            cnt4 += 1
        if len(line.split('/'))-1 == target_depths[4]:
            cnt5 += 1
        if len(line.split('/'))-1 == target_depths[5]:
            cnt6 += 1
    #print depth, count
    target_depths.append(cnt1)
    target_depths.append(cnt2)
    target_depths.append(cnt3)
    target_depths.append(cnt4)
    target_depths.append(cnt5)
    target_depths.append(cnt6)
        
        
    return (total_cnt,len(upath_list),target_tags,target_changes,sum(depths_list),numpy.std(depths_list),target_depths)
#1+1+4+4+1+1+6=18
#4 tag
def tag_fextract(SE,file): ## gb is always 'all'
    
    html_path=os.path.join(HOME,'html')
    
    f=open(os.path.join(html_path,SE+'_parsed','parsed_'+file.split('.html')[0]+'.txt'),'r')
    parsed_lines=f.readlines()
    f.close()
    if 'ext' in SE:
        f = open(os.path.join(html_path, 'mon_ext_html_tagpath', file.split('.html')[0] + '_tagpath.txt'), 'r')
    else:
        #f=open(os.path.join(html_path,'tagpath',file.split('.html')[0]+'_tagpath.txt'),'r')
        f=open(os.path.join(html_path,SE+'_tagpath',file.split('.html')[0]+'_tagpath.txt'),'r')
    path_lines=f.readlines()
    f.close()
    f=open(os.path.join(html_path,SE,file),'r')
    html_lines=f.readlines()
    f.close()
    n_tags=0
    n_attr=0
    n_comment=0
    utag_list=set()
    uattr_list=set()
    for line in path_lines:
        line=re.sub(r'\[.*?\]', '', line)
        n_tags += (len(line.split('/'))-1)
        for tag in line.split('/'):
            if tag == '':
                continue
            utag_list.add(tag)
        if 'comment' in line:
            n_comment += 1
    
    isScript=False  
    isStyle=False
    isScriptData=False  
    isStyleData=False  
    isData=False
    script_cha=0
    style_cha=0   
    attr_cha=0
    data_cha=0
    data_word=0
    sty_data_cha=0
    scr_data_cha=0
    sty_data_word=0
    scr_data_word=0
    for line in parsed_lines:
        line=line.strip()
        if 'attr:' in line:
            n_attr += 1
            uattr_list.add(line.strip().split(':')[1].strip().split(',')[0].strip().replace('(','').replace(')','').replace("'",""))
            temp=line.split(',')[1].replace(')','').replace("'","")
            attr_cha += (len(temp)-temp.count(' '))
            
        if isData:
            data_cha += (len(line)-line.count(' '))
            temp=filter(None,line.split(' '))
            data_word += len(temp)
            isData=False
            
        if isScript:
            temp=line.replace('attr:','').replace('Data     :','').replace('(','').replace(')','')
            script_cha += (len(temp)-temp.count(' '))
            if 'Data     :' in line:
                isScriptData=True
                
        if isStyle:
            temp=line.replace('attr:','').replace('Data     :','').replace('(','').replace(')','')
            style_cha += (len(temp)-temp.count(' '))
            if 'Data     :' in line:
                isStyleData=True
        
        if isScriptData:
            scr_data_cha += (len(line)-line.count(' '))
            temp=filter(None,line.split(' '))
            scr_data_word += len(temp)
            isScriptData=False
            
        if isStyleData:
            sty_data_cha += (len(line)-line.count(' '))
            temp=filter(None,line.split(' '))
            sty_data_word += len(temp)
            isStyleData=False
            
        if 'Start tag: script' in line:
            isScript=True
        
        if 'End tag  : script' in line:
            isScript=False
            
        if 'Start tag: style' in line:
            isStyle=True
        
        if 'End tag  : style' in line:
            isStyle=False
        if 'Data     :' in line:
            isData=True
            
            
    total_cha=0
    for line in html_lines:
        total_cha += len(line)-line.count(' ') #total number of characters in html
    
    
    return (n_tags,len(utag_list),n_comment,n_attr,len(uattr_list),total_cha,script_cha,style_cha,attr_cha,data_cha,data_cha-scr_data_cha-sty_data_cha,data_word,data_word-sty_data_word-scr_data_word)

## 6.get specific portion of images and videos and details (e.g.,size, location, etc.) of them
def get_cont_portion(file,SE):
    html_path=os.path.join(HOME,'html')
    if 'ext' in SE:
        f = open(os.path.join(html_path, 'mon_ext_html_tagpath', file.split('.html')[0] + '_tagpath.txt'), 'r')
    else:
        #f=open(os.path.join(html_path,'tagpath',file.split('.html')[0]+'_tagpath.txt'),'r')
        f=open(os.path.join(html_path,SE+'_tagpath',file.split('.html')[0]+'_tagpath.txt'),'r')
    tagpath_lines=f.readlines()
    f=open(os.path.join(html_path,SE+'_parsed','parsed_'+file.split('.html')[0]+'.txt'),'r')
    parsed_lines=f.readlines()
    img_cnt=0.0
    for line in tagpath_lines:
        if 'img' in line:
            img_cnt += 1
    png_cnt=0.0
    ico_cnt=0.0
    jpg_cnt=0.0
    #jpeg_cnt=0.0
    gif_cnt=0.0
    bmp_cnt=0.0
    html_cnt=0.0
    css_cnt=0.0
    js_cnt=0.0
    mp3_cnt=0.0
    avi_cnt=0.0
    for line in parsed_lines:
        #if 'attr:' in line:
        if '.png' in line:
            png_cnt += 1
        if '.ico' in line:
            ico_cnt += 1
        if '.jpg' in line or '.jpeg' in line:
            jpg_cnt += 1
        
        if '.gif' in line:
            gif_cnt += 1
        if '.bmp' in line:
            bmp_cnt += 1
        if '.html' in line:
            html_cnt += 1
        if '.css' in line:
            css_cnt += 1
        if '.js' in line:
            js_cnt += 1
        if '.mp3' in line:
            mp3_cnt += 1
        if '.avi' in line:
            avi_cnt += 1
            
    
    return (img_cnt,img_cnt/float(len(tagpath_lines)),png_cnt,png_cnt/float(len(tagpath_lines)),ico_cnt,ico_cnt/float(len(tagpath_lines)),jpg_cnt,jpg_cnt/float(len(tagpath_lines)),gif_cnt,gif_cnt/float(len(tagpath_lines)),bmp_cnt,bmp_cnt/float(len(tagpath_lines)),html_cnt,html_cnt/float(len(tagpath_lines)),css_cnt,css_cnt/float(len(tagpath_lines)),js_cnt,js_cnt/float(len(tagpath_lines)),mp3_cnt,avi_cnt)





if __name__ == "__main__":
    '''
    This is the script to generate design-level features for training file.
    Note that we assume that the number of monitored classes is 100
    To modify it, search row_index and change it with yours
    '''
    """Params: replace them with yours"""
    html_num_instance = 290
    html_path='mon_new_300'#'mon_html'

    # website url list location: url_list
    url_list='localized-urls-100-top.csv'#'alexa500-unpop500.csv'
    # bag_file is the name of 'design-level features' file
    bag_file='bag-new-300-train.csv'#'bag-wf-popular.csv'
    """      """
    # For each website, extract features over HTML
    csv_reader=csv.reader(open(os.path.join(HOME,url_list),'r'), delimiter = ',')

    csv_writer=csv.writer(open(os.path.join(HOME,'feature',bag_file),'w+'), delimiter = ',')

    # html path
    hPATH=os.path.join(HOME,'html',html_path)
    list_web=[]
    row_index=range(0,50)
    j=0
    j_index=0
    for row in csv_reader:
        if j in row_index:
            #print(row[0].split('http://')[1])
            if 'http://' in row[0]:
                website=row[0].split('http://')[1].strip()
            else:
                website = row[1].strip()
            list_web.append(website)
            j_index=j
        j+= 1
    index=0
    

    for website in list_web:
	cnt = 0
        #csv_writer.writerow(str(index))
        print('website ',str(index),': ',website)
        for file in os.listdir(hPATH):
	    if cnt == html_num_instance:
		break
            if website in file:
                csv_row=[]
                csv_row.append(str(index))
                result=link_fextract(html_path,website,file)
                for item in result:
                    csv_row.append(item)
		print("link_fextract is done!")
                result2=tagpath_fextract(html_path,file)
                for item in result2:
                    if isinstance(item, list):
                        for sub_item in item:
                            csv_row.append(sub_item)
                    else:
                        csv_row.append(item)
		print("tagpath_fextract is done!")
                result3 = tag_fextract(html_path,file)
                for item in result3:
                    if isinstance(item, list):
                        for sub_item in item:
                            csv_row.append(sub_item)
                    else:
                        csv_row.append(item)
		print("tag_fextract is done!")
                result4=get_cont_portion(file,html_path)
                for item in result4:
                    csv_row.append(item)
		print("get_cont_portion is done!")

                csv_writer.writerow(csv_row)
		cnt += 1
        index += 1


    # Conver features in ranks

    bag_file = 'bag-new-300-train.csv'
    isTest = False
    addIndex = 50
    ranks.generateRanks(bag_file, isTest, addIndex)


