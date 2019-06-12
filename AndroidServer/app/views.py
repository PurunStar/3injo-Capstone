from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import fcm
# Create your views here.

xydic = dict()
linenum = list()
array1 = []
array2 = []
array3 = []
g_flag = 0
def initxy(reqeust, xy):
    if reqeust.method == "GET":
        xydic[xy] = 0
        
        global linenum
        linenum = []
        print("init :", xy)
        if int(xy.split(",")[0]) > 210 :
                array1.append(int(xy.split(",")[0]))
        elif int(xy.split(",")[0]) > 160 :
                array2.append(int(xy.split(",")[0]))
        elif int(xy.split(",")[0]) > 110 :
                array3.append(int(xy.split(",")[0]))
        return JsonResponse({'state' : 'secces',}, json_dumps_params = {'ensure_ascii': True})



def addstack(reqeust, xy, stack):  # 빈자리 생길때 호출 함수
    global g_flag
    if reqeust.method == "GET":
        g_flag+=1
        xydic[xy] = stack
        i = 0
        for a in linenum: # 1번라인, 2번라인, 3번라인

                if int(a) == 210:
                        if int(xy.split(",")[0]) in array1 :
                                fcm.send_fcm_notification("czoE9Zk5Hw0:APA91bFrwGFHzvrYtvIDWtIFka46sQYv8J5i8LT7xeD2ng_-QayO54w4qisUe2d9trPl3awlM_TFLeh_280rvHdd7D1PaooUcGIhoZFs2Lz5MWr9XArqW5hFjU6sjnLvYEzjUEWONsHU"\
                                ,"자리가 비었습니다.","햇님 주차장"+str(1)+ "번 자리가 생겼습니다.")
                if int(a) == 160:
                        if int(xy.split(",")[0]) in array2:

                                fcm.send_fcm_notification("czoE9Zk5Hw0:APA91bFrwGFHzvrYtvIDWtIFka46sQYv8J5i8LT7xeD2ng_-QayO54w4qisUe2d9trPl3awlM_TFLeh_280rvHdd7D1PaooUcGIhoZFs2Lz5MWr9XArqW5hFjU6sjnLvYEzjUEWONsHU"\
                                ,"자리가 비었습니다.","햇님 주차장"+str(2)+ "번 자리가 생겼습니다.")
                if int(a) == 110:
                        if int(xy.split(",")[0]) in array3 :
                                fcm.send_fcm_notification("czoE9Zk5Hw0:APA91bFrwGFHzvrYtvIDWtIFka46sQYv8J5i8LT7xeD2ng_-QayO54w4qisUe2d9trPl3awlM_TFLeh_280rvHdd7D1PaooUcGIhoZFs2Lz5MWr9XArqW5hFjU6sjnLvYEzjUEWONsHU"\
                                ,"자리가 비었습니다.","햇님 주차장"+str(3)+ "번 자리가 생겼습니다.")



                return JsonResponse({'state' : 'secces',}, json_dumps_params = {'ensure_ascii': True})


               
        print(xy, stack)
        return JsonResponse({'state' : 'secces',}, json_dumps_params = {'ensure_ascii': True})

def substack(reqeust, xy):
    global g_flag
    if reqeust.method == "GET":
        g_flag-=1
        xydic[xy] = 0  
        print(xy, "empty")
        return JsonResponse({'state' : 'se`cces',}, json_dumps_params = {'ensure_ascii': True})


#tensorflow
def getFlag(request,b):
        global g_flag
        if request.method == "GET":
                count = b
                emptystack = 0
                for flag in xydic.values():
                        if flag != 0:
                                emptystack += 1
                
                g_flag = emptystack+count
                return JsonResponse({'flag' : emptystack+count,}, json_dumps_params = {'ensure_ascii': True})

# android
def getFlag2(request):
        if request.method == "GET":
                return JsonResponse({'flag' : g_flag}, json_dumps_params = {'ensure_ascii': True})

# def exitCar(request):
#         global g_flag
#         if request.method == "GET":
#                 g_flag -= 1
#                 return JsonResponse({'flag' : g_flag}, json_dumps_params = {'ensure_ascii': True})

def setLine(request, ln):
        if request.method =="GET":
                if  ln not in linenum:
                        linenum.append(ln)
                else :
                        linenum.remove(ln)

                linenum.sort(reverse=True)

                return JsonResponse({'flag' : "emptystack",}, json_dumps_params = {'ensure_ascii': True})