# -*- coding: utf-8 -*-
from RSA.MyRSA import Rsa
import os
from RSA.MySigner import Signer
from config import *
import hashlib
import json
import requests

pk_path = "keys/public_key.pem"
sk_path = "keys/private_key.pem"

def main():
    _rsa = Rsa()
    ## 将类Rsa中的_rsa导入,使用单例模式
    if not (os.path.exists(pk_path) and os.path.exists(sk_path)):
        _rsa.createRsaKeysPem(byte=2048)  # 生成公私钥对
        print("Creating keys seccessful!")

    public_key = _rsa.fromPemLoadRsaPubKey(pk_path)  # 导入
    private_key = _rsa.fromPemLoadRsaPriKey(sk_path)

    # 上传公钥进行注册
    server_url = "http://" + Server_IP + ":" + str(Server_Port) + "/"

    # my file to be sent
    local_file_to_send = pk_path
    # with open(local_file_to_send, 'rb') as f:
    #     f.write('I am a file\n')

    # Ton to be sent
    uid = hashlib.md5(open(local_file_to_send, "rb").read()).hexdigest()
    data = {'uid': uid}

    url = server_url + "update"

    files = [
        ('document', (local_file_to_send, open(local_file_to_send, 'rb'), 'application/octet')),
        ('data', ('data', json.dumps(data), 'application/json')),
    ]

    r = requests.post(url, files=files)
    print(str(r.content, 'utf-8'))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

