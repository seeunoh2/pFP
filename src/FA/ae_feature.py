# -*- coding: utf-8 -*-

""" Auto Encoder: Feature extraction for kFP and CUMUL
"""
from __future__ import division, print_function, absolute_import
import os
import tflearn
import data
import tensorflow as tf

HOME=os.path.expanduser('~')

if not os.path.exists(os.path.join(HOME,'AE_input')):
    os.makedirs(HOME,'AE_input')
if not os.path.exists(os.path.join(HOME,'tflearn_saved_model')):
    os.makedirs(HOME,'tflearn_saved_model')
model_path = os.path.join(HOME,'tflearn_saved_model')
# Encoded representation dimension
min_dim = 100 # 10,20,40,80,100

nClass=100
n_fold=10
mon_instance = 150.0
unmon_instance = 10000
unClass=10000
# Original dimension
dim = 5000



# Number of total instances in to-be-encoded
gb='wf'
WFattack='kfp'#'kfp' or 'cumul'
exp=''
file_name=os.path.join(HOME,'AE_input','AE_'+WFattack+'_'+str(dim)+'_'+gb+'_'+str(nClass)+'_'+str(mon_instance)+'_'+str(unClass)+'_'+str(min_dim)+'.txt')



# All input files are in wang's format
# Before running this script, first you need to partition your dataset into train and test (50:50)
# Here test dataset consists of two testing dataset.
mon_train='wang-format/ae_mon_train'
unmon_train='wang-format/ae_unmon_train'
mon_test='wang-format/ae_mon_test'
unmon_test='wang-format/ae_unmon_test'

#for iter in range(2):
folder_mon_train = 'Trace/'+mon_train
folder_unmon_train = 'Trace/'+unmon_train
folder_mon_test = 'Trace/'+mon_test
folder_unmon_test = 'Trace/'+unmon_test
#folder_mon_train = 'Trace/'+mon_train+str(iter+1)
#folder_unmon_train = 'Trace/'+unmon_train+str(iter+1)
#folder_mon_test = 'Trace/'+mon_test+str(iter+1)
#folder_unmon_test = 'Trace/'+unmon_test+str(iter+1)
print(folder_mon_train)
print(folder_unmon_train)
print(folder_mon_test)
print(folder_unmon_test)

(X,Y,testX,testY)=data.split_pets19_compare(folder_mon_train, folder_unmon_train, folder_mon_test, folder_unmon_test, nClass,mon_instance,unmon_instance,dim,False)
print(len(X))
print(len(Y))
print(len(testX))
print(len(testY))


encoding_target=testX
encoding_target_label=testY

tf.reset_default_graph()
encoder = tflearn.input_data(shape=[None, dim])
encoder = tflearn.fully_connected(encoder, 256, activation='relu',name='dense1')
encoder = tflearn.fully_connected(encoder, min_dim, activation='relu',name='dense2')

# Building the decoder
decoder = tflearn.fully_connected(encoder, 256, activation='relu')
decoder = tflearn.fully_connected(decoder, dim)

# Regression, with mean square error(loss function)
# Adam optimizer: weight adjusted to the error every batch
net = tflearn.regression(decoder, optimizer='adam', learning_rate=0.001,
                         loss='mean_square', metric=None)

# Training the auto encoder
model = tflearn.DNN(net, tensorboard_verbose=0)

model.fit(X, X, n_epoch=10, validation_set=0.1, run_id="auto_encoder"+str(iter), batch_size=256)
# Save model
model.save(os.path.join(model_path,'ae_feature'+str(iter)+'.tflearn'))



# Writing AE inputs....
encoding_model = tflearn.DNN(encoder, session=model.session)
num_ins = len(testX)

f=open(file_name,'w+')
#for i in range(int(total_ins)):
for i in range(int(num_ins)):
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
    

