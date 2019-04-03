'''
Created on Apr 12, 2017

@author: seeunoh
'''
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

# Data loading and preprocessing
import data
import nn_metrics
import os
import tensorflow as tf

HOME=os.path.expanduser('~')
if not os.path.exists(os.path.join(HOME,'feature')):
    os.makedirs(HOME,'feature')
if not os.path.exists(os.path.join(HOME,'results')):
    os.makedirs(HOME,'results')
if not os.path.exists(os.path.join(HOME,'tflearn_saved_model')):
    os.makedirs(HOME,'tflearn_saved_model')
model_path=os.path.join(HOME,'tflearn_saved_model')
exp = 'open'
gb = 'kf'
file_mon = os.path.join(HOME, 'feature', 'Cont_100parent_100_100.csv')  # 'TLS_100google_80_80.csv'
file_unmon = os.path.join(HOME, 'feature', 'merged_back_cont.csv')  # 'merged_back.csv'
nClass=100
dim=2500#784
sub_dim=50
mon_instance = 100
unClass = 10000
unmon_instance = 1
n_epoch1 = 200 # 300
feature = 'resp'
reversed = False
b_label = False
if b_label:
    r = 'b'
else:
    r = 'm'


n_fold=20

for fold in range(n_fold):
    print('Start Fold',fold,' ...')

    (X,Y,testX,testY,allX,allY)=data.split_open_keyword(file_mon, file_unmon, fold, n_fold, nClass, mon_instance, unClass, unmon_instance, dim, reversed, b_label, feature)

    if exp == 'open':
        nClass=nClass+1
    if b_label:
        nClass=2 ## in binary classification, we have only two labels, 0 or -1


    print(len(X))
    print(len(testX))
    print(len(Y))
    print(len(testY))

    print(nClass)
    Y=data.onehot(Y, nClass)
    testY=data.onehot(testY, nClass)
    #print(Y)


    X = X.reshape([-1, sub_dim, sub_dim, 1])
    testX = testX.reshape([-1, sub_dim, sub_dim, 1])

    # Building convolutional network
    tf.reset_default_graph()
    network = input_data(shape=[None, sub_dim, sub_dim, 1], name='input')
    network = conv_2d(network, 32, 3, activation='relu', regularizer="L2")
    network = max_pool_2d(network, 2)
    network = local_response_normalization(network)


    network = fully_connected(network, 256, activation='tanh')
    network = dropout(network, 0.8)

    network = fully_connected(network, nClass, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=0.01,
                         loss='categorical_crossentropy', name='target')

    # Training
    model = tflearn.DNN(network, tensorboard_verbose=0)

    model.fit({'input': X}, {'target': Y}, n_epoch=n_epoch1, validation_set=0.1,
    snapshot_step=100, run_id='Conv_KF_' + str(fold))
    # Save model
    model.save(os.path.join(model_path, 'Conv_KF_' + str(fold) + '.tflearn'))
    prob_vector=model.predict(testX)
    #print(prob_vector)
    k_list=[]
    confs=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    if b_label: # Binary classification
        k_list=[1]
    else:
        k_list=[1,2,3,4,5]
    for topK in k_list:
        if not b_label:
            file=os.path.join(HOME,'results','Conv_KF_'+feature+'_'+r+'_'+str(topK)+'_'+exp+'_'+gb+str(dim)+'_'+str(mon_instance*(nClass-1))+'_'+str(unClass)+'_'+str(n_epoch1)+'.txt')
            for conf in confs:
                nn_metrics.getMetricsTopK(exp,prob_vector,testY,nClass,file,topK,conf,fold)
        else:
            file=os.path.join(HOME,'results','Conv_KF_'+feature+'_'+exp+'_'+gb+str(dim)+'_'+str(nClass)+'_'+str(unClass)+'_'+str(n_epoch1)+'.txt')
            nn_metrics.getMetrics(exp, prob_vector, testY, nClass,file)
