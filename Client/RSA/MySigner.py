import base64
from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class Signer():
    def __init__(self, public_key=None, private_key=None):
        self.public_key = public_key
        self.private_key = private_key

    def sign(self, message, private_key=None):
        if private_key is None:
            private_key = self.private_key
        with open(private_key, 'r') as f:
            private_key = f.read()
            rsa_key_obj = RSA.importKey(private_key)
            signer = PKCS1_v1_5.new(rsa_key_obj)
            # 先以单向加密方式通过某种哈希算法（如MD5，SHA1等）对要发送的数据生成摘要信息（数据指纹）
            digest = SHA1.new()
            digest.update(message.encode())
            # 然后发送方用自己密钥对中的私钥对这个摘要信息进行加密，生成签名信息
            signature = base64.b64encode(signer.sign(digest))
            print('signature info: ', signature)
            return signature

    def verigy(self, message, signature, public_key=None):
        # 验证签名, NEED: message,signature
        if public_key is None:
            public_key = self.public_key
        with open(public_key, 'r') as f:
            public_key = f.read()
            # 数据接收方用发送的公钥对加密后的摘要信息进行解密，得到数据摘要的明文A
            rsa_key_obj = RSA.importKey(public_key)
            signer = PKCS1_v1_5.new(rsa_key_obj)
            # 数据接收方再通过相同的哈希算法计算得到数据摘要信息B
            digest = SHA1.new(message.encode())
            # 对比数据摘要A与数据摘要B，如果两者一致说明数据没有被篡改过
            is_ok = signer.verify(digest, base64.b64decode(signature))
            print('is ok: ', is_ok)
            return is_ok