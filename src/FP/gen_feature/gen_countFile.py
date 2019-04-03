import os
import numpy
import math
import re
import csv
import time
import pandas as pd
import numpy as np
from statsmodels.iolib.table import Row
HOME=os.path.expanduser('~')
def most_common(L):
  # get an iterable of (item, iterable) pairs
    max_cnt=0

    SL = sorted((x, i) for i, x in enumerate(L))
    #print 'SL:', SL
    count_list=[]
    groups = itertools.groupby(SL, key=operator.itemgetter(0))
    
  # auxiliary function to get "quality" for an item
    def _auxfun(g):
      item, iterable = g
      count = 0
      
      min_index = len(L)
      for _, where in iterable:
        count += 1
        
        min_index = min(min_index, where)
      #if count ==30:
      #    print 'item %r, count %r, minind %r' % (item, count, min_index)
      print 'item %r, count %r, minind %r' % (item, count, min_index)

      count_list.append(count)
      
      return count, -min_index
    # pick the highest-count/earliest item
    
    
    
    
    
    max(groups, key=_auxfun)[0]
    return max(count_list)
    
  
def findFingerprintable(filename):
    pPATH=os.path.join(HOME,'results',filename)
    f=open(pPATH)
    NCCword=[]
    TN=0.0
    TP=0.0
    FP=0.0
    FN=0.0
    TTP=0.0
    total=0.0 # total samples in monitored set
    line_num=0
    for line in f:
	if 'fold' in line:
		continue
        predicted=line.split(',')[1]
        actual=line.split(',')[2]
        if (predicted == actual):  
            if (predicted != '-1'):#true negative

                NCCword.append(actual)
                


    most_common(NCCword)
if __name__ == "__main__":
    ## 0-1. find the fingerprintable keywords
    # each line in result file should look like 'index,predicted,actual'
    #nn_result='nn/KF_all_open__wf2500_101_9000.0_500_fullnet.txt'
    """
    python gen_countFile.py result-file > count-file
    """
    nn_result = sys.argv[1].split(' ')[0]
    findFingerprintable(nn_result)
