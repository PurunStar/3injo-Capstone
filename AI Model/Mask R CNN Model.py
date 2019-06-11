import os
import numpy as np
import cv2
import mrcnn.config
import mrcnn.utils
import sys
from mrcnn.model import MaskRCNN
from pathlib import Path
import requests


class MaskRCNNConfig(mrcnn.config.Config):
    NAME = "coco_pretrained_model_config"
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1
    NUM_CLASSES = 1 + 80  
    DETECTION_MIN_CONFIDENCE = 0.6


def get_car_boxes(boxes, class_ids):
    car_boxes = []

    for i, box in enumerate(boxes):
        if class_ids[i] in [3, 8, 6]:
            car_boxes.append(box) 
    return np.array(car_boxes)


ROOT_DIR = os.path.abspath("../") 
sys.path.append(ROOT_DIR)

MODEL_DIR = os.path.join(ROOT_DIR , "logs")

COCO_MODEL_PATH = os.path.join(ROOT_DIR,"mask_rcnn_coco.h5")

if not os.path.exists(COCO_MODEL_PATH):
    mrcnn.utils.download_trained_weights(COCO_MODEL_PATH) 


IMAGE_DIR = os.path.join (ROOT_DIR,"images")

model = MaskRCNN (mode="inference", model_dir=MODEL_DIR, config=MaskRCNNConfig())

model.load_weights(COCO_MODEL_PATH, by_name=True)

parked_car_boxes = None

video_capture = cv2.VideoCapture('parking4.mp4')

free_space_frames = 0

xydic = dict()
xydicstate = dict()
url = 'http://119.77.100.41:8000'


while video_capture.isOpened():
    success, frame = video_capture.read()
    if not success:
        break

    rgb_image = frame[:, :, ::-1]

    results = model.detect([rgb_image], verbose=0)

    r = results[0]

    if parked_car_boxes is None:
        parked_car_boxes = get_car_boxes(r['rois'], r['class_ids'])
    else :
        car_boxes = get_car_boxes(r['rois'], r['class_ids'])
        overlaps = mrcnn.utils.compute_overlaps(parked_car_boxes, car_boxes)
        free_space = False

        for parking_area, overlap_areas in zip(parked_car_boxes, overlaps):
            xykey = ",".join(map(str,parking_area))
            max_IoU_overlap = np.max(overlap_areas)

            y1, x1, y2, x2 = parking_area
            
            if xykey not in xydic:
                xydicstate[xykey] = 1
                xydic[xykey] = 0
                response = requests.get(url=url+"/initxy/"+xykey)
                print(response)

            if max_IoU_overlap < 0.15:
                if xydic[xykey] < 5:
                    xydic[xykey] = xydic[xykey] + 1
                
                elif xydic[xykey] >= 5:
                    if xydicstate[xykey] == 1:
                        response = requests.get(url=url+"/addstack/"+xykey+"/"+str(xydic[xykey]))
                        xydicstate[xykey] *= -1

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    free_space = True
                  
            else:
                if xydic[xykey] == 5:
                    response = requests.get(url=url+"/substack/"+xykey)
                    xydicstate[xykey] *= -1

                xydic[xykey] = 0
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)

            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, f"{max_IoU_overlap:0.2}", (x1 + 6, y2 - 6), font, 0.3, (255, 255, 255))

        if free_space:
            free_space_frames += 1
        else:
            free_space_frames = 0
        cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
         break 

video_capture.release ()
cv2.destroyAllWindows ()