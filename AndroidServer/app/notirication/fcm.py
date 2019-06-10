import requests
import json


def send_fcm_notification(ids, title, body):
    # fcm 푸시 메세지 요청 주소
    url = 'https://fcm.googleapis.com/fcm/send'
    
    # 인증 정보(서버 키)를 헤더에 담아 전달
    headers = {
        'Authorization': 'key=AAAA2K1rvTQ:APA91bFKifL_hpENCus6Bo43nsP4cLmgolqYlzK8TWN82qE7bxImyPeG1iejUCj6pRQnFgCU-qERQKYpTWCZrSJwVZ5D-Nort3Jcuy2QaJCIdDb5nkyrrV6vgoJ_ffiRh2i9hr_l_iIW',
        'Content-Type': 'application/json; UTF-8',
    }

    # 보낼 내용과 대상을 지정
    content = {
        'registration_ids': [ids,],
        'notification': {
            'title': title,
            'body': body
        },
        'data':{
            'title': title,
            'message' : body
            
        }
    }

    # json 파싱 후 requests 모듈로 FCM 서버에 요청
    print(requests.post(url, data=json.dumps(content), headers=headers))

send_fcm_notification("czoE9Zk5Hw0:APA91bFrwGFHzvrYtvIDWtIFka46sQYv8J5i8LT7xeD2ng_-QayO54w4qisUe2d9trPl3awlM_TFLeh_280rvHdd7D1PaooUcGIhoZFs2Lz5MWr9XArqW5hFjU6sjnLvYEzjUEWONsHU"\
    ,"자리가 비었습니다.","효빈이 자리가 비었습니다.")