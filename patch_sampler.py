import os
import cv2

def main():
    images_source_folder = './data/trainset/'  # image source
    images = [img for img in os.listdir(images_source_folder) if img.endswith(".jpg")]
    frame = cv2.imread(images_source_folder + images[0])

    width, height, layers = frame.shape 
    print("H:{0}, W:{1}, C:{2}".format(height, width, layers))

    images = sorted(images, key=lambda x: float(x.split("_")[2].split(".jpg")[0]))  # 순서대로




if __name__=="__main__":
    print('main')
    main()


