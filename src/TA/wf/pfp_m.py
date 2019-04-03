'''
Created on Apr 12, 2017

@author: seeunoh
'''
import tflearn
import data
# Data loading and preprocessing
import tflearn.datasets.mnist as mnist
# X, Y, testX, testY = mnist.load_data(one_hot=True)
import nn_metrics
import os
import tensorflow as tf
import numpy as np
import argparse
from sklearn import metrics
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

HOME = os.path.expanduser('~')
if not os.path.exists(os.path.join(HOME,'feature')):
    os.makedirs(os.path.join(HOME,'feature'))
if not os.path.exists(os.path.join(HOME,'results')):
    os.makedirs(os.path.join(HOME,'results'))
if not os.path.exists(os.path.join(HOME,'tflearn_saved_model')):
    os.makedirs(os.path.join(HOME,'tflearn_saved_model'))
model_path=os.path.join(HOME,'tflearn_saved_model')
gb = 'wf'
b_label = False
n_epoch1 = 50
unClass = 20000.0
nClass = 100
mon_instance = 300.0
exp='open'
unmon_instance = unClass
dim = 5000
folder_mon = 'wang-format/new_mon/new_mon2'#100mon_90_90'
folder_unmon = 'wang-format/new_new_unmon2'
r_train = 60.0
r_test = 40.0
n_iter = 20

for iter in range(n_iter):
    print('Start iter', iter, ':::')
    (X, Y, testX, testY, allX, allY) = data.split_pfp(folder_mon, folder_unmon, r_train, r_test, nClass,
                                                      mon_instance, unClass, unmon_instance, dim, b_label)
    if exp == 'open':
        nClass = nClass + 1
    if b_label:
        nClass = 2  ## in binary classification, we have only two labels, 0 or -1
    print(len(X))
    print(len(testX))
    print(len(Y))
    print(len(testY))

    print(nClass)
    Y = data.onehot(Y, nClass)
    print(testY)
    testY = data.onehot(testY, int(nClass))
    print(exp, 'nClass:', nClass)
    # Building deep neural network

    tf.reset_default_graph()
    input_layer = tflearn.input_data(shape=[None, dim])
    dense1 = tflearn.fully_connected(input_layer, 1345, activation='tanh',
                                    weight_decay=0.0)
    dropout1 = tflearn.dropout(dense1, 0.3)
    dense2 = tflearn.fully_connected(dropout1, 2315, activation='tanh',
                                      weight_decay=0.0)
    dropout2 = tflearn.dropout(dense2, 0.5)

    dense3 = tflearn.fully_connected(dropout2, 2596, activation='tanh',
                                     weight_decay=0.0)
    dropout3 = tflearn.dropout(dense3, 0.5)

    softmax = tflearn.fully_connected(dropout3, int(nClass), activation='softmax')

    # Regression using SGD with learning rate decay and Top-3 accuracy
    sgd = tflearn.SGD(learning_rate=0.03)
    top_k = tflearn.metrics.Top_k(3)
    net = tflearn.regression(softmax, optimizer=sgd,
                             loss='categorical_crossentropy')

    print(len(X))
    print(len(Y))

    # Training
    print(exp, "experiment, number of classes:,", nClass)
    model = tflearn.DNN(net, tensorboard_verbose=0)
    model.fit(X, Y, batch_size=47, n_epoch=n_epoch1, validation_set=0.1)
    # Save model
    model.save(os.path.join(model_path, 'PFP_M_' + str(iter) + '.tflearn'))

    prob_vector = model.predict(testX)
    # print(prob_vector)
    k_list = []
    confs = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    if b_label:  ## Binary classification
        k_list = [1]
    else:
        k_list = [1, 2, 3, 4, 5]
    for topK in k_list:
        if not b_label:
            file = os.path.join(HOME, 'results',
                                'PFP_M_' + str(topK) + '_' + exp + '_' + gb + str(dim) + '_' + str(
                                    mon_instance * (nClass - 1)) + '_' + str(unClass) + '_' + str(n_epoch1) + '.txt')
            for conf in confs:
                nn_metrics.getMetricsTopK(exp, prob_vector, testY, nClass, file, topK, conf, iter, 0, 0)
        else:
            file = os.path.join(HOME, 'results', 'PFP_M_' + exp + '_' + gb + str(dim) + '_' + str(
                mon_instance * (nClass - 1)) + '_' + str(unClass) + '_' + str(n_epoch1) + '.txt')
    for conf in confs:
                nn_metrics.getMetricsTopK(exp, prob_vector, testY, nClass, file, topK, conf, iter, 0, 0)


