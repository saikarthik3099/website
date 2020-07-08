import sys, os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import numpy as np
import re, os, random
import random
random.seed(102)

max_samples = 1000000000000
dwidth, ddepth = 13, 480
aupath = '/work/ssd/projects/word_level/words_48_384_gray_npz/'

'''from keras.layers import Input, Dense, Conv2D, MaxPooling2D, MaxPooling1D, UpSampling2D, Dropout, Reshape, Permute, Concatenate, Activation
from keras.layers import LSTM, TimeDistributed, CuDNNLSTM, Flatten, Conv1D, Lambda, concatenate, BatchNormalization, Bidirectional
from keras.models import Model, load_model
from keras.preprocessing import image
from keras.layers.advanced_activations import LeakyReLU, PReLU, ReLU
from keras.utils import multi_gpu_model as MGM
#import tensorflow as tf
from keras import backend as K
from batchGen import DataGenerator
from keras.applications import inception_v3
#from utils import layer_utils
from keras.optimizers import Adadelta, Adam, RMSprop
from keras.callbacks import ModelCheckpoint
from keras.utils import plot_model'''





from tensorflow.keras.layers import Input, Dense, Conv2D,MaxPooling1D, MaxPooling2D, UpSampling2D, Dropout, Reshape, Permute, Concatenate, Activation
from tensorflow.keras.layers import LSTM, TimeDistributed, Flatten, Conv1D, Lambda, concatenate, BatchNormalization, Bidirectional
from tensorflow.keras import Model
from tensorflow.keras.preprocessing import image
#from tensorflow.keras.layers.advanced_activations import LeakyReLU, PReLU, ReLU
from tensorflow.keras.utils import multi_gpu_model as MGM
#import tensorflow as tf
from tensorflow.keras import backend as K
from batchGen import DataGenerator
from tensorflow.keras.applications import inception_v3
#from utils import layer_utils
from tensorflow.keras.optimizers import Adadelta, Adam, RMSprop
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import plot_model
from tensorflow.python.keras.utils.data_utils import Sequence





random.seed(101)

batch_size=32
train_in_file_path = "/work/sentence_type_classification/speech_classification/train_dataset/"
val_in_file_path = "/work/sentence_type_classification/speech_classification/validation_dataset/"

train_generator = DataGenerator(train_in_file_path, batch_size=batch_size, dwidth=dwidth, ddepth=ddepth, other_class_cnt=125000)
val_generator = DataGenerator(val_in_file_path, batch_size=batch_size, dwidth=dwidth, ddepth=ddepth, other_class_cnt=112500)

print("creating Model")
print("---------------")
input_mfcc = Input(shape=(ddepth, dwidth))
### Model2
'''
x = Reshape( (480, 13, 1) )(input_mfcc)
x = Conv2D(13, (3,3), strides=1, padding='same', activation='relu')(x)
x = Conv2D(13, (3,3), strides=1, padding='same', activation='relu')(x)
x = Conv2D(13, (3,3), strides=1, padding='same', activation='relu')(x)
x = MaxPooling2D(pool_size=(3,3))(x)
x = Conv2D(26, (3,3), strides=1, padding='same', activation='relu')(x)
x = Conv2D(26, (3,3), strides=1, padding='same', activation='relu')(x)
x = Conv2D(26, (3,3), strides=1, padding='same', activation='relu')(x)
x = MaxPooling2D(pool_size=(2,2))(x)
x = Conv2D(52, (3,3), strides=1, padding='same', activation='relu')(x)
x = Conv2D(52, (3,3), strides=1, padding='same', activation='relu')(x)
x = Conv2D(52, (3,3), strides=1, padding='same', activation='relu')(x)
x = MaxPooling2D(pool_size=(2,2))(x)
x = Reshape( (40,52) )(x)
x = Conv1D(104, 3, strides=1, padding='same', activation='relu')(x)
x = Conv1D(104, 3, strides=1, padding='same', activation='relu')(x)
x = Conv1D(104, 3, strides=1, padding='same', activation='relu')(x)
x = MaxPooling1D(pool_size=(2,))(x)
x = Dropout(0.1)(x)
x = Conv1D(300, 3, strides=1, padding='same', activation='relu')(x)
x = Conv1D(300, 3, strides=1, padding='same', activation='relu')(x)
x = Conv1D(300, 3, strides=1, padding='same', activation='relu')(x)
x = MaxPooling1D(pool_size=(2,))(x)
x = Flatten()(x)
x = Dropout(0.1)(x)

x = Dense(2048, activation='relu', name='dense_1')(x)
x = Dropout(0.1)(x)
x = Dense(1024, activation='relu', name='dense_2')(x)
x = Dropout(0.2)(x)
'''

###Model1
x = Reshape( (480, 13, 1) )(input_mfcc)
x = Conv2D(26, (5,5), strides=3, padding='same', activation='relu')(x)
x = Conv2D(52, (3,3), strides=2, padding='same', activation='relu')(x)
x = Conv2D(52, (3,3), strides=1, padding='same', activation='relu')(x)
x = MaxPooling2D(pool_size=(2,3))(x)
x = Reshape( (40,52) )(x)
x = Conv1D(104, 5, strides=2, padding='same', activation='relu')(x)
x = Conv1D(300, 3, strides=1, padding='same', activation='relu')(x)
x = Conv1D(300, 3, strides=1, padding='same', activation='relu')(x)
x = MaxPooling1D(pool_size=(2,))(x)
x = Flatten()(x)

#x = Dropout(0.1)(x)

x = Dense(2048, activation='relu', name='dense_1')(x)
#x = Dropout(0.1)(x)
x = Dense(1024, activation='relu', name='dense_2')(x)
#x = Dropout(0.2)(x)


x = Dense(3, activation='softmax', name='output')(x)
output = x

classifier_model = Model(input_mfcc, output)

classifier_model.summary()
plot_model(classifier_model, to_file='speech_classifier_rnn_only.png', show_shapes=True)

print("Compiling Model")
print("---------------")
classifier_model.compile(optimizer='adadelta', loss="categorical_crossentropy", metrics=['accuracy'])

print("Training Model")
print("--------------")
for i in range(1, 10):
    print('Iteration', str(i))
    classifier_model.fit_generator(train_generator, validation_data=val_generator, epochs=1, 
        use_multiprocessing=True, workers=28, max_queue_size=100, shuffle=True, verbose=1)
    #classifier_model.save('models/speech_classification_'+str(i)+'.hf5')



