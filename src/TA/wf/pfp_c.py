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
import tflearn.datasets.mnist as mnist
import data
import nn_metrics
import os
import tensorflow as tf

HOME = os.path.expanduser('~')
if not os.path.exists(os.path.join(HOME,'feature')):
    os.makedirs(os.path.join(HOME,'feature'))
if not os.path.exists(os.path.join(HOME,'results')):
    os.makedirs(os.path.join(HOME,'results'))
if not os.path.exists(os.path.join(HOME,'tflearn_saved_model')):
    os.makedirs(os.path.join(HOME,'tflearn_saved_model'))
model_path=os.path.join(HOME,'tflearn_saved_model')
n_epoch1 = 30 #40
unClass = 40000
nClass = 100
dim = 5000  # 784
n_fold =20
exp = 'open'
gb = 'wf'
mon_instance = 300.0
unmon_instance = unClass
folder_mon = 'feature/new_mon2'# should be under ~/feature
folder_unmon = 'feature/new_new_unmon2'
r_train = 60.0
r_test = 40.0
b_label = False
if b_label:
    r = 'b'
else:
    r = 'm'
for fold in range(n_fold):
    print('Start Fold', fold, ' ...')
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
    testY = data.onehot(testY, nClass)
    # print(Y)

    X = X.reshape([-1, 1, dim, 1])
    testX = testX.reshape([-1, 1, dim, 1])

    # Building convolutional network
    tf.reset_default_graph()
    network = input_data(shape=[None, 1, dim, 1], name='input')
    network = conv_2d(network, 128, (1,12), activation='relu', regularizer="L2")
    network = max_pool_2d(network, 10)
    network = local_response_normalization(network)

    network = conv_2d(network, 128, (1,12), activation='relu', regularizer="L2")
    network = max_pool_2d(network, 10)
    network = local_response_normalization(network)

    network = fully_connected(network, 256, activation='tanh')
    network = dropout(network, 0.8)


    softmax = fully_connected(network, nClass, activation='softmax')

    sgd = tflearn.SGD(learning_rate=0.05, lr_decay=0.96, decay_step=1000)
    top_k = tflearn.metrics.Top_k(1)
    network = tflearn.regression(softmax, optimizer=sgd, metric=top_k, loss='categorical_crossentropy',
                                 name='target')

    # Training
    model = tflearn.DNN(network, tensorboard_verbose=0)
    model.fit({'input': X}, {'target': Y}, validation_set=0.1, n_epoch=n_epoch1,show_metric=True, snapshot_step=100,
              run_id='PFP_C_' + str(fold))
    # Save model
    model.save(os.path.join(model_path, 'PFP_C_' + str(fold) + '.tflearn'))
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
                                'PFP_C_' +  r + '_' + str(
                                    topK) + '_' + exp + '_' + gb + str(dim) + '_' + str(
                                    mon_instance * (nClass - 1)) + '_' + str(unClass) + '_' + str(
                                    n_epoch1) + '.txt')
            for conf in confs:
                nn_metrics.getMetricsTopK(exp, prob_vector, testY, nClass, file, topK, conf, fold, 0, 0)
        else:
            file = os.path.join(HOME, 'results',
                                'PFP_C_' +  exp + '_' + gb + str(dim) + '_' + str(
                                    mon_instance * (nClass - 1)) + '_' + str(unClass) + '_' + str(n_epoch1) + '.txt')
            nn_metrics.getMetrics(exp, prob_vector, testY, nClass, file)
