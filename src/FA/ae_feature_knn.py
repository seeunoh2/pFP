# -*- coding: utf-8 -*-

""" Auto Encoder: feature extraction for knn
"""
from __future__ import division, print_function, absolute_import
import os
import tflearn
# Data loading and preprocessing
import data
import tensorflow as tf

HOME=os.path.expanduser('~')

if not os.path.exists(os.path.join(HOME,'AE_input')):
    os.makedirs(HOME,'AE_input')
if not os.path.exists(os.path.join(HOME,'tflearn_saved_model')):
    os.makedirs(HOME,'tflearn_saved_model')
model_path = os.path.join(HOME,'tflearn_saved_model')
min_dim = 80
nClass=100

unClass=10000
mon_instance = 150.0
unmon_instance = unClass
dim = 5000
# All input files are in wang's format
# Before running this script, first you need to partition your dataset into train and test (50:50)
# Here test dataset consists of two testing dataset.
mon_train='wang-format/ae_mon_train'
unmon_train='wang-format/ae_unmon_train'
mon_test='wang-format/ae_mon_test'
unmon_test='wang-format/ae_unmon_test'
gb='wf'
WFattack='knn'#'kfp'
file_name=os.path.join(HOME,'AE_input','AE_knn_'+WFattack+'_'+str(dim)+'_'+gb+'_'+str(nClass)+'_'+str(mon_instance)+'_'+str(unClass)+'_'+str(min_dim)+'.txt')

folder_mon_train = 'Trace/'+mon_train
folder_unmon_train = 'Trace/'+unmon_train
folder_mon_test = 'Trace/'+mon_test
folder_unmon_test = 'Trace/'+unmon_test
print(folder_mon_train)
print(folder_unmon_train)
print(folder_mon_test)
print(folder_unmon_test)

(X, Y, testX, testY) = data.split_pets19_compare(folder_mon_train, folder_unmon_train, folder_mon_test,
                                                 folder_unmon_test, nClass, mon_instance, unmon_instance, dim,
                                                 False)
print(len(X))
print(len(Y))
print(len(testX))
print(len(testY))
encoding_target=testX
encoding_target_label=testY

tf.reset_default_graph()
encoder = tflearn.input_data(shape=[None, dim])
encoder = tflearn.fully_connected(encoder, 1000, activation='relu',name='dense0')
encoder = tflearn.fully_connected(encoder, 784, activation='relu',name='dense1')
encoder = tflearn.fully_connected(encoder, min_dim, activation='relu',name='dense2')

# Building the decoder
decoder = tflearn.fully_connected(encoder, 784, activation='relu')
decoder = tflearn.fully_connected(decoder, dim)

# Regression, with mean square error(loss function)
# Adam optimizer: weight adjusted to the error every batch
net = tflearn.regression(decoder, optimizer='adam', learning_rate=0.001,
                         loss='mean_square', metric=None)

# Training the auto encoder
model = tflearn.DNN(net, tensorboard_verbose=0)

model.fit(X, X, n_epoch=20, validation_set=0.1, run_id="auto_encoder_knn"+str(iter), batch_size=256)
# Save model
model.save(os.path.join(model_path, 'ae_feature_knn'+str(iter)+'.tflearn'))

# New model, re-using the same session, for weights sharing
# Writing inputs....
encoding_model = tflearn.DNN(encoder, session=model.session)
#encoding_model.fit(X, X, n_epoch=10, validation_set=(testX, testX), run_id="auto_encoder", batch_size=256)
f=open(file_name,'w+')
for i in range(int(len(testX))):
    #print(Y[i])
    #f.write(Y[i])
    k=1

    try:
        line=str(int(encoding_target_label[i]))
    except IndexError:
        #print(i)
        print('Index Error')

    for j in encoding_model.predict([encoding_target[i]])[0]:
        line = line+' '+str(k)+':'+str(j)

        k += 1
    #print(line)
    f.write(line)
    f.write('\n')
    

