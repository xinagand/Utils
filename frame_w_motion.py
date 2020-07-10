import glob

import os, gc, random, shutil
import os.path
import numpy as np
import cv2
from tqdm import tqdm

path_out = '/home/zaigham/Downloads/out'

def main():
    images_source_folder = './data/good/'

    patch_size = 135
    sliding_step = 75
    threshold_percentage_of_motion_in_patch = 10

    images = [img for img in os.listdir(images_source_folder) if img.endswith(".jpg")]
    frame = cv2.imread(images_source_folder + images[0])
    width, height, layers = frame.shape
    print("H:{0}, W:{1}, C:{2}".format(height, width, layers))

    images = sorted(images, key=lambda x: float(x.split("_")[2].split(".jpg")[0]))  # 순서대로

    # binay_mask = cv2.imread('binary_mask2.jpg')
    # Clean up tmp folder
    files = glob.glob('./out/patch_w_motion/*')
    for f in files:
        os.remove(f)
    files = glob.glob('./out/patch_wo_motion/*')
    for f in files:
        os.remove(f)
    for i, img in enumerate(images):
        print("Running... [{0}/{1}]".format(i,len(images)))
        files = glob.glob('./out/frame_motion/*')
        for f in files:
            os.remove(f)
        files = glob.glob('./out/frame_patch/*')
        for f in files:
            os.remove(f)
        files = glob.glob('./out/motion_patch/*')
        for f in files:
            os.remove(f)

        tmp_img = cv2.imread(os.path.join(images_source_folder, img))
        tmp_frame_slices, _ = get_image_patches_individual_processing(tmp_img, width, height,
                                                                                       destination_dir = path_out + '/frame_patch/',
                                                                                       img_name=img,
                                                                                       nd_patch_size=[
                                                                                           patch_size,
                                                                                           patch_size],
                                                                                       nd_stride=[
                                                                                           sliding_step,
                                                                                           sliding_step])

        name = img.split('_')
        temp_name = name[2].split('.jpg')
        if i == 0:  # Next frame as neighbor
            name[2] = str(int(temp_name[0]) + 1) + '.jpg'
        else:  # Prev frame as neighbor
            name[2] = str(int(temp_name[0]) - 1) + '.jpg'
        neighbor_image_name = "_".join(name)
        if os.path.isfile(os.path.join(images_source_folder, neighbor_image_name)):
            neighbor_img = cv2.imread(os.path.join(images_source_folder, neighbor_image_name))
        else:  # Scene not connected. just skip this frame
            neighbor_img = tmp_img

        motion_map = cv2.absdiff(neighbor_img, tmp_img)
        # cv2.imshow('show', motion_map)
        # cv2.waitKey()
        motion_map[motion_map <= 50] = 0
        motion_map[motion_map > 50] = 255
        # motion_map = motion_map * binay_mask  # Delete less interesting point
        cv2.imwrite(path_out + '/frame_motion/' + img, motion_map)

        total_motion_pixels_in_motion_frame = np.count_nonzero(motion_map > 0)
        # motion_map = cv2.cvtColor(motion_map, cv2.COLOR_GRAY2BGR)
        tmp_motion_slices, _ = get_image_patches_individual_processing(motion_map, width, height,
                                                                                       destination_dir=path_out + '/motion_patch/',
                                                                                       img_name=img,
                                                                                       nd_patch_size=[
                                                                                           patch_size,
                                                                                           patch_size],
                                                                                       nd_stride=[
                                                                                           sliding_step,
                                                                                           sliding_step])

        for i, j in enumerate((range(tmp_frame_slices.shape[0]))):
            total_motion_pixels_in_patch = np.count_nonzero(tmp_motion_slices[i, :, :, :] > 0)  # Motion in Frame?

            if total_motion_pixels_in_motion_frame == 0:  # No Motion in Frame
                if random.random() < 0.05:
                    cv2.imwrite(path_out + '/patch_wo_motion/' + img + '_{0}.jpg'.format(i), tmp_frame_slices[i, :, :, :])
            else:
                if total_motion_pixels_in_patch * 100 / total_motion_pixels_in_motion_frame > threshold_percentage_of_motion_in_patch:
                    cv2.imwrite(path_out + '/patch_w_motion/' + img + '_{0}.jpg'.format(i), tmp_frame_slices[i, :, :, :])
                else:
                    if random.random() < 0.05:
                        cv2.imwrite(path_out + '/patch_wo_motion/' + img + '_{0}.jpg'.format(i), tmp_frame_slices[i, :, :, :])

        del tmp_frame_slices, _, tmp_motion_slices, total_motion_pixels_in_motion_frame, motion_map, neighbor_img, neighbor_image_name, name
        gc.collect()


def get_image_patches_individual_processing(image_src, width, height, destination_dir, img_name, nd_patch_size, nd_stride):
    #This function processes each frame separately. Which means there will be no global counter for patch numbers.

    lst_patches = []
    lst_locations = []

    n_stride_h = nd_stride[0]
    n_stride_w = nd_stride[1]

    # for i in range(0,n_frame_h,n_stride_h):
    # np.array(lst_patches[10])[0,:,:]
    flag_permission_h = True
    i = 0
    patch_number = 0

    while i < height and flag_permission_h:
        flag_permission_w = True
        start_h = i
        end_h = i + nd_patch_size[0]
        if end_h > height:  # Clip in the end
            end_h = height
            start_h = height - nd_patch_size[0]
        # for j in range(0,n_frame_w,n_stride_w):
        j = 0
        while j < width and flag_permission_w:
            start_w = j
            end_w = j + nd_patch_size[1]
            if end_w > width:
                end_w = width
                start_w = width - nd_patch_size[1]

            tmp_slices = np.array(image_src[start_w:end_w, start_h:end_h, :])  # this is the image i can save to a target folder as one patch

            #TODO: READ FROM HERE
            patch_name_and_path = os.path.join(destination_dir, img_name + '_patch_'+str(patch_number)+'.jpg')
            cv2.imwrite(patch_name_and_path, tmp_slices)
            patch_number +=1
            lst_patches.append(tmp_slices)
            lst_locations.append([start_h, start_w])

            j += n_stride_w
            if j > width:
                flag_permission_w = False
                j = width - nd_patch_size[1]

        i += n_stride_h
        if i > height:
            flag_permission_h = False
            i = width - nd_patch_size[0]

    return np.array(lst_patches), lst_locations

if __name__=="__main__":
    print('main')
    main()








