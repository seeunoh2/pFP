import csv
import os
import numpy
HOME=os.path.expanduser('~')
# convert each feature vector into rank vector:
def getRanks(feature_vec):
    feature_vec=numpy.array(feature_vec)
    ranks_vec=[]
    for features in feature_vec.T:#transpose the list
        print
        order=features.argsort()
        ranks=order.argsort()
        ranks_vec.append(ranks)

    ranks_vec=numpy.array(ranks_vec)
    return ranks_vec.T #transpose again

def generateRanks(bag_file,isTest,addIndex):
    csv_reader = csv.reader(open(os.path.join(HOME,'feature',bag_file),'r'), delimiter = ',')
    csv_writer_feature=csv.writer(open(os.path.join(HOME,'feature','rank_'+bag_file),'w+'), delimiter = ',')
    fw_ranks=open(os.path.join(HOME,'feature',bag_file.split('.')[0]+'.txt'),'w+')
    features_list=[]
    features_label=[]
    for row in csv_reader:#write original rank feature libsvm file
        features_list.append(row[1:])
        features_label.append(row[0])

    feature_ranks = getRanks(features_list)
    for i in range(len(features_label)):  # write original rank feature libsvm file
        row_csv = []
        if not isTest:
            row = str(features_label[i])
            row_csv.append(str(features_label[i]))
        else:
            row = str(int(features_label[i])+addIndex)
            row_csv.append(str(int(features_label[i])+addIndex))
        f_index = 1
        for item in feature_ranks[i]:
            row = row + ' ' + str(f_index) + ':' + str(item)
            row_csv.append(item)
            f_index += 1
        fw_ranks.write(row)
        fw_ranks.write('\n')
        print row_csv
        csv_writer_feature.writerow(row_csv)


bag_file='bag-new-300-train.csv'
isTest=False
addIndex=50
generateRanks(bag_file,isTest,addIndex)
bag_file='bag-new-300-test.csv'
isTest=True
addIndex=50
generateRanks(bag_file,isTest,addIndex)


