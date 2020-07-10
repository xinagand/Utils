import cv2
import os
from tqdm import tqdm
# from PIL import Image

image_folder = './data/'
video_path = ''
video_name = 'Pohang_191113'

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(image_folder + images[0])
height, width, layers = frame.shape

images = sorted(images, key=lambda x: float(x.split("_")[2].split(".jpg")[0]))  # 순서대로
# print(images)



video = cv2.VideoWriter(video_path+video_name+'.avi', cv2.VideoWriter_fourcc(*'DIVX'), 60, (width, height))
for image in tqdm(images):
    # print(image)
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()