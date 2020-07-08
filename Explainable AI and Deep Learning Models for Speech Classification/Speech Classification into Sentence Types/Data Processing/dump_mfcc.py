from python_speech_features import mfcc
import matplotlib.pyplot as plt
import librosa
import numpy as np
import sys,os,glob
from multiprocessing import Pool

#mfcc_feat = np.empty(shape=[10000,189,13])
pool_args = []

def make_npz(mp3_dir):
    index = 1
    os.chdir(mp3_dir)
    for file in glob.glob("*.wav"):
        pool_args.append( (file,) )
    pool = Pool(28)
    pool.starmap(make_npz_act, pool_args)
    pool.close()
    pool.join()


def make_npz_act(file_path):
    sys.stdout.write('.')
    sys.stdout.flush()

    mp3_path = os.path.abspath(file_path)
    npz_path = mp3_path.replace(".wav",".npz")
    npz_path = npz_path.replace("/question/","/question_npz/")
    (sig,rate) = librosa.load(file_path,sr=16000)
    mfcc_feat = mfcc(sig,rate)

    #print(index)
    #dindex += 1
    #print(npz_path)
    #print(mfcc_feat)
    np.savez_compressed(npz_path,mfcc_feat)

'''

pool = Pool(28)
pool.starmap(make_npz_act, pool_args)
pool.close()
pool.join()
'''

if __name__ == '__main__':
    if(len(sys.argv)) < 2:
        print("usage : python savanth_trial.py mp3_folder_path")
        sys.exit(1)

    mp3_dir = sys.argv[1]
    make_npz(mp3_dir)

