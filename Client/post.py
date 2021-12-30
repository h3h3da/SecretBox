import json
import requests
import hashlib
from config import *
from RSA.MyRSA import Rsa
import os
import base64

pk_path = "keys/public_key.pem"
sk_path = "keys/private_key.pem"

def main():
    _rsa = Rsa()
    public_key = _rsa.fromPemLoadRsaPubKey(pk_path)  # 导入
    private_key = _rsa.fromPemLoadRsaPriKey(sk_path)
    ## 将类Rsa中的_rsa导入,使用单例模式
    if not (os.path.exists(pk_path) and os.path.exists(sk_path)):
        print("请先注册！运行 python register.py")
    else:
        uid = hashlib.md5(open(pk_path, "rb").read()).hexdigest()
        server_url = Server_IP + ":" + str(Server_Port) + "/postmsg"
        print("WELCOME TO SECRET BOX!")
        while True:
            options = '''
1. Get User List
2. Post a message
0. Exit.
            '''
            opt = input(options)
            user = None
            while opt not in ['0', '1', '2']:
                opt = input(options)
            if opt == '0':
                print("Bye!")
                break
            elif opt == '1':
                url = "http://" + Server_IP + ":" + str(Server_Port) + "/list"
                r = requests.get(url=url)
                res = json.loads(bytes.decode(r.content))
                if res["users"]:
                    for user in res["users"]:
                        print(user)
            else:
                user = input("Please input user id:")
                # 获取对方的公钥
                get_pk_url = "http://" + Server_IP + ":" + str(Server_Port) + "/getkey?uid=" + user
                r = requests.get(url=get_pk_url)
                print(r.text)
                pks_path = "./pks/"
                if r.content != "Error! Invalid UID!":
                    with open(pks_path + user + ".pem", "wb") as f:
                        f.write(r.content)
                        f.close()
                    print(type(r.content))
                    print(pks_path + user + ".pem")
                    public_key = _rsa.fromPemLoadRsaPubKey(pks_path + user + ".pem")
                    msg = input("Please input message:")
                    e_msg = base64.encodebytes(_rsa.encrypt(str.encode(msg), public_key=public_key)).decode()

                    data = {
                        "from": uid,
                        "to": user,
                        "msg": e_msg
                    }
                    url = "http://" + Server_IP + ":" + str(Server_Port) + "/postmsg"
                    headers = {'Content-Type': 'application/json'}
                    r = requests.post(url, headers=headers, data=json.dumps(data))
                    print(r.text)
                else:
                    print("Please chose a user first!")
                # pk = pks_path + user + ".pem"
                '''
                if user:
                    msg = input("Please input message:")
                    data = {
                        "from": uid,
                        "to": user,
                        "msg": msg
                    }
                    url = "http://" + Server_IP + ":" + str(Server_Port) + "/postmsg"
                    headers = {'Content-Type': 'application/json'}
                    r = requests.post(url, headers=headers, data=json.dumps(data))
                    print(r.text)
                else:
                    print("Please chose a user first!")
                '''

if __name__ == "__main__":
    main()
