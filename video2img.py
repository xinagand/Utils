from openpyxl import load_workbook
import os
import ffmpeg
from moviepy.editor import *
import sys
from tqdm import tqdm

path_dir = sys.argv[1]
video_dir = sys.argv[2]
folders = os.listdir((video_dir))

count=0
filenum = 0
for filename in tqdm(folders, desc='All Files'):
    my_clip = VideoFileClip(video_dir+filename)
    duration = int(my_clip.duration)
    filenum+=1
    for i in tqdm(range(0, duration), desc='Video %d %s'%(filenum, filename)):
        if i in range(30600,34200):
            my_clip.save_frame(path_dir+str(count)+".jpg", i) # normal은 너무 많아서 1초에 한장만
            count+=1
        elif i in range(63000,66600):
            my_clip.save_frame(path_dir + str(count) + ".jpg", i)  # normal은 너무 많아서 1초에 한장만
            count += 1
        else:
            pass

# # Abnormal Extraction part
# # data_only=Ture로 해줘야 수식이 아닌 값으로 받아온다.
# print("Video2img done!")
# label = load_workbook("TrainTestAbnormalLabel_0323.xlsx", data_only=True)
# # 시트 이름으로 불러오기
# load_label = label['Sheet1']
#
# labels =[]
# for i in load_label.rows:
#     TF = i[2].value
#     labels.append(TF)
#
# for i,dead in enumerate(labels):
#     if dead==False:
#         name = path_dir + str(i+1)+".jpg"
#         os.remove(name)


