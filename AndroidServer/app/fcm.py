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
            'message': body
        }
    }

    # json 파싱 후 requests 모듈로 FCM 서버에 요청
    print(requests.post(url, data=json.dumps(content), headers=headers))