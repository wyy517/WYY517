#!/usr/bin/env python3
from fraction import Fraction

# 测试基本功能
print("测试分数类...")
f1 = Fraction(1, 2)
f2 = Fraction(1, 3)
print(f"1/2 + 1/3 = {f1 + f2}")
print(f"1/2 - 1/3 = {f1 - f2}")
print("测试完成！")