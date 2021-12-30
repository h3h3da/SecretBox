import rsa
class Rsa():
    def __init__(self, public_key=None, private_key=None):
        self.public_key = public_key
        self.private_key = private_key
    def createRsaKeysPem(self, public_pem_save_path='./keys/public_key.pem', private_pem_save_path='./keys/private_key.pem', byte=2048):
        '''生成公私钥对，并将其序列化保存为文件'''
        (pub_key, pri_key) = rsa.newkeys(byte)
        with open(public_pem_save_path, 'wb+') as f:
            f.write(pub_key.save_pkcs1('PEM'))
        with open(private_pem_save_path, 'wb+') as f:
            f.write(pri_key.save_pkcs1('PEM'))
        return (pub_key, pri_key)

    def fromBytesLoadRsaPubKey(self, pk=None):
        if pk:
            self.public_key = rsa.PublicKey.load_pkcs1(pk)
        return self.public_key

    def fromBytesLoadRsaPriKey(self, sk=None):
        if sk:
            self.private_key = rsa.PrivateKey.load_pkcs1(sk)
        return self.private_key

    def fromPemLoadRsaPubKey(self, path='./keys/public_key.pem'):
        '''从文件导入公钥'''
        with open(path, 'rb') as f:
            pem = f.read()
            self.public_key = rsa.PublicKey.load_pkcs1(pem)
        return self.public_key

    def fromPemLoadRsaPriKey(self, path='./keys/private_key.pem'):
        '''从文件导入私钥'''
        with open(path, 'rb') as f:
            pem = f.read()
            self.private_key = rsa.PrivateKey.load_pkcs1(pem)
        return self.private_key

    def encrypt(self, data, public_key=None):
        '''使用公钥加密或验签，返回数据为bytes类型'''
        if public_key is None:
            public_key = self.public_key
        return rsa.encrypt(data, public_key)

    def decrypt(self, data, private_key=None):
        '''使用私钥解密或签名，返回数据为bytes类型'''
        if private_key is None:
            private_key = self.private_key
        return rsa.decrypt(data, private_key)