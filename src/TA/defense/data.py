'''
Created on Jan 12, 2017

@author: seeunoh
'''
import os
import numpy as np
HOME=os.path.expanduser('~')

def split_close_tamaraw(folder, r_train, r_test, nClass, mon_instance, dim):
    ## r_train:r_test = 3:2, for example.

    if 'normal_rcv_181128_111112' not in folder:
	PATH = os.path.join(HOME, folder)  ## wf/feature/mon_90_90/TLS_100google_80_80.csv
    else:
	PATH = folder
    ## We need to uniformly random selection over each monitored class
    num_mtrain_instance = mon_instance * (
    r_train / (r_train + r_test))  ## number of monitored training instances for each class
    # print num_mtrain_instance
    
    mon_random = range(int(mon_instance))
    np.random.shuffle(mon_random)

    mon_train_ins = mon_random[:int(num_mtrain_instance)]
    mon_test_ins = mon_random[int(num_mtrain_instance):]

    # print num_umtest_instance
    train_feature = []
    test_feature = []
    features = []
    train_label = []
    test_label = []
    labels = []
    print('Monitored training set partitioning...')
    for c in range(int(nClass)):
        i = 0
        for instance in mon_train_ins:
            file_path=os.path.join(PATH, str(c) + '-' + str(instance))
            if os.path.exists(file_path):
            #if os.path.exists(os.path.join(PATH, str(c) + '-' + str(instance))):
                #print os.path.join(PATH, str(c) + '-' + str(instance))
                feature = []
                f = open(file_path, 'r')
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
    for c in range(int(nClass)):
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
    # print i_train
    # print i_test
    return (np.array(train_feature), np.array(train_label), np.array(test_feature), np.array(test_label))


def split_close_wtfpad(folder, r_train, r_test, nClass, mon_instance, dim):
    ## r_train:r_test = 3:2, for example.

    if 'normal_rcv_181128_111112' not in folder:
        PATH = os.path.join(HOME, folder)  ## wf/feature/mon_90_90/TLS_100google_80_80.csv
    else:
        PATH = folder
    ## We need to uniformly random selection over each monitored class
    num_mtrain_instance = mon_instance * (
            r_train / (r_train + r_test))  ## number of monitored training instances for each class
    # print num_mtrain_instance
    
    mon_random = range(len(mon_instance))
    np.random.shuffle(mon_random)

    mon_train_ins = mon_random[:int(num_mtrain_instance)]
    mon_test_ins = mon_random[int(num_mtrain_instance):]
    # print num_umtest_instance
    train_feature = []
    test_feature = []
    features = []
    train_label = []
    test_label = []
    labels = []
    print('Monitored training set partitioning...')
    for c in range(int(nClass)):
        i = 0
        for instance in mon_train_ins:
            file_path = os.path.join(PATH, str(c) + '-' + str(instance))
            if os.path.exists(file_path):
                # if os.path.exists(os.path.join(PATH, str(c) + '-' + str(instance))):
                # print os.path.join(PATH, str(c) + '-' + str(instance))
                feature = []
                f = open(file_path, 'r')
                lines = f.readlines()
                for e in range(dim):
                    # for line in lines:
                    if e >= len(lines):
                        feature.append(0)  # all_feature.append(0)
                    else:
                        feature.append(int(lines[e].split('\t')[1].replace('\n',
                                                                           '')))  # all_feature.append(int(lines[e].split('\t')[1].replace('\n','')))

                        # all_feature.append(float(lines[e].split(' ')[1].replace('\n','')))
                train_label.append(c)
                train_feature.append(feature)
                labels.append(c)
                features.append(feature)
                i += 1
    print i
    print('Monitored testing set partitioning...')
    for c in range(int(nClass)):
        i = 0
        for instance in mon_test_ins:
            if os.path.exists(os.path.join(PATH, str(c) + '-' + str(instance))):
                feature = []
                f = open(os.path.join(PATH, str(c) + '-' + str(instance)), 'r')
                lines = f.readlines()
                for e in range(dim):
                    # for line in lines:
                    if e >= len(lines):
                        feature.append(0)  # all_feature.append(0)
                    else:
                        feature.append(int(lines[e].split('\t')[1].replace('\n',
                                                                           '')))  # all_feature.append(int(lines[e].split('\t')[1].replace('\n','')))

                        # all_feature.append(float(lines[e].split(' ')[1].replace('\n','')))
                test_label.append(c)
                test_feature.append(feature)
                labels.append(c)
                features.append(feature)
                i += 1
    print i
    # print i_train
    # print i_test
    return (np.array(train_feature), np.array(train_label), np.array(test_feature), np.array(test_label))

def split_close_walkie(folder, r_train, r_test, nClass, mon_instance, dim):
    ## r_train:r_test = 3:2, for example.
    PATH = os.path.join(HOME, folder)  ## wf/feature/mon_90_90/TLS_100google_80_80.csv


    ## We need to uniformly random selection over each monitored class
    num_mtrain_instance = mon_instance * (
    r_train / (r_train + r_test))  ## number of monitored training instances for each class
    # print num_mtrain_instance
    
    mon_random = range(len(mon_instance))
    np.random.shuffle(mon_random)

    mon_train_ins = mon_random[:int(num_mtrain_instance)]
    mon_test_ins = mon_random[int(num_mtrain_instance):]
    # print num_umtest_instance
    train_feature = []
    test_feature = []
    features = []
    train_label = []
    test_label = []
    labels = []
    print('Monitored training set partitioning...')
    for c in range(int(nClass)):
        i = 0
        for instance in mon_train_ins:
            file_path=os.path.join(PATH, str(c) + '-' + str(instance)+'.cell')
            #print(file_path)
            if os.path.exists(file_path):
                #print(file_path)
            #if os.path.exists(os.path.join(PATH, str(c) + '-' + str(instance))):
                #print os.path.join(PATH, str(c) + '-' + str(instance))
                feature = []
                f = open(file_path, 'r')
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
    for c in range(int(nClass)):
        i = 0
        for instance in mon_test_ins:
            if os.path.exists(os.path.join(PATH, str(c) + '-' + str(instance)+'.cell')):
                feature = []
                f = open(os.path.join(PATH, str(c) + '-' + str(instance)+'.cell'), 'r')
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
    # print i_train
    # print i_test
    return (np.array(train_feature), np.array(train_label), np.array(test_feature), np.array(test_label))

def split_close_buflo(folder, r_train, r_test, nClass, mon_instance, dim):
    ## r_train:r_test = 3:2, for example.
    if 'normal' not in folder:
    	PATH = os.path.join(HOME, folder)  ## wf/feature/mon_90_90/TLS_100google_80_80.csv
    else:
	PATH = folder

    ## We need to uniformly random selection over each monitored class
    num_mtrain_instance = mon_instance * (
    r_train / (r_train + r_test))  ## number of monitored training instances for each class
    # print num_mtrain_instance
    
    mon_random = range(len(mon_instance))
    np.random.shuffle(mon_random)

    mon_train_ins = mon_random[:int(num_mtrain_instance)]
    mon_test_ins = mon_random[int(num_mtrain_instance):]
    # print num_umtest_instance
    train_feature = []
    test_feature = []
    features = []
    train_label = []
    test_label = []
    labels = []
    print('Monitored training set partitioning...')
    for c in range(int(nClass)):
        i = 0
        for instance in mon_train_ins:
            file_path=os.path.join(PATH, str(c) + '-' + str(instance))
            #print(file_path)
            if os.path.exists(file_path):
                #print(file_path)
            #if os.path.exists(os.path.join(PATH, str(c) + '-' + str(instance))):
                #print os.path.join(PATH, str(c) + '-' + str(instance))
                feature = []
                f = open(file_path, 'r')
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
    for c in range(int(nClass)):
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
    # print i_train
    # print i_test
    return (np.array(train_feature), np.array(train_label), np.array(test_feature), np.array(test_label))

def split_close_defense(folder, r_train, r_test, nClass, mon_instance, dim):
    ## r_train:r_test = 3:2, for example.
    if 'normal' not in folder:
    	PATH = os.path.join(HOME, folder)  ## wf/feature/mon_90_90/TLS_100google_80_80.csv
    else:
	PATH = folder

    ## We need to uniformly random selection over each monitored class
    num_mtrain_instance = mon_instance * (
    r_train / (r_train + r_test))  ## number of monitored training instances for each class
    # print num_mtrain_instance
    
    mon_random = range(len(mon_instance))
    np.random.shuffle(mon_random)

    mon_train_ins = mon_random[:int(num_mtrain_instance)]
    mon_test_ins = mon_random[int(num_mtrain_instance):]
    # print num_umtest_instance
    train_feature = []
    test_feature = []
    features = []
    train_label = []
    test_label = []
    labels = []
    print('Monitored training set partitioning...')
    for c in range(int(nClass)):
        i = 0
        for instance in mon_train_ins:
            file_path=os.path.join(PATH, str(c) + '-' + str(instance))
            #print(file_path)
            if os.path.exists(file_path):
                #print(file_path)
            #if os.path.exists(os.path.join(PATH, str(c) + '-' + str(instance))):
                #print os.path.join(PATH, str(c) + '-' + str(instance))
                feature = []
                f = open(file_path, 'r')
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
    for c in range(int(nClass)):
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
    # print i_train
    # print i_test
    return (np.array(train_feature), np.array(train_label), np.array(test_feature), np.array(test_label))

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
