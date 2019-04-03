'''
Created on Jan 12, 2017

@author: seeunoh
'''
import os
import numpy as np
HOME=os.path.expanduser('~')


def split_ssl(folder_mon, folder_unmon, r_train, r_test, nClass, mon_instance, unClass, unmon_instance,
                          dim):
    ## r_train:r_test = 3:2, for example.
    PATH = os.path.join(HOME, folder_mon)  ## wf/feature/mon_90_90/TLS_100google_80_80.csv
    uPATH = os.path.join(HOME, folder_unmon)

    ## We need to uniformly random selection over each monitored class
    num_mtrain_instance = mon_instance * (
            r_train / (r_train + r_test))  ## number of monitored training instances for each class
    # print num_mtrain_instance
    num_umtrain_instance = unmon_instance * (
            r_train / (r_train + r_test))  ## number of monitored training instances for each class
    # print num_umtrain_instance
    

    mon_random = range(int(mon_instance))
    np.random.shuffle(mon_random)

    mon_train_ins = mon_random[:int(num_mtrain_instance)]
    mon_test_ins = mon_random[int(num_mtrain_instance):]

    unmon_random = range(int(unmon_instance))
    np.random.shuffle(unmon_random)

    unmon_train_ins = unmon_random[:int(num_umtrain_instance)]
    unmon_test_ins = unmon_random[int(num_umtrain_instance):]
    
    train_feature = []
    test_feature = []
    features = []
    train_label = []
    test_label = []
    labels = []
    print('Monitored training set partitioning...')
    for c in range(nClass):
        i = 0
        for instance in mon_train_ins:
            if os.path.exists(os.path.join(PATH, str(c) + '-' + str(instance))):
		#print(os.path.join(PATH,str(c)+'-'+str(instance)))
                feature = []
                f = open(os.path.join(PATH, str(c) + '-' + str(instance)), 'r')
                lines = f.readlines()
                for e in range(dim):
                    # for line in lines:
                    if e >= len(lines):
                        feature.append(0)
                        # all_feature.append(0)
                    else:
                        feature.append(int(lines[e].split('\t')[1].replace('\n', '')))
                        # all_feature.append(int(lines[e].split('\t')[1].replace('\n','')))

                        # all_feature.append(float(lines[e].split(' ')[1].replace('\n','')))
                train_label.append(c)
                train_feature.append(feature)
                labels.append(c)
                features.append(feature)
                i += 1
    print i
    print('Monitored testing set partitioning...')
    for c in range(nClass):
        i = 0
        for instance in mon_test_ins:
            if os.path.exists(os.path.join(PATH, str(c) + '-' + str(instance))):
                feature = []
                f = open(os.path.join(PATH, str(c) + '-' + str(instance)), 'r')
                lines = f.readlines()
                for e in range(dim):
                    # for line in lines:
                    if e >= len(lines):
                        feature.append(0)
                        # all_feature.append(0)
                    else:
                        feature.append(int(lines[e].split('\t')[1].replace('\n', '')))
                        # all_feature.append(int(lines[e].split('\t')[1].replace('\n','')))

                        # all_feature.append(float(lines[e].split(' ')[1].replace('\n','')))
                test_label.append(c)
                test_feature.append(feature)
                labels.append(c)
                features.append(feature)
                i += 1
    print i
    num_test_monitored = i * mon_instance
    print('Unmonitored training set partitioning...')
    i = 0
    for instance in unmon_train_ins:
        if os.path.exists(os.path.join(uPATH, str(instance))):
            feature = []
            f = open(os.path.join(uPATH, str(instance)), 'r')
            lines = f.readlines()
            for e in range(dim):
                # for line in lines:
                if e >= len(lines):
                    feature.append(0)
                    # all_feature.append(0)
                else:
            	    feature.append(int(lines[e].split('\t')[1].replace('\n', '')))
	    train_feature.append(feature)
            train_label.append(-1)
            features.append(feature)
            labels.append(-1)
            i += 1
    print i
    print('Unmonitored testing set partitioning...')
    i = 0
    for instance in unmon_test_ins:
        if os.path.exists(os.path.join(uPATH, str(instance))):
            feature = []
            f = open(os.path.join(uPATH, str(instance)), 'r')
            lines = f.readlines()
            for e in range(dim):
                # for line in lines:
                if e >= len(lines):
                    feature.append(0)
                    # all_feature.append(0)
                else:
                    feature.append(int(lines[e].split('\t')[1].replace('\n', '')))
		# all_feature.append(float(lines[e].split(' ')[1].replace('\n','')))
            test_feature.append(feature)
            test_label.append(-1)
            features.append(feature)
            labels.append(-1)
            i += 1

    print i
    print 'train_feature: ', len(train_feature)
    print 'train_label: ', len(train_label)
    print 'test_feature: ', len(test_feature)
    print 'test_label: ', len(test_label)
    print 'features: ', len(features)
    print 'labels: ', len(labels)
    print 'train_dim: ', len(train_feature[0])
    print 'test_dim: ', len(test_feature[0])
    # print train_feature
    # print test_feature
    return (
    np.array(train_feature), np.array(train_label), np.array(test_feature), np.array(test_label), np.array(features),
    np.array(labels))

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


