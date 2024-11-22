import base64
import requests

server_path = "https://pbd.uwuwu.us.kg"  # "127.0.0.1:8000"

uid = 0
token = ""


def ipt(text):
    print(text, end=" ")
    return input()


def auth():
    global uid
    global token
    uid = ipt("uid:")
    token = ipt("token:")


def req(path, **kwargs):
    try:
        kwargs["uid"] = uid
        kwargs["token"] = token
        path_all = server_path+"/paintboard/"+path
        print("req:", path_all)
        resp = requests.post(url=path_all, data=kwargs)
        print("resp:", resp.status_code, "\n", resp.text)
        if (resp.status_code == 500):
            return None
        return resp.json()['data']
    except Exception as e:
        print("req error:", str(e))
        return None


def ToBase64(file):
    with open(file, 'rb') as fileObj:
        data = fileObj.read()
        base64_data = base64.b64encode(data)
    return str(base64_data, 'utf-8')


def banip():
    ip = ipt("ip:")
    req("banip", ip=ip)


def unbanip():
    ip = ipt("ip:")
    req("unbanip", ip=ip)


def banuid():
    uid = ipt("uid:")
    req("banuid", uid=uid)


def unbanuid():
    uid = ipt("uid:")
    req("unbanuid", uid=uid)


def fill():
    color = ipt("color:")
    x1 = ipt("x1:")
    y1 = ipt("y1:")
    x2 = ipt("x2:")
    y2 = ipt("y2:")
    req("fill", color=color, x1=x1, y1=y1, x2=x2, y2=y2)


def fillimg():
    pathh = ipt("path:")
    x = ipt("x:")
    y = ipt("y:")
    tb64 = ToBase64(pathh)
    print("imgb64:", tb64)
    req("fillimg", img=tb64, x=x, y=y)


def errcnt():
    ret = req("errcnt")
    if (ret == None):
        return
    retdict = ret
    sum = 0
    for status in retdict:
        sum += retdict[status]
    for status in retdict:
        print(status, ":", '%.20f' % (retdict[status]/sum))

def createtoken():
    print("[fr,to)")
    fr = ipt("fr:")
    to = ipt("to:")
    ret=[]
    for cuid in range(int(fr), int(to)):
        reqq=req("createtoken", cuid=cuid)
        ret.append((cuid,reqq['token']))
    print(ret)

if __name__ == '__main__':
    auth()
    while (1):
        try:
            op = ipt(">")
            match (op):
                case ".banip":
                    banip()
                case ".unbanip":
                    unbanip()
                case ".banuid":
                    banuid()
                case ".unbanuid":
                    unbanuid()
                case ".fill":
                    fill()
                case ".fillimg":
                    fillimg()
                case ".errcnt":
                    errcnt()
                case ".createtoken":
                    createtoken()
                case ".exit":
                    break
                case _:
                    print("op not found")
        except Exception as e:
            print(str(e))
