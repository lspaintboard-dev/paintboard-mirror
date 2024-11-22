from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.gzip import gzip_page
from PIL import Image
import base64
import io
from index.models import *


import time
import uuid
# import json
import requests

import index.config as cg
mapp = []
lstsavebd = 0.0
tokenlist = {}
reqip_a = {}
reqip_g = {}
ip_address = {}
mapppt = []
img = Image.new("RGB", (1000, 600))
cnt = {200: 0, 201: 0, 202: 0, 203: 0, 400: 0, 401: 0, 402: 0, 403: 0, 500: 0}


def initbd():
    for x in range(0, 600):
        mapp.append([])
        mapppt.append([])
        for y in range(0, 1000):
            mapp[x].append((255, 255, 255))
            mapppt[x].append(("unknown", 0, 0))


initbd()


def init_dict():
    for uid in cg.root:
        Tokenlist.objects.filter(uid=uid).delete()
        Tokenlist.objects.create(uid=uid, token=cg.roottext, time=0)
    tokenlist_all_from_db = Tokenlist.objects.all()
    for obj in tokenlist_all_from_db:
        tokenlist[obj.id] = {'token': obj.token, 'time': float(cg.start_time)}
    reqip_a_all_from_db = IpSpeed_a.objects.all()
    for obj in reqip_a_all_from_db:
        reqip_a[obj.ip] = {'time': float(obj.time), 'times': int(obj.times)}
    reqip_g_all_from_db = IpSpeed_g.objects.all()
    for obj in reqip_g_all_from_db:
        reqip_g[obj.ip] = {'time': float(obj.time), 'times': int(obj.times)}
    ip_address_all_from_db = Ip_address.objects.all()
    for obj in ip_address_all_from_db:
        ip_address[obj.ip] = obj.address


init_dict()


def get_ip(request):
    # print(str(request.META))
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def save_board():
    try:
        gb = requests.get(cg.url+cg.board)
        gb_text = gb.content
        for i in range(0, 1800000, 3):
            mapp[int((i/3) % 600)][int((i/3)//600)] = (gb_text[i],gb_text[i+1],gb_text[i+2])
        global img
        for i in range(0, 600):
            for j in range(0, 1000):
                img.putpixel((j, i), mapp[i][j])
        global getboard_last_save
        if (cg.need_to_save_as_file and time.time()-getboard_last_save > cg.save_to_db_cd):
            img.save("save/"+str(time.time())+".png")
        img.save("board.png")

    except Exception as e:
        print("Errorrrrrrrrrrrrrrrrrrrrrrrrrrr", str(e))


# IpSpeed_g.objects.all().delete()
# IpSpeed_a.objects.all().delete()

save_board()


getboard_need_update = 1

# what getboard last save
getboard_last_return = ""

# what time getboard last save
getboard_last_save = 0


def mklog(data, request):
    ip = get_ip(request)
    id = request.path
    ipt = {}
    if request.method == 'POST':
        ipt = str(dict(request.POST.items()))[:50]
    else:
        ipt = str(dict(request.GET.items()))[:50]
    print("["+id+"]", ip, ipt, "->", str(data)[:150])


def mkret(status, data, request):
    # if(int(status//100)!=2):

    cnt[status if (status != 204)else 203] += 1
    if (status == 203):
        mklog("", request)
        # 0, status=status)  # , content_type='image/gif')
        return HttpResponse(data)
    elif (status == 204):
        mklog("", request)
        return HttpResponse(data, content_type='image/png')  # status=203
    else:
        retl = {"status": status, "time": time.time(), "data": data}
        mklog(retl, request)
        return JsonResponse(retl, status=200)
    # if (status == 200):
    #     ret = str('\x00')
    # elif (status == 201):
    #     ret = str('\x01')+str(data)
    # elif (status == 203):
    #     ret = str(data)
    # else:
    #     ret = str(chr(status-400+16))
    # return HttpResponse(ret, status=status)

def send_req(mention,url,data={},retry=3):
    if(mention=="GET"):
        for _ in range(0,retry):
            ret = requests.get(url,json={})
            if(ret.status_code // 100 == 5):
                continue
            return ret
    elif(mention=="POST"):
        for _ in range(0,retry):
            ret = requests.post(url,json={})
            if(ret.status_code // 100 == 5):
                continue
            return ret
    else:
        raise TypeError
    raise ConnectionRefusedError



def speedcheck_a(request, authneed):
    # return 1
    nowt = time.time()
    if (authneed and nowt > cg.end_time):
        return 0
    if request.method == 'GET':
        uid = request.GET.get('uid', -1)
        token = request.GET.get('token', -1)
    else:
        uid = request.POST.get('uid', -1)
        token = request.POST.get('token', -1)
    checkres = ((not (uid == -1 and token == -1))) and (checktoken(uid, token))
    if (authneed and (not checkres)):
        return -1
    if (int(uid) in cg.root):
        return 1
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    get_reqip_from_dict = reqip_a.get(ip, None)
    if (get_reqip_from_dict == None):
        if (IpSpeed_a.objects.filter(ip=ip).exists()):
            get_reqip_from_db = IpSpeed_a.objects.filter(ip=ip).first()
            times = get_reqip_from_db.times
            time_ = float(get_reqip_from_db.time)
            reqip_a[ip] = {'times': times, 'time': time_}
        else:
            IpSpeed_a.objects.create(ip=ip, time=nowt, times=1)
            reqip_a[ip] = {'times': 1, 'time': nowt}
            return 1
    else:
        times = reqip_a[ip]['times']
        time_ = float(reqip_a[ip]['time'])
    if ((nowt-time_) > cg.iptime_a):
        # IpSpeed_a.objects.filter(ip=ip).update(time=nowt, times=1)
        reqip_a[ip]['times'] = 1
        return 1
    times += 1
    if (times <= cg.iptime_a_each):
        # IpSpeed_a.objects.filter(ip=ip).update(times=times)
        reqip_a[ip]['times'] = times
        return 1
    return 0


def speedcheck_g(request, authneed):
    # return 1
    nowt = time.time()
    if request.method == 'GET':
        uid = request.GET.get('uid', -1)
        token = request.GET.get('token', -1)
    else:
        uid = request.POST.get('uid', -1)
        token = request.POST.get('token', -1)
    checkres = ((not (uid == -1 and token == -1))) and (checktoken(uid, token))
    if (authneed and (not checkres)):
        return -1
    if (int(uid) in cg.root):
        return 1
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    get_reqip_from_dict = reqip_g.get(ip, None)
    if (get_reqip_from_dict == None):
        if (IpSpeed_g.objects.filter(ip=ip).exists()):
            get_reqip_from_db = IpSpeed_g.objects.filter(ip=ip).first()
            times = get_reqip_from_db.times
            time_ = float(get_reqip_from_db.time)
            reqip_g[ip] = {'times': times, 'time': time_}
        else:
            IpSpeed_g.objects.create(ip=ip, time=nowt, times=1)
            reqip_g[ip] = {'times': 1, 'time': nowt}
            return 1
    else:
        times = reqip_g[ip]['times']
        time_ = float(reqip_g[ip]['time'])
    if ((nowt-time_) > cg.iptime_g):
        # IpSpeed_g.objects.filter(ip=ip).update(time=nowt, times=1)
        reqip_g[ip] = {'times': 1, 'time': nowt}
        return 1
    times += 1
    if (times <= cg.iptime_g_each):
        # IpSpeed_g.objects.filter(ip=ip).update(times=times)
        reqip_g[ip]['times'] = times
        return 1
    return 0


def gettk(request):
    spck = speedcheck_a(request, 0)
    if (spck == 0):
        return mkret(401, {"error": "Too fast"}, request)
    if (spck == -1):
        return mkret(400, {"error": "Token Error"}, request)
    if request.method == 'POST':
        uid = request.POST['uid']
        paste = request.POST['paste']
    else:
        uid = request.GET['uid']
        paste = request.GET['paste']
    try:
        req = send_req("POST",cg.url+cg.paint,{"uid":uid,"paste":paste})
    except ConnectionRefusedError:
        return mkret(500, {"error":"can't reach the main server!!"}, request)
    return mkret(req.status_code, req.json(), request)


@gzip_page
def getboard(request):
    spck = speedcheck_g(request, 0)
    if (spck == 0):
        return mkret(401, {"error": "Too fast"}, request)
    if (spck == -1):
        return mkret(400, {"error": "Token Error"}, request)
    # mklog("",request)
    global getboard_need_update
    global getboard_last_return
    global getboard_last_save
    if (time.time()-getboard_last_save>cg.upd_from_server):
        save_board()
    ret = getboard_last_return
    return mkret(203, ret, request)


@gzip_page
def getboardasimg(request):
    spck = speedcheck_g(request, 0)
    if (spck == 0):
        return mkret(401, {"error": "Too fast"}, request)
    if (spck == -1):
        return mkret(400, {"error": "Token Error"}, request)
    global getboard_need_update
    global getboard_last_return
    global getboard_last_save
    if (time.time()-getboard_last_save>cg.upd_from_server):
        save_board()
    rett = io.BytesIO()
    img.save(rett, format='PNG')
    ret = rett.getvalue()

    return mkret(204, ret, request)


def checktoken(uid, token):
    return True


def paintboard(request):
    global getboard_last_return
    try:
        nowt = time.time()
        spck = speedcheck_a(request, 1)
        if (spck == 0):
            return mkret(401, {"error": "Too fast"}, request)
        if (spck == -1):
            return mkret(400, {"error": "Token Error"}, request)
        if request.method == 'POST':
            uid = request.POST.get('uid', None)
            token = request.POST.get('token', None)
            y = request.POST.get('y', None)
            x = request.POST.get('x', None)
            color = request.POST.get('color', None)
            lcapi = request.POST.get('lcapi', 1)
        else:
            uid = request.GET.get('uid', None)
            token = request.GET.get('token', None)
            y = request.GET.get('y', None)
            x = request.GET.get('x', None)
            color = request.GET.get('color', None)
            lcapi = request.GET.get('lcapi', 1)
        uid = int(uid)
        tt = tokenlist[uid]
        if ((not (uid in cg.root)) and (nowt-float(tt['time']) < cg.cd)):
            return mkret(402, {"error": "Paint too fast"}, request)
        # y = request.POST.get('y', None)
        if (y == None):
            return mkret(403, {"error": "Where is your 'y'?"}, request)
        try:
            y = int(y)
        except Exception:
            return mkret(403, {"error": "y incorrect"}, request)
        if (y > 599 or y < 0):
            return mkret(403, {"error": "y incorrect"}, request)
        # x = request.POST.get('x', None)
        if (x == None):
            return mkret(403, {"error": "Where is your 'x'?"}, request)
        try:
            x = int(x)
        except Exception:
            return mkret(403, {"error": "x incorrect"}, request)
        if (x > 999 or x < 0):
            return mkret(403, {"error": "x incorrect"}, request)
        if (color == None):
            return mkret(403, {"error": "Where is your 'color'?"}, request)
        try:
            color_ = int(color) if(not lcapi) else int(color,16)
        except Exception:
            return mkret(403, {"error": "color incorrect, or you should check your 'lcapi'"}, request)
        if (token == None):
            return mkret(403, {"error": "Where is your 'token'?"}, request)
        mapp[y][x] = color_
        mapppt[y][x] = (get_ip(request), uid, time.time())
        print(uid, "paint", color, "at", x, y)
        global getboard_need_update
        getboard_need_update = 1
        try:
            req = send_req("POST",cg.url+cg.paint,{"uid":uid,"token":token,"color":color_})
        except ConnectionRefusedError:
            return mkret(500, {"error":"can't reach the main server!!"}, request)
        return mkret(req.status_code, req.json(), request)
    except Exception as e:
        return mkret(500, {"error": str(e)}, request)


def banip(request):
    if request.method == 'GET':
        uid = request.GET.get('uid', -1)
        token = request.GET.get('token', -1)
        ip = request.GET.get('ip', -1)
    else:
        uid = request.POST.get('uid', -1)
        token = request.POST.get('token', -1)
        ip = request.POST.get('ip', -1)
    if ((not int(uid) in cg.root) or (not token == cg.roottext)):
        return mkret(400, {"error": "Token Error"}, request)
    IpSpeed_a.objects.filter(ip=ip).update(time=11451419198.0)
    IpSpeed_g.objects.filter(ip=ip).update(time=11451419198.0)
    reqip_a[ip]['time'] = 11451419198.0
    reqip_g[ip]['time'] = 11451419198.0
    return mkret(200, {"result": "Done"}, request)


def unbanip(request):
    if request.method == 'GET':
        uid = request.GET.get('uid', -1)
        token = request.GET.get('token', -1)
        ip = request.GET.get('ip', -1)
    else:
        uid = request.POST.get('uid', -1)
        token = request.POST.get('token', -1)
        ip = request.POST.get('ip', -1)
    if ((not int(uid) in cg.root) or (not token == cg.roottext)):
        return mkret(400, {"error": "Token Error"}, request)
    IpSpeed_a.objects.filter(ip=ip).update(time=cg.start_time)
    IpSpeed_g.objects.filter(ip=ip).update(time=cg.start_time)
    reqip_a[ip]['time'] = 0
    reqip_g[ip]['time'] = 0
    return mkret(200, {"result": "Done"}, request)


def banuid(request):
    if request.method == 'GET':
        uid = request.GET.get('uid', -1)
        token = request.GET.get('token', -1)
    else:
        uid = request.POST.get('uid', -1)
        token = request.POST.get('token', -1)
    if ((not int(uid) in cg.root) or (not token == cg.roottext)):
        return mkret(400, {"error": "Token Error"}, request)
    Tokenlist.objects.filter(uid=uid).update(time=11451419198.0)
    tokenlist[uid]['time'] = 11451419198.0
    return mkret(200, {"result": "Done"}, request)


def unbanuid(request):
    if request.method == 'GET':
        uid = request.GET.get('uid', -1)
        token = request.GET.get('token', -1)
    else:
        uid = request.POST.get('uid', -1)
        token = request.POST.get('token', -1)
    if ((not int(uid) in cg.root) or (not token == cg.roottext)):
        return mkret(400, {"error": "Token Error"}, request)
    Tokenlist.objects.filter(uid=uid).update(time=cg.start_time)
    tokenlist[uid]['time'] = 0
    return mkret(200, {"result": "Done"}, request)


def fill(request):
    return mkret(418, "", request)
    if request.method == 'GET':
        uid = request.GET.get('uid', -1)
        token = request.GET.get('token', -1)
        x1 = request.GET.get('x1', -1)
        x2 = request.GET.get('x2', -1)
        y1 = request.GET.get('y1', -1)
        y2 = request.GET.get('y2', -1)
        color = request.GET.get('color', -1)
    else:
        uid = request.POST.get('uid', -1)
        token = request.POST.get('token', -1)
        x1 = request.POST.get('x1', -1)
        x2 = request.POST.get('x2', -1)
        y1 = request.POST.get('y1', -1)
        y2 = request.POST.get('y2', -1)
        color = request.POST.get('color', -1)
    if ((not int(uid) in cg.root) or (not checktoken(uid, token))):
        return mkret(400, {"error": "Token Error"}, request)
    R, G, B = int(color[0:2], 16), int(
        color[2:4], 16), int(color[4:6], 16)
    for x in range(int(x1), int(x2)):
        for y in range(int(y1), int(y2)):
            mapp[y][x] = (R, G, B)
    global getboard_need_update
    global getboard_last_save
    getboard_need_update = 1
    getboard_last_save = 0
    return mkret(200, {"result": "Done"}, request)

def fillimg(request):
    return mkret(418, "", request)
    try:
        if request.method == 'GET':
            uid = request.GET.get('uid', -1)
            token = request.GET.get('token', -1)
            img = request.GET.get('img', -1)
            x = int(request.GET.get('x', -1))
            y = int(request.GET.get('y', -1))
        else:
            uid = request.POST.get('uid', -1)
            token = request.POST.get('token', -1)
            img = request.POST.get('img', -1)
            x = int(request.POST.get('x', -1))
            y = int(request.POST.get('y', -1))

        if ((not int(uid) in cg.root) or (not (checktoken(uid, token)))):
            return mkret(400, {"error": "Token Error"}, request)
        img = base64.b64decode(img)
        img = Image.open(io.BytesIO(img))
        sizzz = img.size
        for xx in range(x, x+sizzz[0]):
            for yy in range(y, y+sizzz[1]):
                if (xx >= 1000):
                    break
                if (yy >= 600):
                    break
                mapp[yy][xx] = img.getpixel((xx-x, yy-y))
        global getboard_need_update
        global getboard_last_save
        getboard_need_update = 1
        getboard_last_save = 0
        return mkret(200, {"result": "Done"}, request)
    except Exception as e:
        return mkret(500, {"error": str(e)}, request)


def ret_cnt(request):
    try:
        if request.method == 'GET':
            uid = request.GET.get('uid', -1)
            token = request.GET.get('token', -1)
        else:
            uid = request.POST.get('uid', -1)
            token = request.POST.get('token', -1)
        if ((not int(uid) in cg.root) or (not token == cg.roottext)):
            return mkret(400, {"error": "Token Error"}, request)
        return mkret(200, cnt, request)
    except Exception as e:
        return mkret(500, {"error": str(e)}, request)


def index(request):
    mklog("", request)
    return render(request, "index.html")


def querypaint(request):
    try:
        if request.method == 'GET':
            uid = request.GET.get('uid', -1)
            token = request.GET.get('token', -1)
            x = request.GET.get('x', None)
            y = request.GET.get('y', None)
        else:
            uid = request.POST.get('uid', -1)
            token = request.POST.get('token', -1)
            x = request.POST.get('x', None)
            y = request.POST.get('y', None)

        if ((not int(uid) in cg.root) or (not token == cg.roottext)):
            return mkret(400, {"error": "Token Error"}, request)
        if (x != None and y != None):
            x = int(x)
            y = int(y)
            return mkret(200, {"uid": mapppt[y][x][1]}, request)
        return mkret(200, mapppt, request)
    except Exception as e:
        return mkret(500, {"error": str(e)}, request)


def createtoken(request):
    return mkret(418, "", request)
    try:
        if request.method == 'GET':
            uid = request.GET.get('uid', -1)
            token = request.GET.get('token', -1)
            cuid = request.GET.get('cuid', -1)
        else:
            uid = request.POST.get('uid', -1)
            token = request.POST.get('token', -1)
            cuid = request.POST.get('cuid', -1)
        if ((not int(uid) in cg.root) or (not (checktoken(uid, token)))):
            return mkret(400, {"error": "Token Error"}, request)
        Tokenlist.objects.filter(uid=cuid).delete()
        tk = str(uuid.uuid4())
        Tokenlist.objects.create(uid=cuid, token=tk, time=0)
        tokenlist[cuid] = {'token': tk, 'time': 0}
        # print(tk)
        return mkret(201, {"token": tk}, request)

    except Exception as e:
        return mkret(500, {"error": str(e)}, request)
