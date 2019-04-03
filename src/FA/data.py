import os
import numpy as np
import random

HOME = os.path.expanduser('~')


def split_pets19_compare(folder_mon_train, folder_unmon_train, folder_mon_test, folder_unmon_test, nClass, mon_instance,
                         unmon_instance,
                         dim, b_label):
    if b_label:
        print("It's binary classification!!!")
    tr_PATH = os.path.join(HOME, folder_mon_train)  ## wf/feature/mon_90_90/TLS_100google_80_80.csv
    tr_uPATH = os.path.join(HOME, folder_unmon_train)
    te_PATH = os.path.join(HOME, folder_mon_test)
    te_uPATH = os.path.join(HOME, folder_unmon_test)

    # print num_umtest_instance
    train_feature = []
    test_feature = []
    train_label = []
    test_label = []

    print('Monitored training set extract...')
    for file in os.listdir(tr_PATH):
        f=open(os.path.join(tr_PATH, file), 'r')
        feature=[]
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
        #print file.split('-')[0]
        if not b_label:
            train_label.append(file.split('-')[0])

        else:
            train_label.append(0)

        train_feature.append(feature)
    print(len(train_feature))


    print('Monitored testing set extract...')
    for file in os.listdir(te_PATH):
        f=open(os.path.join(tr_PATH, file), 'r')
        feature=[]
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
        if not b_label:
            test_label.append(file.split('-')[0])

        else:
            test_label.append(0)

        test_feature.append(feature)
    print(len(test_feature))

    print('Unmonitored training set extract...')
    for file in os.listdir(tr_uPATH):

        feature = []

        f = open(os.path.join(tr_uPATH, file), 'r')
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
    print(len(train_feature))


    print('Unmonitored testing set extract...')
    for file in os.listdir(te_uPATH):

        feature = []

        f = open(os.path.join(te_uPATH, file), 'r')
        lines = f.readlines()
        for e in range(dim):
            # for line in lines:
            if e >= len(lines):
                feature.append(0)
                # all_feature.append(0)
            else:
                feature.append(int(lines[e].split('\t')[1].replace('\n', '')))
        test_feature.append(feature)
        test_label.append(-1)
    print(len(test_feature))

    return (np.array(train_feature), np.array(train_label), np.array(test_feature), np.array(test_label))
