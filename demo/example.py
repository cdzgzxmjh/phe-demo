#!/usr/bin/env python3.4
#
# author: maijiaheng
#
# PHE相关算法取自 data61/python-paillier 项目，url: https://github.com/data61/python-paillier
#
import math

import phe.encoding
from phe import paillier


class ExampleEncodedNumber(phe.encoding.EncodedNumber):
    BASE = 64
    LOG2_BASE = math.log(BASE, 2)


# 模拟客户端
class Client:
    # 必须定义密钥对
    def __init__(self, pub_key, pri_key, encrypted_x=None, encrypted_y=None):
        self.pub_key = pub_key
        self.pri_key = pri_key
        self.encrypted_x = encrypted_x
        self.encrypted_y = encrypted_y

    # 加密
    def encrypt(self, x, y):
        # 对加密数据进行编码包装，标识加密数据
        encoded_x = ExampleEncodedNumber.encode(self.pub_key, x)
        encoded_y = ExampleEncodedNumber.encode(self.pub_key, y)
        # 执行加密
        self.encrypted_x = self.pub_key.encrypt(encoded_x)
        self.encrypted_y = self.pub_key.encrypt(encoded_y)

    # 解密
    def decrypt(self, encrypted):
        return self.pri_key.decrypt_encoded(encrypted, ExampleEncodedNumber).decode()

    # 评估函数
    @classmethod
    def evaluate(cls, x, y):
        return x + y

    # 目标计算函数
    @classmethod
    def expect(cls, x, y):
        return x + y


# 模拟云服务
class Cloud:
    # 必须定义公钥与评估函数
    def __init__(self, pub_key, evaluate):
        self.pub_key = pub_key
        self.evaluate = evaluate

    # 模拟云服务计算
    def calculate(self, x, y):
        return self.evaluate(x, y)


def math_example(pub_key, pri_key, a, b, h=None):
    client = Client(pub_key, pri_key)
    # 客户端加密
    client.encrypt(a, b)
    cloud = Cloud(pub_key, Client.evaluate)
    # 云服务计算
    encrypted = cloud.calculate(client.encrypted_x, client.encrypted_y)
    # 客户端解密
    result = client.decrypt(encrypted)
    assert abs(Client.expect(p1, p2) - result) < 1e-15
    print("成功")


if __name__ == "__main__":
    print("生成密钥对...")
    public_key, private_key = paillier.generate_paillier_keypair()
    print("生成密钥对完毕")
    p1 = 102545 + (64 ** 8)
    p2 = 13254 + (8 ** 20)
    # 完成一次数学运算
    math_example(public_key, private_key, p1, p2)
