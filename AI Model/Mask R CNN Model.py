import os
import numpy as np
import cv2
import mrcnn.config
import mrcnn.utils
import sys
from mrcnn.model import MaskRCNN
from pathlib import Path

import requests


# 마스크 -RCNN 라이브러리가 사용할 구성
class MaskRCNNConfig(mrcnn.config.Config):
    NAME = "coco_pretrained_model_config"
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1
    NUM_CLASSES = 1 + 80   # COCO 데이터 세트에는 80 개의 클래스 + 하나의 백그라운드 클래스가 있습니다.
    DETECTION_MIN_CONFIDENCE = 0.6


# 탐지 된 자동차 / 트럭 만 얻으려면 마스크 R-CNN 검색 결과 목록을 필터링하십시오
def get_car_boxes(boxes, class_ids):
    car_boxes = []

    for i, box in enumerate(boxes):
        # If the detected object isn't a car / truck, skip it
        if class_ids[i] in [3, 8, 6]:
            car_boxes.append(box) 

    return np.array(car_boxes)

# 프로젝트의 루트 디렉토리
ROOT_DIR = os.path.abspath("../") #최상위 경로 지정
sys.path.append(ROOT_DIR)

# 로그 및 훈련 된 모델을 저장할 디렉토리
MODEL_DIR = os.path.join(ROOT_DIR , "logs")

# 훈련 된 Weight 파일에 대한 로컬 경로
COCO_MODEL_PATH = os.path.join(ROOT_DIR,"mask_rcnn_coco.h5")


if not os.path.exists(COCO_MODEL_PATH):
    mrcnn.utils.download_trained_weights(COCO_MODEL_PATH) 

# 검색을 실행할 이미지 디렉토리
IMAGE_DIR = os.path.join (ROOT_DIR,"images")

# 추론 모드에서 Mask-RCNN 모델을 만든다.
model = MaskRCNN (mode="inference", model_dir=MODEL_DIR, config=MaskRCNNConfig())

# 미리 훈련 된 모델로드
model.load_weights(COCO_MODEL_PATH, by_name=True)

# 주차 공간 위치
parked_car_boxes = None

# 탐지를 실행하려는 비디오 파일을로드합니다.
video_capture = cv2.VideoCapture('parking4.mp4')

# 우리는 열려있는 주차 공간이있는 행에서 본 적이 얼마나 많은 비디오의 프레임
free_space_frames = 0

# 김민중
xydic = dict()
xydicstate = dict()
url = 'http://119.77.100.41:8000'

# 동영상의 각 프레임을 반복합니다.
while video_capture.isOpened():
    success, frame = video_capture.read()
    if not success:
        break

    # BGR 색상 (OpenCV에서 사용)에서 RGB 색상으로 이미지 변환
    rgb_image = frame[:, :, ::-1]

    # 마스크 R-CNN 모델을 통해 이미지를 실행하여 결과를 얻습니다.
    results = model.detect([rgb_image], verbose=0)

    # 마스크 R-CNN은 여러 이미지에서 탐지를 실행한다고 가정합니다.
    # 우리는 단지 하나의 이미지를 통과하기 만 했으므로 첫 번째 결과 만 잡습니다.
    r = results[0]

    # r 변수는 이제 탐지 결과를 갖습니다 :
    # - r [ 'rois']는 탐지 된 각 객체의 경계 상자입니다
    # - r [ 'class_ids']는 탐지 된 각 객체의 클래스 ID (유형)입니다
    # - r [ 'scores']는 각 탐지에 대한 신뢰 점수입니다
    # - r [ 'masks']는 탐지 된 각 객체에 대한 객체 마스크입니다 (객체 개요를 제공합니다)


    if parked_car_boxes is None:
        # 이것은 비디오의 첫 번째 프레임입니다. 감지 된 모든 차량이 주차 공간에 있다고 가정합니다.
        # 각 차량의 위치를 ​​주차 공간 상자로 저장하고 다음 비디오 프레임으로 이동하십시오.
        parked_car_boxes = get_car_boxes(r['rois'], r['class_ids'])
    else :
        # 이미 주차 공간이 어디에 있는지 알고 있습니다. 현재 비어있는 지 확인하십시오.

        # 자동차가 현재 프레임에있는 곳을 찾으십시오.
        car_boxes = get_car_boxes(r['rois'], r['class_ids'])

        # 그 차가 알려진 주차 공간과 얼마나 겹치는 지보십시오
        overlaps = mrcnn.utils.compute_overlaps(parked_car_boxes, car_boxes)

        # 공백이 있다고 판단 할 때까지 공백이 없다고 가정합니다
        free_space = False

        

        # 각 알려진 주차 공간 상자를 반복합니다.
        for parking_area, overlap_areas in zip(parked_car_boxes, overlaps):
            xykey = ",".join(map(str,parking_area))
            # 이 주차 공간에 대해 주차 공간의 최대 금액을 찾으십시오.
            # 이미지에서 감지 된 차 (실제로 어떤 차가 아닌지) 
            max_IoU_overlap = np.max(overlap_areas)

            # 주차 영역의 왼쪽 위 및 오른쪽 아래 좌표 가져 오기
            y1, x1, y2, x2 = parking_area
            
            if xykey not in xydic:
                xydicstate[xykey] = 1
                xydic[xykey] = 0
                response = requests.get(url=url+"/initxy/"+xykey)
                print(response)

            # 차가 겹치는 지 확인하여 주차 공간이 가득 차 있는지 확인하십시오.
            # IoU를 사용하여 0.15 이상
            if max_IoU_overlap < 0.15:
                # 주위에 녹색 상자 그리기
                if xydic[xykey] < 5:
                    xydic[xykey] = xydic[xykey] + 1
                
                elif xydic[xykey] >= 5:
                    if xydicstate[xykey] == 1:
                        response = requests.get(url=url+"/addstack/"+xykey+"/"+str(xydic[xykey]))
                        xydicstate[xykey] *= -1


                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    # 우리가 적어도 하나의 열린 공간을 보았던 것을 나타내는 깃발
                    free_space = True
                  
            else:

                # 주차 공간이 여전히 채워져 있습니다. - 주위에 빨간색 상자를 그립니다.
                if xydic[xykey] == 5:
                    response = requests.get(url=url+"/substack/"+xykey)
                    xydicstate[xykey] *= -1

                xydic[xykey] = 0
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)

            # 상자 안에 IoU 측정 값을 씁니다.
            font = cv2.FONT_HERSHEY_DUPLEX

            cv2.putText(frame, f"{max_IoU_overlap:0.2}", (x1 + 6, y2 - 6), font, 0.3, (255, 255, 255))

        # 적어도 하나의 공간이 비어 있으면 프레임 계산 시작
        # 이것은 우리가 열리는 지점의 한 프레임에 기초하여 경고하지 않기 위해서입니다.
        # 이렇게하면 잘못된 탐지로 트리거 된 스크립트를 방지 할 수 있습니다.
        if free_space:
            free_space_frames += 1
        else:
            # 사용 가능한 스폿이없는 경우 카운트를 재설정하십시오
            free_space_frames = 0

        # 공간이 여러 프레임에 대해 자유라면, 우리는 그것이 정말로 무료라는 것을 꽤 확신합니다!
        """ if free_space_frames > 10 :
            # 공간을 쓰십시오 !! 화면 상단에
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, f"SPACE AVAILABLE!", (10, 150), font, 3.0, (0, 255, 0), 2, cv2.FILLED)

            # 아직 SMS를 보내지 않았다면 보내주십시오!
             if not sms_sent:
                print("SENDING SMS!!!")
                message = client.messages.create(
                    body="Parking space open - go go go!",
                    from_=twilio_phone_number,
                    to=destination_phone_number
                )
                sms_sent = True  """

        # 화면에 비디오 프레임 표시
        cv2.imshow('Video', frame)

     # 'q'를 눌러 종료하십시오.
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break 


# 완료되면 모든 것을 정리하십시오.
video_capture.release ()
cv2.destroyAllWindows ()