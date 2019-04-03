'''
Created on Apr 12, 2017

@author: seeunoh
'''
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization

# Data loading and preprocessing
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

n_epoch1 = 100
n_iter = 20
nClass = 100
folder = 'feature/walkiebatch-defended'
r_train = 60.0
r_test = 40.0
nClass = 100
mon_instance = 100.0
gb='wf'
b_label = False # Is it binary classification?
exp = 'close' # closed or open world experiment?
dim = 2500  # 784
for iter in range(n_iter):

    print('Start Iter', iter, ' ...')
    (X, Y, testX, testY) = data.split_close_walkie(folder, 60.0, 40.0, 100.0, mon_instance, dim)

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
    network = conv_2d(network, 32, 3, activation='tanh', regularizer="L2")
    network = max_pool_2d(network, 2)
    network = local_response_normalization(network)

    network = fully_connected(network, 256, activation='tanh')
    network = dropout(network, 0.8)

    softmax = fully_connected(network, nClass, activation='softmax')

    sgd = tflearn.SGD(learning_rate=0.1, lr_decay=0.96, decay_step=1000)
    top_k = tflearn.metrics.Top_k(3)
    network = tflearn.regression(softmax, optimizer=sgd, metric=top_k,
                                 loss='categorical_crossentropy', name='target')

    # Training
    model = tflearn.DNN(network, tensorboard_verbose=0)
    model.fit({'input': X}, {'target': Y}, validation_set=0.1, n_epoch=n_epoch1,
              snapshot_step=100, run_id='convnet_walkie')
    # Save model
    model.save(os.path.join(model_path, 'Conv_walkie_' + str(iter) + '.tflearn'))
    prob_vector = model.predict(testX)
    k_list = []
    # confidence thresholds
    confs = [0.1, 0.3, 0.5, 0.7, 0.9]
    # top k accuracy
    k_list = [1, 2, 3]
    for topK in k_list:
        for conf in confs:
            file = os.path.join(HOME, 'results',
                                'Conv_walkie_' + '_top_' + str(topK) + '_' + gb + str(dim) + '_' + str(
                                    nClass) + '_' + str(dim) + '.txt')

            nn_metrics.getMetricsTopK(exp, prob_vector, testY, nClass, file, topK, conf, iter, 0,mon_instance*nClass)
