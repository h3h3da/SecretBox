# -*- coding: utf-8 -*-
from RSA.MyRSA import Rsa
import os
from RSA.MySigner import Signer
import hashlib
from config import *
import requests
import json
from threading import Timer
import time
import base64

pk_path = "keys/public_key.pem"
sk_path = "keys/private_key.pem"

def get_msg():
    _rsa = Rsa()
    public_key = _rsa.fromPemLoadRsaPubKey(pk_path)  # 导入
    private_key = _rsa.fromPemLoadRsaPriKey(sk_path)
    uid = hashlib.md5(open(pk_path, "rb").read()).hexdigest()
    server_url = "http://" + Server_IP + ":" + str(Server_Port) + "/getmsg?uid=" + uid
    r = requests.get(url=server_url)
    res = json.loads(bytes.decode(r.content))
    if res["result"]:
        # print(res["msg"])
        for m in res["msg"].keys():
            print("From " + str(m) + ":")
            for i in res["msg"][m]:
                get_msg = bytes.decode(_rsa.decrypt(base64.b64decode(i["msg"])))
                print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(i["datetime"])) + " " + get_msg)
    else:
        pass
        # print("No message!")

def loop_func(func, second):
    # 每隔second秒执行func函数
    while True:
        timer = Timer(second, func)
        timer.start()
        timer.join()


def main():
    ## 将类Rsa中的_rsa导入,使用单例模式
    if not (os.path.exists(pk_path) and os.path.exists(sk_path)):
        print("请先注册！运行 python register.py")
    else:
        loop_func(get_msg, 3)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
