import os,glob,sys
import subprocess
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.editor as mp

movie_no = 0
movie_set_folder = ''

def cut_movie(line,count,movie_path,sub):
    duration = line
    arr = duration.split('-->')
    start_arr = arr[0].split(':')
    end_arr = arr[1].split(':')
    start_sec_arr = start_arr[2].split(',')
    end_sec_arr = end_arr[2].split(',')

    start_time = (int(start_arr[0])*3600) + (int(start_arr[1])*60) + (int(start_sec_arr[0])) + (0.001*int(start_sec_arr[1][0:3]))
    end_time = (int(end_arr[0])*3600) + (int(end_arr[1])*60) + (int(end_sec_arr[0])) + (0.001*int(end_sec_arr[1][0:3]))

    with VideoFileClip(movie_path) as video:
        new = video.subclip(start_time,end_time)

        if ('?' in sub):
            #writing splitted subclip
            new.write_videofile("C:/Users/Eshwar7799/Desktop/video_datasets/question/" + movie_set_folder + "_" + "movie"+ str(movie_no) + "_vid" + str(count) + ".mp4")
            #Resizing original subclip and replacing original one
            '''clip = mp.VideoFileClip("/work/video_datasets/question/" + movie_set_folder + "_" + "movie"+ str(movie_no) + "_vid" + str(count) + ".mp4")
            clip_resized = clip.resize("/work/video_datasets/question/" + movie_set_folder + "_" + "movie"+ str(movie_no) + "_vid" + str(count) + ".mp4")
            clip_resized.write_videofile("/work/video_datasets/question/" + movie_set_folder + "_" + "movie"+ str(movie_no) + "_vid" + str(count) + ".mp4")'''
            #Extracting audioo and writing a mp3 file in compressed version
            input_path = "C:/Users/Eshwar7799/Desktop/video_datasets/question/" + movie_set_folder + "_" +"movie"+str(movie_no)+"_vid"+ str(count) + ".mp4"
            output_path = "C:/Users/Eshwar7799/Desktop/video_datasets/question/" + movie_set_folder + "_"  + "movie" + str(movie_no) + "_aud" + str(count) + ".mp3"
            command = "ffmpeg -i " + input_path + " -b:a 16000 -vn " + output_path
            subprocess.call(command,shell=True)
        elif ('!' in sub):
            new.write_videofile("C:/Users/Eshwar7799/Desktop/video_datasets/exclamation/" + movie_set_folder + "_" + "movie"+ str(movie_no) + "_vid" + str(count) + ".mp4")
            '''clip = mp.VideoFileClip("/work/video_datasets/exclamation/" + movie_set_folder + "_" + "movie"+ str(movie_no) + "_vid" + str(count) + ".mp4")
            clip_resized = clip.resize(height=360)
            clip_resized.write_videofile("/work/video_datasets/exclamation/" + movie_set_folder + "_" + "movie"+ str(movie_no) + "_vid" + str(count) + ".mp4")'''
            input_path = "C:/Users/Eshwar7799/Desktop/video_datasets/exclamation/" + movie_set_folder + "_"  + "movie" + str(movie_no)+"_vid"+ str(count) + ".mp4"
            output_path = "C:/Users/Eshwar7799/Desktop/video_datasets/exclamation/" + movie_set_folder + "_" + "movie" + str(movie_no) + "_aud" + str(count) + ".mp3"
            command = "ffmpeg -i " + input_path + " -b:a 16000 -vn " + output_path
            subprocess.call(command,shell=True)
        else:
            new.write_videofile("C:/Users/Eshwar7799/Desktop/video_datasets/other/" + movie_set_folder + "_" + "movie"+ str(movie_no) + "_vid" + str(count) + ".mp4")
            '''clip = mp.VideoFileClip("/work/video_datasets/other/" + movie_set_folder + "_" + "movie"+ str(movie_no) + "_vid" + str(count) + ".mp4")
            clip_resized = clip.resize(height=360)
            clip_resized.write_videofile("/work/video_datasets/other/" + movie_set_folder + "_" + "movie"+ str(movie_no) + "_vid" + str(count) + ".mp4")'''
            input_path = "C:/Users/Eshwar7799/Desktop/video_datasets/other/" + movie_set_folder + "_" +"movie"+str(movie_no)+"_vid"+ str(count) + ".mp4"
            output_path = "C:/Users/Eshwar7799/Desktop/video_datasets/other/" + movie_set_folder + "_" + "movie" + str(movie_no) + "_aud" + str(count) + ".mp3"
            command = "ffmpeg -i " + input_path +" -b:a 16000 -vn " + output_path
            subprocess.call(command,shell=True)

def split_movie(movie_file_path,srt_file_path):
    count = 0
    with open(srt_file_path) as f:
        print("NOW"+srt_file_path)
        line = f.readline()
        while(line):
            if '-->' in line:
                duration_line = line
                sub = ''
                line = f.readline()
                line = line.strip()

                while(line!=""):
                    sub += line
                    line = f.readline()
                    line = line.strip()
                if ('?' in sub):
                    txt_file = open("C:/Users/Eshwar7799/Desktop/video_datasets/question/"+ movie_set_folder + "_"+"movie"+str(movie_no)+"_sub"+str(count)+".txt","w")
                elif ('!' in sub):
                    txt_file = open("C:/Users/Eshwar7799/Desktop/video_datasets/exclamation/"+ movie_set_folder + "_" +"movie"+str(movie_no)+"_sub"+str(count)+".txt","w")
                else :
                    txt_file = open("C:/Users/Eshwar7799/Desktop/video_datasets/other/"+ movie_set_folder + "_" +"movie"+str(movie_no)+"_sub"+str(count)+".txt","w")
                txt_file.write(sub)
                cut_movie(duration_line,count,movie_file_path,sub)
                count += 1
            line = f.readline()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage : python3 split.py /movie_folder/")
        sys.exit(1)
    #getting main directory
    movie_dir = sys.argv[1]
    #store the movie set folder name to add it to the name of mp4,mp3,text files in classification problems
    split_arr = movie_dir.split('/')
    movie_set_folder = split_arr[len(split_arr)-2]
    print("HEY " + movie_set_folder)
    movies_list = os.listdir(movie_dir)
    print(movies_list)
    index = 1
    for dirs in movies_list:
        print("haha")
        print(movie_dir+"/"+dirs)
        if os.path.isdir(movie_dir+"/"+dirs):
            print("kakak")
            print(index,"--------------------")
            os.chdir(movie_dir+"/"+dirs)
            for name in os.listdir("."):
                if name.endswith(".mp4"):
                    movie_file_path = os.path.abspath(name)
                    print(name)
                    print(movie_file_path)
            for srts in os.listdir("."):
                
                if srts.endswith(".srt"):
                    print(srts)
                    srt_file_path = os.path.abspath(srts)
                    print(srt_file_path)
                    
            '''for file in movie_dir+"/"+dirs:   #(glob.glob("*.mp4") or glob.glob("*.mkv") or glob.glob("*.avi")):
                movie_file_path = os.path.abspath(file)
                print(movie_file_path)
            for file in glob.glob("*.srt"):

                srt_file_path = os.path.abspath(file)
                print("haha")'''
            index += 1
            movie_no += 1
            split_movie(movie_file_path,srt_file_path)
			    #print("gafcjab")
				#print(srt_file_path)
		