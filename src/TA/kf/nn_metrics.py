'''
Created on Apr 14, 2017

@author: seeunoh
'''
import numpy as np
import os
from sklearn import metrics
HOME=os.path.expanduser('~')
def getMetrics(exp,prob_vector,true_vector,nClass,file,fold,conf): #true_vector should be in one-hot format
    fw=open(file,'a')
    fw.write('iter='+str(fold)+', conf='+str(conf))
    fw.write('\n')
    tp=0.0
    tn=0.0
    fp=0.0
    ffp=0.0
    fn=0.0
    ttp=0.0
    num_monitored=0.0
    if exp == 'close':
        i=0
        for pred in prob_vector:#For each probability vector per instance in testing data
            predicted=pred.tolist().index(max(pred))
            true=np.array(true_vector[i]).tolist().index(1)
            if predicted == true:
                tp += 1
            fw.write(str(i)+','+str(predicted)+','+str(true))
            fw.write('\n')
            i += 1
            #for prob in pred: #for each prediction for each instance
        print('accuracy=',str(tp/len(true_vector)))
        fw.write('accuracy='+str(tp/len(true_vector)))
        fw.write('\n')
    else: # open world metrics
        i=0
        neg=0
        for pred in prob_vector:#prob_vector:#For each probability vector per instance in testing data


            #print('predicted:',predicted)
            #if predicted == (nClass-1):
            #    print('prediction equals negative')
            #print(pred)
            true=np.array(true_vector[i]).tolist().index(1)
            if max(pred) < conf:
                '''
                ## detected as others
                '''
                if true == 0: ## Monitored
                    predicted=-1
                else:
                    predicted=0
            else:
                '''
                ## detected as it is
                '''
                predicted = pred.tolist().index(max(pred))
            
            if predicted == true: ## TP or TN
                if true == (nClass-1): #negative
                    tn += 1
                else:
                    tp += 1
                    ttp += 1
                    num_monitored += 1
            else: ## FP or FN
                if true == (nClass-1): ## detected as positive but actual is negative
                    fp += 1
                    ffp += 1
                else:
                    if predicted != (nClass-1): ## confusion between monitored classes
                        #print('it is not fn')
                        tp += 1
                        ffp += 1
                    else:
                        fn += 1
                    num_monitored += 1
            if true == (nClass-1):# negative
                true=-1
            if predicted == (nClass-1):# negative
                predicted=-1
            fw.write(str(i)+','+str(predicted)+','+str(true))
            fw.write('\n')
            
            i += 1
        fw.close()
        print(ttp,tp,tn,fp,fn)
        


        return ttp/(ttp+fn),ffp/(ffp+tn)

def getMetricsTopK(exp,prob_vector,true_vector,nClass,file,topK,conf_thr,fold,unClass,num_monitored): #true_vector should be in one-hot format
    fw=open(file,'a')
    fr=open(file,'r')
    if len(fr.readlines())==0:
        fw.write('iter:conf=conf_thres wmacc,multi-tpr,multi-fpr,binary-tpr,binary-fpr,precision,binary-bdr,multi-bdr,wmacc-fpr')
    fr.close()
    fw_roc=open(os.path.join(HOME,'results',file.split('.')[0]+'_roc.txt'),'a')
    fw_roc.write('iter='+str(fold))
    fw_roc.write('\n')
    
    tp=0.0
    tn=0.0
    fp=0.0
    fn=0.0
    ttp=0.0
    ffp=0.0
    
    
    n=0
    p=0
    for v in true_vector:
        if v[-1]==1:
            n += 1
        else:
            p += 1
    print('num of Neg data:',n)
    print('num of Pos data:',p)
    if exp == 'close':
        '''
            ### close world metrics
        '''
        i=0
        for pred in prob_vector:#For each probability vector per instance in testing data
            top_list=[]
            '''
            ## Make top_list based on conf_thr
            '''
            for top in sorted(pred,reverse=True)[:topK]:
                if top > conf_thr:
                    top_list.append(np.array(pred).tolist().index(top))
                    #top_list_prob.append(top)
            predicted=np.array(pred).tolist().index(max(pred))
            print(top_list)
            true=np.array(true_vector[i]).tolist().index(1)
            if len(top_list) != 0:
                if true in top_list:# and all(i > conf_thr for i in top_list_prob):
                    tp += 1
                    predicted=true
                else:
                    predicted=top_list[0]
            
            i += 1
            
            #for prob in pred: #for each prediction for each instance
            fw_roc.write(str(i) + ',' + str(predicted) + ',' + str(true))
            fw_roc.write('\n')
        fw.write(str(fold)+': conf='+str(conf_thr)+' '+str(tp/len(true_vector)))
        fw.write('\n')

        fw.close()
        fw_roc.close()
        print('accuracy=',tp/len(true_vector))

    else:
        '''
            ### open world metrics
        '''
        i=0
        neg=0
        print('size of each prediction prob vector=',len(prob_vector[0]))
        for pred in prob_vector:#For each probability vector per instance in testing data
            top_list=[]
            #top_list_prob=[]
            
            for top in sorted(pred,reverse=True)[:topK]:
                if top > conf_thr:
                    top_list.append(np.array(pred).tolist().index(top))

            predicted=pred.tolist().index(max(pred))
            true=np.array(true_vector[i]).tolist().index(1)
            if len(top_list) == 0:
                '''
                ## no top-k labels whose prob > conf_thres, detect as "others"
                '''

                if true == (nClass-1):
                    '''
                    # if true label is negative, it is predicted as negative
                    '''
                    for top in sorted(pred, reverse=True)[:topK]:
                        if np.array(pred).tolist().index(top) != (nClass - 1):
                            predicted = np.array(pred).tolist().index(top)
                            break
                    tn += 1
                else:
                    '''
                    # if true label is positive,
                    '''
                    predicted = -1
                    fn += 1
            else:
                
                if true in top_list:
                    '''
                    # True Alarm
                    '''
                    #if all(i > conf_thr for i in top_list_prob): ## for confidence threshold,
                    predicted=true
                    if true == (nClass-1): #negative
                         tn += 1
                    else:
                         tp += 1
                         ttp += 1
                else:
                    '''
                    # False Alarm
                    '''
                    if true == (nClass-1):
                        predicted=top_list[0]
                        fp += 1
                        ffp += 1
                    else:
                        if (nClass-1) in top_list:
                            '''
                            # if there is a negative label, it is fn
                            '''
                            predicted=(nClass-1)
                            fn += 1
                        else:
                            '''
                            # if all labels in top list are positive, it is tp for binary or fp for multi.
                            '''
                            tp += 1
                            ffp += 1
                            predicted=top_list[0]
                        #num_monitored += 1
            if true == (nClass-1):# negative
                true=-1
            if predicted == (nClass-1):# negative
                predicted=-1
            fw_roc.write(str(i)+','+str(predicted)+','+str(true))
            fw_roc.write('\n')
            
            i += 1
        


        pbm=(tp+fn)/total#(unClass+num_monitored)
        pbu=(tn+fp)/total#(unClass+num_monitored)
        if (ttp+fn) == 0:
            wmtpr=0
        else:
            wmtpr=ttp/(ttp+fn)
        if (ffp+tn) == 0:
            wmfpr=0
        else:
            wmfpr=ffp/(ffp+tn)
        if (tp+fn) == 0:
            tpr=0
        else:
            tpr=tp/(tp+fn)
        if (fp+tn) == 0:
            fpr=0
        else:
            fpr=fp/(fp+tn)
        if (tp+fp) == 0:
            pre=0
        else:
            pre=tp/(tp+fp)
        if (tpr*pbm+fpr*pbu)==0:
            bi_bdr=0
        else:
            bi_bdr=tpr*pbm/(tpr*pbm+fpr*pbu)
        if (wmtpr*pbm+wmfpr*pbu)==0:
            mul_bdr=0
        else:
            mul_bdr=wmtpr*pbm/(wmtpr*pbm+wmfpr*pbu)
        
        fw.write('\n')
        fw.write(str(fold)+': conf='+str(conf_thr)+' '+str(wmtpr)+', '+str(wmfpr)+', '+str(tpr)+', '+str(fpr)+', '+str(pre)+', '+str(bi_bdr)+', '+str(mul_bdr))
        fw.write('\n')

        fw.close()
        fw_roc.close()


