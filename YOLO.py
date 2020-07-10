from imageai.Detection import ObjectDetection
import os











path = os.getcwd()
image_path = 'color/'

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(path,"resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()

images = os.listdir('color')
# print(images)

for image in images:
    target = detector.CustomObjects(person=True)
    detections, extracted = detector.detectCustomObjectsFromImage(
        custom_objects=target,
        input_image=os.path.join(image_path, image),
        output_image_path=os.path.join(path, "output/{0}.jpg".format(image)),
        minimum_percentage_probability=60,
        extract_detected_objects=True)

