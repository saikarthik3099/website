from pydub import AudioSegment
import librosa
import os,glob,sys
from multiprocessing import Pool

cnt=0
def dump_file(file):
    sys.stdout.write('.')
    sys.stdout.flush()
    dest_path = os.path.abspath(file)
    dest_path = dest_path.replace(".mp3",".wav")
    y,s = librosa.load(os.path.abspath(file),sr=16000)
    librosa.output.write_wav(dest_path,y,s)

index = 0
pool_args = []
os.chdir("/work/video_datasets/other/")
for file in glob.glob("*.mp3"):
    index += 1
    #sound = AudioSegment.from_mp3(file)
    #sound.export(dest_path,format="wav",bitrate='16k')
    pool_args.append( (file,) )

pool = Pool(28)
pool.starmap(dump_file, pool_args)
pool.close()
pool.join()

