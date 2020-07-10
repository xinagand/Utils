import numpy as np
from tqdm import tqdm
import os, sys
from PIL import Image
from matplotlib import pyplot as plt

def main():
    print('util file')
    data_path = './data/'
    # rename_all(data_path)


def rename_all(path):
    images = [img for img in os.listdir(path) if img.endswith(".jpg")]  # read images inside folders
    images = sorted(images, key=lambda x: float(x.split("_")[2].split(".jpg")[0]))  # TODO: define sorting rule here

    for image in tqdm(images):  # assume filename is xxx_yyy_0321.jpg
        name = image.split('_')
        temp_name = name[2].split('.jpg')
        name[2] = str(int(temp_name[0])) + '.jpg'  # change 0001 -> 1
        new_name = "_".join(name)
        os.rename(os.path.join(path, image), os.path.join(path, new_name))


def read_npy(file_path):
    # file_path = '05_0021.npy'  # example
    data = np.load(file_path)
    print(data)

# resize the all images inside folders into (size,size) pixel
# Crop with ratio if needed
# careful! this function changes the original file!
def resize_save(path, size, ratio):
    folders = os.listdir(path)  # what's in that location
    for filename in tqdm(folders): # for all files in the path
        ori = Image.open(path + filename)  # read one file
        if ratio:  # crop if needed
            ori = center_crop(ori, ratio[0], ratio[1])
        rsz = ori.resize((size, size))  # resize
        rsz.save(path + filename)  # save


def center_crop(img, w_ratio, h_ratio):
    width = img.size[0]
    height = img.size[1]

    new_width = width*(1/w_ratio)
    new_height = height*(1/h_ratio)

    left = int(np.ceil((width - new_width) / 2))
    right = width - int(np.floor((width - new_width) / 2))

    top = int(np.ceil((height - new_height) / 2))
    bottom = height - int(np.floor((height - new_height) / 2))

    crop_rectangle = (left, top, right, bottom)
    cropped_img = img.crop(crop_rectangle)

    return cropped_img


if __name__ == '__main__':
    main()