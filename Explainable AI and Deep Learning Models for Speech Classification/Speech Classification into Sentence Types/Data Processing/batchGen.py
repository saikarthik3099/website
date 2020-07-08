import os,re
import numpy as np
from tensorflow.keras import utils as kutils
from tensorflow.keras.preprocessing.image import array_to_img, img_to_array, load_img
from time import time

class DataGenerator(kutils.Sequence):
    'Generates data for Keras'
    def __init__(self, in_file_path, batch_size=32, dwidth=13, ddepth=500, shuffle=True, other_class_cnt=25000):
        'Initialization initialize all files'
        self.dwidth = dwidth
        self.ddepth = ddepth
        self.batch_size = batch_size
        self.in_file_path = in_file_path
        self.in_file_names = []
        self.output_arr = {}
        self.shuffle = shuffle
        self.other_class_cnt = other_class_cnt

        self.list_inp_files_and_output()
        self.suffle_data()
    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.in_file_names) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        file_IDs_temp = [self.in_file_names[k] for k in indexes]

        # Generate data
        X, Y = self.__data_generation(file_IDs_temp)
        return X, Y

    def list_inp_files_and_output(self):
        inpfiles = [f for f in os.listdir(self.in_file_path)]
        #inpfiles = os.listdir(input_dirn)
        #print(inpfiles) 

        cnt_oth = 0
        for fl in inpfiles:
            if re.match(r'(?i)^.+_question.npz$', fl):
                self.in_file_names.append(fl)
                self.output_arr[fl] = [1, 0, 0]
            elif re.match(r'(?i)^.+_exclamation.npz$', fl):
                self.in_file_names.append(fl)
                self.output_arr[fl] = [0, 1, 0]
            elif re.match(r'(?i)^.+_other.npz$', fl):
                if cnt_oth > self.other_class_cnt: continue
                self.in_file_names.append(fl)
                self.output_arr[fl] = [0, 0, 1]
                cnt_oth+=1

    def suffle_data(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.in_file_names))

        if self.shuffle == True:
            np.random.shuffle(self.indexes)


    def __data_generation(self, file_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, ddepth, dwidth)
        # Initialization
        X = np.empty((self.batch_size, self.ddepth, self.dwidth))
        Y = np.empty((self.batch_size,3))
        # Generate data
        for i, ID in enumerate(file_IDs_temp):
            # Store input sample
            audata = np.load(self.in_file_path+ID)['arr_0']
            # check the size of audata and truncate it to ddepth
            audepth = audata.shape[0]
            if audepth < self.ddepth:
                tmp = np.zeros( (self.ddepth, self.dwidth) )
                tmp[:audepth, :self.dwidth] = audata
            else:
                tmp = audata[:self.ddepth]
            X[i,] = tmp
            # Store output sample
            Y[i,] = self.output_arr[ID]

        #print(i, 'read', ID, X.shape, Y.shape)
        return X, Y


