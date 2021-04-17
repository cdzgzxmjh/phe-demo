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


class Client:
    def __init__(self, pub_key, pri_key, encrypted_x=None, encrypted_y=None):
        self.pub_key = pub_key
        self.pri_key = pri_key
        self.encrypted_x = encrypted_x
        self.encrypted_y = encrypted_y

    def encrypt(self, x, y):
        encoded_x = ExampleEncodedNumber.encode(self.pub_key, x)
        encoded_y = ExampleEncodedNumber.encode(self.pub_key, y)
        self.encrypted_x = self.pub_key.encrypt(encoded_x)
        self.encrypted_y = self.pub_key.encrypt(encoded_y)

    @classmethod
    def evaluate(cls, x, y):
        return x + y

    @classmethod
    def expect(cls, x, y):
        return x + y

    def decrypt(self, encrypted):
        return self.pri_key.decrypt_encoded(encrypted, ExampleEncodedNumber).decode()


class Cloud:
    def __init__(self, pub_key, evaluate):
        self.pub_key = pub_key
        self.evaluate = evaluate

    def calculate(self, x, y):
        return self.evaluate(x, y)


def math_example(pub_key, pri_key, a, b, h=None):
    client = Client(pub_key, pri_key)
    client.encrypt(a, b)
    cloud = Cloud(pub_key, Client.evaluate)
    encrypted = cloud.calculate(client.encrypted_x, client.encrypted_y)
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
