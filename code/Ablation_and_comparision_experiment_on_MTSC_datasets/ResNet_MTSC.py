# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 21:30:56 2022

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 11:59:16 2020

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 11:53:43 2020

@author: Administrator
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 20:11:19 2016

@author: stephen
"""
 
# from __future__ import print_function
import os
print(os.path.abspath(os.path.join(os.getcwd(), "../..")))
last_last_path=os.path.abspath(os.path.join(os.getcwd(), "../.."))

print(os.path.abspath(os.path.join(os.getcwd(), "..")))
last_path=os.path.abspath(os.path.join(os.getcwd(), "..")) 
from tensorflow import keras
import numpy as np
import pandas as pd
import os
import pickle
import scipy as sp
import datetime
#data = sp.genfromtxt("filename.tsv", delimiter="\t")
np.random.seed(813306)

def build_resnet(input_shape, n_feature_maps, nb_classes):
    print ('build conv_x')
    x = keras.layers.Input(shape=(input_shape))
    conv_x = keras.layers.BatchNormalization()(x)
    conv_x = keras.layers.Conv2D(n_feature_maps, 8, strides=1, padding='same')(conv_x)
    conv_x = keras.layers.BatchNormalization()(conv_x)
    conv_x = keras.layers.Activation('relu')(conv_x)
     
    print ('build conv_y')
    conv_y = keras.layers.Conv2D(n_feature_maps, 5, strides=1, padding='same')(conv_x)
    conv_y = keras.layers.BatchNormalization()(conv_y)
    conv_y = keras.layers.Activation('relu')(conv_y)
     
    print ('build conv_z')
    conv_z = keras.layers.Conv2D(n_feature_maps, (3, 1), padding='same')(conv_y)
    conv_z = keras.layers.BatchNormalization()(conv_z)
     
    is_expand_channels = not (input_shape[-1] == n_feature_maps)
    if is_expand_channels:
        shortcut_y = keras.layers.Conv2D(n_feature_maps, (1, 1),padding='same')(x)
        shortcut_y = keras.layers.BatchNormalization()(shortcut_y)
    else:
        shortcut_y = keras.layers.BatchNormalization()(x)
    print ('Merging skip connection')
    y = keras.layers.Add()([shortcut_y, conv_z])
    y = keras.layers.Activation('relu')(y)
     
    print ('build conv_x')
    x1 = y
    conv_x = keras.layers.Conv2D(n_feature_maps*2, 8, strides=1, padding='same')(x1)
    conv_x = keras.layers.BatchNormalization()(conv_x)
    conv_x = keras.layers.Activation('relu')(conv_x)
     
    print ('build conv_y')
    conv_y = keras.layers.Conv2D(n_feature_maps*2, 5, strides=1, padding='same')(conv_x)
    conv_y = keras.layers.BatchNormalization()(conv_y)
    conv_y = keras.layers.Activation('relu')(conv_y)
     
    print ('build conv_z')
    conv_z = keras.layers.Conv2D(n_feature_maps*2, (3, 1), padding='same')(conv_y)
    conv_z = keras.layers.BatchNormalization()(conv_z)
     
    is_expand_channels = not (input_shape[-1] == n_feature_maps*2)
    if is_expand_channels:
        shortcut_y = keras.layers.Conv2D(n_feature_maps*2, (1, 1),padding='same')(x1)
        shortcut_y = keras.layers.BatchNormalization()(shortcut_y)
    else:
        shortcut_y = keras.layers.BatchNormalization()(x1)
    print ('Merging skip connection')
    y = keras.layers.Add()([shortcut_y, conv_z])
    y = keras.layers.Activation('relu')(y)
     
    print ('build conv_x')
    x1 = y
    conv_x = keras.layers.Conv2D(n_feature_maps*2, 8, strides=1, padding='same')(x1)
    conv_x = keras.layers.BatchNormalization()(conv_x)
    conv_x = keras.layers.Activation('relu')(conv_x)
     
    print ('build conv_y')
    conv_y = keras.layers.Conv2D(n_feature_maps*2, 5, strides=1, padding='same')(conv_x)
    conv_y = keras.layers.BatchNormalization()(conv_y)
    conv_y = keras.layers.Activation('relu')(conv_y)
     
    print ('build conv_z')
    conv_z = keras.layers.Conv2D(n_feature_maps*2, (3, 1), padding='same')(conv_y)
    conv_z = keras.layers.BatchNormalization()(conv_z)

    is_expand_channels = not (input_shape[-1] == n_feature_maps*2)
    if is_expand_channels:
        shortcut_y = keras.layers.Conv2D(n_feature_maps*2, (1, 1),padding='same')(x1)
        shortcut_y = keras.layers.BatchNormalization()(shortcut_y)
    else:
        shortcut_y = keras.layers.BatchNormalization()(x1)
    print ('Merging skip connection')
    y = keras.layers.Add()([shortcut_y, conv_z])
    y = keras.layers.Activation('relu')(y)
     
    full = keras.layers.GlobalAveragePooling2D()(y)
    out = keras.layers.Dense(nb_classes, activation='softmax')(full)
    print ('        -- model was built.')
    return x, out

def readucr(filename):
    data = np.loadtxt(filename, delimiter = '\t')
    Y = data[:,0]
    X = data[:,1:]
    return X, Y
def divide_x_y_by_lenth(X_train,y_train,lenth):
    
    print('time series max_len_is {}'.format(X_train.shape[2]))
    print('time series len is {}'.format(lenth))
    X_train = np.transpose(X_train, (0, 2, 1))
    X_train=np.expand_dims(X_train, axis=2)
    x_tr=[]
    y_tr=[]
    for i in range(X_train.shape[0]):
        for j in range(int(X_train.shape[1]/lenth)):
            x_tr.append(X_train[i,j*lenth:(j+1)*lenth,:,:])
            y_tr.append(y_train[i])
    x_tr=np.array(x_tr)
    y_tr=np.array(y_tr)
    
    return x_tr, y_tr   
    


nb_epochs = 250
run_times=10

run_begin_index=0
method_name='RESNET_MTSC'


path = last_last_path + r"/dataset/MTSC/MTSC"
flist = os.listdir(path)
flist.sort(key=str.lower)
print(flist[run_begin_index:])


error_record=[]
loss_record=[]



if os.path.exists(last_last_path +r"/experiments_result/method_error_txt/{}.txt".format(method_name)):os.remove(last_last_path +r"/experiments_result/method_error_txt/{}.txt".format(method_name))

# for (num,each) in enumerate(flist[run_begin_index:run_begin_index+1]):
for (num,each) in enumerate(flist[run_begin_index:]):
    print('aaaaaaaaaaa')
    print('each')
    
  


    
    for i in range(run_times):

        print('xxx')
        
        fname = each

        
        
        X_train = np.load(last_last_path + r"/dataset/MTSC/MTSC"+"//" +fname+"//"+fname+"//"+ 'X_train.npy')
        y_train = np.load(last_last_path + r"/dataset/MTSC/MTSC"+"//" +fname+"//"+fname+ "//"+'y_train.npy')
        X_test  = np.load(last_last_path + r"/dataset/MTSC/MTSC"+"//" +fname+"//"+fname+"//"+'X_test.npy')
        y_test  = np.load(last_last_path + r"/dataset/MTSC/MTSC"+"//" +fname+"//"+fname+"//"+ 'y_test.npy')
        
        x_train,y_train=divide_x_y_by_lenth(X_train,y_train,X_train.shape[2])
        x_test,y_test=divide_x_y_by_lenth(X_test,y_test,X_train.shape[2])
        
        if np.any(y_test == 0):
            print('exist 0')
            
        else:
            y_train-=min(np.unique(y_test))

            y_test-=min(np.unique(y_test))
            # print(y_test)
        if  each==   'NetFlow':
            y_train[y_train==12]=1
            y_test[y_test==12]=1
        
        nb_classes = len(np.unique(y_test))
        batch_size = min(x_train.shape[0]//10, 16)
         
        # y_train = (y_train - y_train.min())/(y_train.max()-y_train.min())*(nb_classes-1)
        # y_test = (y_test - y_test.min())/(y_test.max()-y_test.min())*(nb_classes-1)
         
         
        Y_train = keras.utils.to_categorical(y_train, nb_classes)
        Y_test = keras.utils.to_categorical(y_test, nb_classes)
         
        # x_train_mean = x_train.mean()
        # x_train_std = x_train.std()
        # x_train = (x_train - x_train_mean)/(x_train_std)
          
        # x_test = (x_test - x_train_mean)/(x_train_std)
        # x_train = x_train.reshape(x_train.shape + (1,1,))
        # x_test = x_test.reshape(x_test.shape + (1,1,))
         
         
        x , y = build_resnet(x_train.shape[1:], 64, nb_classes)
        model = keras.models.Model(inputs=x, outputs=y)
        optimizer = keras.optimizers.Adam()
        model.compile(loss='categorical_crossentropy',
                      optimizer=optimizer,
                      metrics=['accuracy'])
          
        reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.5,
                          patience=50, min_lr=0.0001) 
        
        
        hist = model.fit(x_train, Y_train, batch_size=batch_size, epochs=nb_epochs,
                  verbose=1, validation_data=(x_test, Y_test), callbacks = [reduce_lr])
        #Print the testing results which has the lowest training loss.
        log = pd.DataFrame(hist.history)


        log = pd.DataFrame(hist.history)
        log.to_excel(last_last_path + r"/experiments_result/log/{}_dataset_{}_log{}_time{}.xlsx".format(method_name,str(flist.index(each)),i,datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
             
            
        print(log.loc[log['loss'].idxmin]['loss'], log.loc[log['loss'].idxmin]['val_acc'])
        error_record.append(1-log.loc[log['loss'].idxmin]['val_acc'])
        loss_record.append(log.loc[log['loss'].idxmin]['loss'])
        
        file = open(last_last_path + r"/experiments_result/method_error_txt/{}.txt".format(method_name), 'a')
        file.write( str(flist.index(each))+'error:'+'    '+str('%.5f'%(1-log.loc[log['loss'].idxmin]['val_acc']))+'     '+'loss:'+str('%.8f'%(log.loc[log['loss'].idxmin]['loss']))+'     ')
     
#        file.write( 'error:'+'   '+str('%.5f'%(1-log.loc[log['loss'].idxmin]['val_acc']))+'        '+'corresponding_min_loss:'+'   '+str('%.5f'%log.loc[log['loss'].idxmin]['loss']) +'        '+str(flist.index(each))+'        ' +each +'/n')
#        file.write( 'error:'+'   '+str('%.5f'%(1-log.loc[log['loss'].idxmin]['val_acc']))+'        '+'corresponding_min_loss:'+'   '+str('%.5f'%log.loc[log['loss'].idxmin]['loss']) +'        '+str(flist.index(each))+'        ' +each +'/n')
    
        file.close()

        print('!!!!!!!!!!!!!!!!  {} {} {}::runtime:{}____min_error:{}'.format(method_name,num,each,i,'%.5f'%min(error_record)))
        
        if 1-log.loc[log['loss'].idxmin]['val_acc']==0:
            break

    file = open(last_last_path + r"/experiments_result/method_error_txt/{}.txt".format(method_name), 'a')
    file.write('min_error:'+'     '+ str('%.5f'%(min(error_record)))+'     '+'     '+str(flist.index(each))+'        ' +each +'\n')
    file.close()
    error_record=[]
    loss_record=[]

    
    
    
############## Get CAM ################
# import matplotlib.pyplot as plt
# # from matplotlib.backends.backend_pdf import PdfPages

# get_last_conv = keras.backend.function([model.layers[0].input, keras.backend.learning_phase()], [model.layers[-3].output])
# last_conv = get_last_conv([x_test[:100], 1])[0]

# get_softmax = keras.backend.function([model.layers[0].input, keras.backend.learning_phase()], [model.layers[-1].output])
# softmax = get_softmax(([x_test[:100], 1]))[0]
# softmax_weight = model.get_weights()[-2]
# CAM = np.dot(last_conv, softmax_weight)


# # pp = PdfPages('CAM.pdf')
# for k in range(20):
#     CAM = (CAM - CAM.min(axis=1, keepdims=True)) / (CAM.max(axis=1, keepdims=True) - CAM.min(axis=1, keepdims=True))
#     c = np.exp(CAM) / np.sum(np.exp(CAM), axis=1, keepdims=True)
#     plt.figure(figsize=(13, 7));
#     plt.plot(x_test[k].squeeze());
#     plt.scatter(np.arange(len(x_test[k])), x_test[k].squeeze(), cmap='hot_r', c=c[k, :, :, int(y_test[k])].squeeze(), s=100);
#     plt.title(
#         'True label:' + str(y_test[k]) + '   likelihood of label ' + str(y_test[k]) + ': ' + str(softmax[k][int(y_test[k])]))
#     plt.colorbar();
# #     pp.savefig()
# #
# # pp.close()