'''
Created on Apr 12, 2017

@author: seeunoh
'''
import tflearn
import data
# Data loading and preprocessing
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
n_iter=20
exp = 'close'
n_epoch1 = 60
mon_instance = 300.0
folder='tamaraw_oh_100' # should be under ~/feature
r_train = 60.0
r_test = 40.0
nClass = 100
mon_instance = 300.0
gb = 'wf'
b_label = False
dim = 10000
for iter in range(n_iter):
    print('Start iter',iter,':::')
    (X, Y, testX, testY) = data.split_close_defense('feature/' + folder, 60.0, 40.0, 100.0, mon_instance, dim)

    if exp == 'open':
        nClass=nClass+1
    if b_label:
        nClass=2 ## in binary classification, we have only two labels, 0 or -1

    Y=data.onehot(Y, int(nClass))
    print(testY)
    testY=data.onehot(testY, int(nClass))
    print(exp,'nClass:',nClass)
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


    model.fit(X, Y, n_epoch=n_epoch1, validation_set=0.1,
                  show_metric=True, run_id='Fullnet_tamaraw_' + str(iter))

    # Save model
    model.save(os.path.join(model_path, 'Fullnet_tamaraw_' + str(iter) + '.tflearn'))

    prob_vector = model.predict(testX)
    # print(prob_vector)
    k_list = []
    # confidence thresholds
    confs = [0.1, 0.3, 0.5, 0.7, 0.9]
    # top k accuracy
    k_list = [1, 2, 3]
    for topK in k_list:
        for conf in confs:
            file = os.path.join(HOME, 'results',
                                'Fullnet_Tamaraw' + '_top_' + str(topK) + '_' + gb + str(dim) + '_' + str(
                                    nClass) + '_' + str(dim) + '_conf_' + str(conf) + '.txt')
            nn_metrics.getMetricsTopK(exp, prob_vector, testY, nClass, file, topK, conf, iter, 0,mon_instance*nClass)
