# quick_test.py
import random
from fraction import Fraction

print("=== 快速导入测试 ===")
print("random 模块导入成功!")
print("Fraction 类导入成功!")

# 测试基本功能
f1 = Fraction(1, 2)
f2 = Fraction(1, 3)
print(f"分数运算测试: 1/2 + 1/3 = {f1 + f2}")

# 测试随机数生成
print(f"随机数测试: {random.randint(1, 10)}")

print("所有基础模块工作正常!")