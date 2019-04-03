'''
Created on Jan 12, 2017

@author: seeunoh
'''
import os
import numpy as np
import csv
HOME=os.path.expanduser('~')

def round_down(num, divisor):
    value=abs(num) - (abs(num)%divisor)
    if num<0:
        return -value
    else:
        return value



def split_open_keyword(file_mon,file_unmon,fold,n_fold,nClass,mon_instance,unClass,unmon_instance,dim,reversed,b_label,feature):
    PATH=os.path.join(HOME,'Trace',file_mon) ## part2/feature/google/TLS_100google_80_80.csv
    PATH2=os.path.join(HOME,'Trace',file_unmon)
    fileReader = csv.reader(open(PATH,'r'), delimiter=',')
    fileReader2 = csv.reader(open(PATH2,'r'), delimiter=',')
    cell_len=[]
    csv_lines_mon=[]
    csv_lines_un=[]
    for row in fileReader:
        if reversed: ## if need to reverse the array
            csv_lines_mon.append([row[0]]+row[1:][::-1])
        else:
            csv_lines_mon.append(row)
        
    for row in fileReader2:
        if reversed:
            csv_lines_un.append([row[0]]+row[1:][::-1])
        else:
            csv_lines_un.append(row)
    
    
    sorted_csv_mon=sorted(csv_lines_mon, key = lambda x: int(x[0]))
    #sorted_csv_un=sorted(csv_lines_un, key = lambda x: int(x[0]))
    
    
    ins_train=int(mon_instance*nClass*(1-1.0/n_fold)+unmon_instance*unClass*(1-1.0/n_fold))
    ins_test=int(mon_instance*nClass*(1.0/n_fold)+unmon_instance*unClass*(1.0/n_fold))
    ins_all=int(mon_instance*nClass+unmon_instance*unClass)
    
    all_features=np.zeros(shape=(ins_all,dim))
    train_features=np.zeros(shape=(ins_train,dim))
    test_features=np.zeros(shape=(ins_test,dim))
    
    all_labels=np.zeros(ins_all)
    train_labels=np.zeros(ins_train)
    test_labels=np.zeros(ins_test)
    
    #print test_labels
    print('ins_train',ins_train)
    print('ins_test',ins_test)
    print('ins_all',ins_all)
    i_train=0
    i_test=0
    i_all=0
    for c in range(nClass): ## monitored set
        i=0
        j=0
        #print('For class',c,':')
        #print(int(fold*(mon_instance/n_fold)),int(fold*(mon_instance/n_fold)+(mon_instance/n_fold)))
        for line in sorted_csv_mon:
            if c == int(line[0]):
                #if i < mon_instance:
                if i in range(int(fold*(mon_instance/n_fold)),int(fold*(mon_instance/n_fold)+(mon_instance/n_fold))):
                    temp=[]
                    ##################
                    if feature == 'cell':
                        for item in line[1:]: # /512
                            rounded=round_down(float(item),512.0)
                            for r in range(int(abs(rounded/512))):
                                if rounded<0:
                                    temp.append(-1)
                                else:
                                    temp.append(1)
                    elif feature == 'resp':
                        for item in line[1:]: # /512
                            rounded=round_down(float(item),512.0)
                            temp.append(abs(int(rounded/512)))
                    else: ## cumul
                        for item in line[1:]: # /512
                            rounded=round_down(float(item),512.0)
                            temp.append(int(abs(rounded/512)))
                                
                    ###################
                    test_feature=[]
                    cell_len.append(len(temp))
                    if len(temp) <dim:
                        test_feature=temp
                        
                        for r in range(dim-len(temp)):
                            test_feature.append(0)
                            
                    else:
                        test_feature=temp[:dim]
                        
                    #print(i_test,line[0])
                    test_features[i_test]=test_feature
                    all_features[i_all]=test_feature
                    if b_label:
                        test_labels[i_test]=0
                        all_labels[i_all]=0
                    else:
                        test_labels[i_test]=int(line[0])
                        all_labels[i_all]=int(line[0])
                    
                    
                    i_test += 1
                    i_all += 1
                else:
                    #if j==(mon_instance/n_fold):
                    if i==mon_instance:
                        i=0
                        break
                    temp=[]
                    ##################
                    if feature == 'cell':
                        for item in line[1:]: # /512
                            rounded=round_down(float(item),512.0)
                            for r in range(int(abs(rounded/512))):
                                if rounded<0:
                                    temp.append(-1)
                                else:
                                    temp.append(1)
                    elif feature == 'resp':
                        for item in line[1:]: # /512
                            rounded=round_down(float(item),512.0)
                            temp.append(abs(int(rounded/512)))
                    else: ## cumul
                        for item in line[1:]: # /512
                            rounded=round_down(float(item),512.0)
                            temp.append(int(abs(rounded/512)))
                    ###################
                    train_feature=[]
                    cell_len.append(len(temp))
                    if len(temp) <dim:
                        train_feature=temp
                        for r in range(dim-len(temp)):
                            train_feature.append(0)
                    else:
                        train_feature=temp[:dim]
                    #print(i_train,line[0])
                    train_features[i_train]=train_feature
                    all_features[i_all]=train_feature
                    if b_label:
                        train_labels[i_train]=0
                        all_labels[i_all]=0
                    else:
                        train_labels[i_train]=int(line[0])
                        all_labels[i_all]=int(line[0])
                    
                    i_train += 1
                    i_all += 1
                i += 1
    i=0
    j=0
    print('Background class:')
    print(int(fold*(unClass/n_fold)),int(fold*(unClass/n_fold)+(unClass/n_fold)))
    for line in csv_lines_un: ## background set
        #if i < (unmon_instance/n_fold)*9:
        if i in range(int(fold*(unClass/n_fold)),int(fold*(unClass/n_fold)+(unClass/n_fold))):
            temp=[]
            ##########################
            if feature == 'cell':
                for item in line[1:]: # /512
                    rounded=round_down(float(item),512.0)
                    for r in range(int(abs(rounded/512))):
                        if rounded<0:
                            temp.append(-1)
                        else:
                            temp.append(1)
            elif feature == 'resp':
                for item in line[1:]: # /512
                    rounded=round_down(float(item),512.0)
                    temp.append(abs(int(rounded/512)))
            else: ## cumul
                for item in line[1:]: # /512
                    rounded=round_down(float(item),512.0)
                    temp.append(int(abs(rounded/512)))
            ##########################
            test_feature=[]
            cell_len.append(len(temp))
            if len(temp) <dim:
                test_feature=temp
                for r in range(dim-len(temp)):
                    test_feature.append(0)
            else:
                test_feature=temp[:dim]
            #print(i_test,-1)
            test_features[i_test]=test_feature
            all_features[i_all]=test_feature
            test_labels[i_test]=-1
            all_labels[i_all]=-1
            
            i_test += 1
            i_all += 1
        else:
            if i==unClass:
                i=0
                break
            temp=[]
            ##########################
            if feature == 'cell':
                for item in line[1:]: # /512
                    rounded=round_down(float(item),512.0)
                    for r in range(int(abs(rounded/512))):
                        if rounded<0:
                            temp.append(-1)
                        else:
                            temp.append(1)
            elif feature == 'resp':
                for item in line[1:]: # /512
                    rounded=round_down(float(item),512.0)
                    temp.append(abs(int(rounded/512)))
            else: ## cumul
                for item in line[1:]: # /512
                    rounded=round_down(float(item),512.0)
                    temp.append(int(abs(rounded/512)))
            #############################3
            train_feature=[]
            cell_len.append(len(temp))
            if len(temp) <dim:
                train_feature=temp
                for r in range(dim-len(temp)):
                    train_feature.append(0)
            else:
                train_feature=temp[:dim]
            #print(i_train,-1)
            train_features[i_train]=train_feature
            all_features[i_all]=train_feature
            train_labels[i_train]=-1
            all_labels[i_all]=-1
            
            i_train += 1
            i_all += 1
        i += 1
   
    #print(i_train)
    #print(i_test)
    #print(i_all)
    #print(train_features[0])
    print(str(fold),'median:',np.median(np.array(cell_len)))
    print(str(fold),'max:',np.max(np.array(cell_len)))
    return (np.array(train_features),np.array(train_labels),np.array(test_features),np.array(test_labels),np.array(all_features),np.array(all_labels))



def onehot(label_array,nClass):
    #print(label_array)
    convertedArr=np.zeros(shape=(len(label_array),nClass))
    i=0
    neg=0
    for label in label_array:
        print(label)
        if int(label) == -1:
            neg += 1
        convertedArr[i][int(label)]=1
        i += 1
    count = 0
    
    for item in convertedArr:
        if item[-1] == 1:
            count += 1
    #print('Number of negative test samples:',count)
    #print('Number of negative real samples:',neg)
    #print(convertedArr)
    return convertedArr
    

