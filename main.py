# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 08:36:06 2017

@author: bipin
"""

#importing Keras, Library for deep learning 
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.preprocessing.image import  img_to_array
from keras import backend as K
# Fix for Issue - #3 https://github.com/shreyans29/thesemicolon/issues/3
K.set_image_dim_ordering('th')

import numpy as np

# Image manipulations and arranging data
import os
from PIL import Image
import theano

theano.config.optimizer="None"
#Sklearn to modify the data

from sklearn.cross_validation import train_test_split
os.chdir("F:/aiprojects/data/plr");

# input image dimensions
m,n = 50,50

path1="test";
path2="train";

classes=os.listdir(path2)
print(classes)
x=[]
y=[]
for fol in classes: #fol for folder
    print (fol)
    imgfiles=os.listdir(path2+'/'+fol);
    for img in imgfiles:
        if (img != "Thumbs.db"):
            im=Image.open(path2+'/'+fol+'/'+img);
            im=im.convert(mode='RGB')
            imrs=im.resize((m,n))
            imrs=img_to_array(imrs)/255;
            imrs=imrs.transpose(2,0,1);
            imrs=imrs.reshape(3,m,n);
            x.append(imrs)
            y.append(fol)
        
x=np.array(x);
y=np.array(y);

batch_size=32
nb_classes=len(classes)
nb_epoch=20
nb_filters=32
nb_pool=2
nb_conv=3

x_train, x_test, y_train, y_test= train_test_split(x,y,test_size=0.2,random_state=4)

uniques, id_train=np.unique(y_train,return_inverse=True)
Y_train=np_utils.to_categorical(id_train,nb_classes)
uniques, id_test=np.unique(y_test,return_inverse=True)
Y_test=np_utils.to_categorical(id_test,nb_classes)

model= Sequential()
model.add(Convolution2D(nb_filters,nb_conv,nb_conv,border_mode='same',input_shape=x_train.shape[1:]))
model.add(Activation('relu'));
model.add(Convolution2D(nb_filters,nb_conv,nb_conv));
model.add(Activation('relu'));
model.add(MaxPooling2D(pool_size=(nb_pool,nb_pool)));
model.add(Dropout(0.5));
model.add(Flatten());
model.add(Dense(128));
model.add(Dropout(0.5));
model.add(Dense(nb_classes));
model.add(Activation('softmax'));
model.compile(loss='categorical_crossentropy',optimizer='adadelta',metrics=['accuracy'])

nb_epochs=10;
batch_size=36;
model.fit(x_train,Y_train,batch_size=batch_size,epochs=nb_epochs,verbose=1,validation_data=(x_test, Y_test))


files=os.listdir(path1);
img=files[0] 
im = Image.open(path1 + '/' + img);
imrs = im.resize((m,n))
imrs=img_to_array(imrs)/255;
imrs=imrs.transpose(2,0,1);
imrs=imrs.reshape(3,m,n);

x=[]
x.append(imrs)
x=np.array(x);
predictions = model.predict(x)
print (predictions)


#errors
#thumbs.db >>> https://www.sitepoint.com/switch-off-thumbs-db-in-windows/