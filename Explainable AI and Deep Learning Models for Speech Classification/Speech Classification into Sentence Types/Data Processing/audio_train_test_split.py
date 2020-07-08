

import random
import os,re
from shutil import copy


datasets = [('/work/video_datasets/question/','_question'),('/work/video_datasets/exclamation/','_exclamation'),('/work/video_datasets/other/','_other')]

#dump_path = 'batch1/'
#test_path = 'demo/'
val_dest = '/work/sentence_type_classification/speech_classification/audio_validation_dataset/'
train_dest = '/work/sentence_type_classification/speech_classification/audio_train_dataset/'
for (dataset,tt) in datasets:
    all_filenames = [f for f in os.listdir(dataset) if re.match(r'^.+.wav', f)]
    cnt = 0
    for file_name in all_filenames:
        cnt += 1
        dest_file_path = file_name
        dest_file_path = dest_file_path.replace(".wav",tt+".wav")
        if cnt%10==0 :
            copy(dataset + file_name,val_dest + dest_file_path)
        else :
            copy(dataset + file_name,train_dest + dest_file_path)


