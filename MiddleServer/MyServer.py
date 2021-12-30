import os
import time
import hashlib

from flask import Flask, request, make_response, send_from_directory
import json

app = Flask(__name__)

pk_path = "./PublicKeys/"

# 假设存在用户集合
user_set = {}

# 假设存在数据集合
msg_set = {}

'''
# 假设存在用户集合
user_set = {
    "A": "./PublicKeys/A.pem",
    "B": "./PublicKeys/B.pem"
}

# 假设存在数据集合
msg_set = {
    "A": { # 发给A的消息
        "B": [
            {
                "msg": "Hello! I am B!",
                "datetime": 1640851079
            },
            {
                "msg": "Hi!",
                "datetime": 1640851090
            }
        ],
        "C": [
            {
                "msg": "This is C!",
                "datetime": 1640852014
            }
        ]
    },
    "B": {
        "C": [
            {
                "msg": "This is CCCC",
                "datetime": 1640861230
            }
        ]
    }
}
'''

@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/update', methods=["POST"])
def update(): # 上传公钥和个人相关信息，这里可以使用redis来做存储，
    posted_file = request.files['document']
    posted_data = json.load(request.files['data'])
    print(type(posted_file))
    print(posted_data)

    posted_file.save(pk_path + posted_data["uid"] + ".pem")
    uid = hashlib.md5(open(pk_path + posted_data["uid"] + ".pem", "rb").read()).hexdigest() # pk.pem的MD5值
    print(uid)
    if posted_data["uid"] == uid:
        user_set[uid] = pk_path + uid + ".pem"
        return "Update Done!"
    else:
        os.remove(pk_path + posted_data["uid"] + ".pem")
        return "Update Error!"


@app.route('/list', methods=["GET"])
def list_users(): # 返回所有的username信息
    response = {
        "users": list(user_set.keys())
    }
    return response

@app.route('/getkey', methods=["GET"])
def get_key(): # 请求某个用户id，返回其公钥
    uid = request.args.get("uid")

    if os.path.exists(pk_path + uid + ".\pem"):
        response = make_response(
            send_from_directory(pk_path, uid + ".pem", as_attachment=True))
        return response
    return "Error! Invalid UID!"

@app.route('/getmsg', methods=["GET"])
def get_msg(): # 发送自己的uid（使用自己的私钥签名），去服务器中请求有无自己的信息
    uid = request.args.get("uid")
    res = {}
    if os.path.exists(pk_path + uid + ".pem"):
        user_set[uid] = pk_path + uid + ".pem"
    if uid in msg_set.keys():
        msg = msg_set.pop(uid)
        res = {
            "result": True,
            "msg": msg
        }
    else:
        res = {
            "result": False
        }
    return json.dumps(res)

@app.route('/postmsg', methods=["POST"])
def post_msg(): # 发送自己的用户名、对方用户名、对方公钥加密的信息到中继服务器
    data = request.get_json()
    print(data)
    from_user = data["from"]
    to_user = data["to"]
    date = round(time.time())
    msg = {
        "msg": data["msg"],
        "datetime": date
    }

    # 更新用户在线列表
    if os.path.exists(pk_path + from_user + ".pem"):
        user_set[from_user] = pk_path + from_user + ".pem"

    # 判断用户是否存在
    if not os.path.exists(pk_path + to_user + ".pem"):
        return "User id is invalid!"
    else:
        # 发送消息
        if to_user in msg_set.keys():
            if from_user in msg_set[to_user].keys():
                msg_set[to_user][from_user].append(msg)
            else:
                msg_set[to_user][from_user] = [msg]
        else:
            msg_set[to_user] = {
                from_user: [msg]
            }
        return "Sended!"
    return 'Hello World!'

if __name__ == '__main__':
    app.run("0.0.0.0", threaded=True, port=1234)