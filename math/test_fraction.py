#!/usr/bin/env python3
from fraction import Fraction

# 测试基本运算
print("=== 分数运算测试 ===")

# 测试 1/2 - 1/6
f1 = Fraction(1, 2)
f2 = Fraction(1, 6)
result = f1 - f2
print(f"1/2 - 1/6 = {result} (应该是 1/3)")
print(f"计算结果: {result.numerator}/{result.denominator}")

# 测试 1/4 - 1/2 (应该被拒绝，因为会产生负数)
f3 = Fraction(1, 4)
f4 = Fraction(1, 2)
try:
    result2 = f3 - f4
    print(f"1/4 - 1/2 = {result2} (这不应该出现，因为不能有负数)")
except:
    print("1/4 - 1/2 被正确拒绝（会产生负数）")

# 测试其他运算
print(f"\n=== 其他运算测试 ===")
print(f"1/3 + 1/6 = {Fraction(1,3) + Fraction(1,6)}")
print(f"2/3 × 1/2 = {Fraction(2,3) * Fraction(1,2)}")
print(f"1/2 ÷ 1/4 = {Fraction(1,2) / Fraction(1,4)}")