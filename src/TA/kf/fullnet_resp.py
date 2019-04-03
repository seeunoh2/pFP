'''
Created on Apr 12, 2017

@author: seeunoh
'''
import tflearn
import data
# Data loading and preprocessing
import tflearn.datasets.mnist as mnist
#X, Y, testX, testY = mnist.load_data(one_hot=True)
import nn_metrics
import os
import tensorflow as tf
import numpy as np

HOME=os.path.expanduser('~')
if not os.path.exists(os.path.join(HOME,'feature')):
    os.makedirs(HOME,'feature')
if not os.path.exists(os.path.join(HOME,'results')):
    os.makedirs(HOME,'results')
if not os.path.exists(os.path.join(HOME,'tflearn_saved_model')):
    os.makedirs(HOME,'tflearn_saved_model')
model_path=os.path.join(HOME,'tflearn_saved_model')
dim = 784
n_epoch1 = 500
nClass=100
gb='kf'
exp='open'
feature='resp'#'cumul'
file_mon = os.path.join(HOME, 'feature', 'Cont_100parent_100_100.csv')  # 'TLS_100google_80_80.csv'
file_unmon = os.path.join(HOME, 'feature', 'merged_back_cont.csv')  # 'merged_back.csv'
mon_instance=100
unClass=10000
unmon_instance=1
reversed=False
b_label=False
if b_label:
    r='b'
else:
    r='m'
n_fold=20
for fold in range(n_fold):
    print('Start Fold',fold,':::')


    (X,Y,testX,testY,allX,allY)=data.split_open_keyword(file_mon, file_unmon, fold, n_fold, nClass, mon_instance, unClass, unmon_instance, dim, reversed, b_label, feature)
    if exp == 'open':
        nClass=nClass+1
    if b_label:
        nClass=2 ## in binary classification, we have only two labels, 0 or -1
    preY=Y
    Y=data.onehot(Y, nClass)
    print(testY)
    testY=data.onehot(testY, nClass)
    print(exp,'nClass:',nClass)
    # Building deep neural network
    tf.reset_default_graph()
    input_layer = tflearn.input_data(shape=[None, dim])
    dense1 = tflearn.fully_connected(input_layer, 256, activation='tanh',
                                     regularizer='L2', weight_decay=0.001)
    dropout1 = tflearn.dropout(dense1, 0.8)
    dense2 = tflearn.fully_connected(dropout1, 256, activation='tanh',
                                     regularizer='L2', weight_decay=0.001)
    dropout2 = tflearn.dropout(dense2, 0.8)
    softmax = tflearn.fully_connected(dropout2, nClass, activation='softmax')

    # Regression using SGD with learning rate decay and Top-3 accuracy
    sgd = tflearn.SGD(learning_rate=0.1, lr_decay=0.96, decay_step=1000)
    top_k = tflearn.metrics.Top_k(3)
    net = tflearn.regression(softmax, optimizer=sgd, metric=top_k,
                             loss='categorical_crossentropy')

    print(len(X))
    print(len(Y))

    # Training
    print(exp,"experiment, number of classes:,",nClass)
    model = tflearn.DNN(net, tensorboard_verbose=0)

    model.fit(X, Y, n_epoch=n_epoch1, validation_set=0.1, run_id='Fullnet_KF_' + str(fold))
    # Save model
    model.save(os.path.join(model_path, 'Fullnet_KF_' + str(fold) + '.tflearn'))

    prob_vector=model.predict(testX)
    k_list = []
    confs = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    if b_label:  # Binary classification
        k_list = [1]
    else:
        k_list = [1, 2, 3, 4, 5]
    for topK in k_list:
        if not b_label:
            file = os.path.join(HOME, 'results',
                                'Fullnet_KF_' + feature + '_' + r + '_' + str(topK) + '_' + exp + '_' + gb + str(
                                    dim) + '_' + str(mon_instance * (nClass - 1)) + '_' + str(unClass) + '_' + str(
                                    n_epoch1) + '.txt')
            for conf in confs:
                nn_metrics.getMetricsTopK(exp, prob_vector, testY, nClass, file, topK, conf, fold)
        else:
            file = os.path.join(HOME, 'results',
                                'Fullnet_KF_' + feature + '_' + exp + '_' + gb + str(dim) + '_' + str(nClass) + '_' + str(
                                    unClass) + '_' + str(n_epoch1) + '.txt')
            nn_metrics.getMetrics(exp, prob_vector, testY, nClass, file)
