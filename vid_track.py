
from moviepy.editor import *
import os
from PIL import Image, ImageDraw
from PIL import ImageFont
from shapely.geometry import Polygon

def calculate_iou(box_1, box_2):
    poly_1 = Polygon(box_1)
    poly_2 = Polygon(box_2)
    iou = poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
    return iou

def Crop_save(target, target_bb, detection):
    im = Image.open(target)
    crop_im = im.crop(target_bb)
    count = 1
    if idx != 0:
        if detection[idx-1][0] == detection[idx][0]:
            count = 2
    crop_im.save("Crop/{0}_{1}.jpg".format(detection[idx][0], count))

def get_bb(detection):
    # draw bounding box
    target_bb = [detection[idx][2], detection[idx][3], detection[idx][2] + detection[idx][4],
                 detection[idx][3] + detection[idx][5]]

    # draw oversize box
    center_x = (detection[idx][2] * 2 + detection[idx][4]) / 2
    center_y = (detection[idx][3] * 2 + detection[idx][5]) / 2
    stride_x = detection[idx][4]
    stride_y = detection[idx][5]

    target_bb = [center_x - stride_x * 1.25, center_y - stride_y * 0.75, center_x + stride_x * 1.25,
                 center_y + stride_y * 0.75]
    if target_bb[0] < 0:
        target_bb[0] = 0
    if target_bb[1] < 0:
        target_bb[1] = 0
    if target_bb[2] > 1280:
        target_bb[2] = 1280
    if target_bb[3] > 720:
        target_bb[3] = 720

    # refine location of BB
    target_bb[0] = (target_bb[0] / 1280) * 640
    target_bb[1] = (target_bb[1] / 720) * 360
    target_bb[2] = (target_bb[2] / 1280) * 640
    target_bb[3] = (target_bb[3] / 720) * 360

    return target_bb

def set_font():
    font_path = "font/OpenSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 16)
    return font


def draw_bb(target, target_bb, detection):
    im = Image.open(target)
    draw = ImageDraw.Draw(im)

    score = float(detection[idx][1])
    if score < 0.1:
        # draw.rectangle(target_bb, outline=(int(float(detection[idx][1])*255), 0, 0, 0))
        draw.rectangle(target_bb, outline=(255, 0, 255, 0))
        draw.text((target_bb[0],target_bb[1]),"Normal",fill=(0,0,255,0),font=font)
    elif score < 0.15:
        draw.rectangle(target_bb, outline=(255, 0, 255, 0))
    elif score < 0.2:
        draw.rectangle(target_bb, outline=(0, 0, 255, 0))
    else:
        draw.rectangle(target_bb, outline=(0, 0, 255, 0))
    draw.text((target_bb[0],target_bb[1]),"text",fill=(0,0,0,0),font=font)

    del draw
    im.save("output/{0}.jpg".format(detection[idx][0]))


def read_match(vid_name):
    data_path = vid_name + "_raw.txt'"
    num_data = 1
    count = 0
    detection = []
    # read data
    for i in range(num_data):
        print(data_path[i] + " reading")
        with open(data_path[i], 'r') as f:
            for k in f:
                if count == 0:
                    count += 1
                    continue
                data = k.split(',')
                if data[0] == '\n':
                    # print(len(detection))
                    break
                data[5] = data[5][:-1]
                detection.append(data)

    for i in range(len(detection)):
        for j in range(len(detection[0])):
            detection[i][j] = float(detection[i][j])
            if j == 0:
                detection[i][j] = detection[i][j] / 10

    detection = detection[:-1]
    matches = []
    count = 0
    with open("scores.csv", 'r') as f:
        for k in f:
            match_box = []
            if count == 0:
                count += 1
                continue
            data = k.split(',')
            data[0] = data[0][:-4]
            data[1] = data[1][:-1]
            match_box = data[0].split('_')
            match_box.append(data[1])
            matches.append(match_box)

    count = 0
    for score in matches:
        for idx, data in enumerate(detection):
            if data[0] == float(score[0]):
                if score[1] == '2':
                    detection[idx + 1][1] = score[2]
                else:
                    detection[idx][1] = score[2]
                count += 1
                break
    return detection

def vid2img(vid_name):
    path_dir = "vid_save/"
    video_dir = vid_name + ".avi"
    my_clip = VideoFileClip(video_dir)
    duration = int(my_clip.duration)
    print(duration)
    count = 0.0
    ROI = 33612
    while count < duration:
        if count > ROI:
            my_clip.save_frame(path_dir + str(count) + ".jpg", count)  # normal은 너무 많아서 1초에 한장만
        count = round(count + 0.1, 1)
        if count > ROI + 100:
            break





vid_name = "amber_180604_000000"


path = os.getcwd()
image_path = 'output/'
images = os.listdir('vid_save')

prev_box = 0
detection = read_match(vid_name)
font = set_font()

for idx in range(len(detection)):
    # read image with detection
    target = image_path + str(detection[idx][0]) + ".jpg"

    # get bounding box
    target_bb = get_bb(detection)

    # Crop images
    Crop_save(target, target_bb, detection)

    # draw color box around object
    # draw_bb(target, target_bb, detection)





# from imageai.Detection import ObjectDetection
# import os
#
# path = os.getcwd()
# image_path = 'vid_save/'
#
# detector = ObjectDetection()
# detector.setModelTypeAsRetinaNet()
# detector.setModelPath(os.path.join(path,"resnet50_coco_best_v2.0.1.h5"))
# detector.loadModel()
#
# images = os.listdir('vid_save')
# print(images)
#
# for image in images:
#     target = detector.CustomObjects(person=True)
#     detections, extracted = detector.detectCustomObjectsFromImage(
#         custom_objects=target,
#         input_image=os.path.join(image_path, image),
#         output_image_path=os.path.join(path, "output/{0}.jpg".format(image)),
#         minimum_percentage_probability=60,
#         extract_detected_objects=True)
#

