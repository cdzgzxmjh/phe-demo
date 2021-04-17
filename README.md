## 一个简单的PHE（部分同态加密）例子
同态加密（基于PHE）的一个简单例子，模拟客户端与云端通信  
PHE算法取自 data61/python-paillier 项目，url: https://github.com/data61/python-paillier
此同态算法支持：
1. 加密数据相加
2. 加密数据与非加密数据相加
3. 加密数据与非加密数据相乘

例子为加密数据相加