import math
import random

class Fraction:
    """分数类，支持分数的各种运算"""
    
    def __init__(self, numerator, denominator=1):
        if denominator == 0:
            raise ValueError("分母不能为零")
        
        self.numerator = numerator
        self.denominator = denominator
        self.simplify()
    
    def simplify(self):
        """约分"""
        if self.numerator == 0:
            self.denominator = 1
            return
        
        gcd_val = math.gcd(abs(self.numerator), abs(self.denominator))
        self.numerator //= gcd_val
        self.denominator //= gcd_val
        
        # 确保分母为正
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator
    
    def to_mixed_number(self):
        """转换为带分数形式"""
        if self.denominator == 1:
            return str(self.numerator)
        
        whole = self.numerator // self.denominator
        remainder = abs(self.numerator) % self.denominator
        
        if whole == 0:
            if self.numerator < 0:
                return f"-{abs(self.numerator)}/{self.denominator}"
            return f"{self.numerator}/{self.denominator}"
        elif remainder == 0:
            return str(whole)
        else:
            if whole < 0:
                return f"{whole}'{remainder}/{self.denominator}"
            return f"{whole}'{remainder}/{self.denominator}"
    
    def to_improper_fraction(self):
        """将带分数转换为假分数"""
        if "'" in str(self.numerator):
            parts = str(self.numerator).split("'")
            whole = int(parts[0])
            frac_parts = parts[1].split('/')
            num = int(frac_parts[0])
            den = int(frac_parts[1])
            if whole < 0:
                return Fraction(whole * den - num, den)
            return Fraction(whole * den + num, den)
        return self
    
    def __add__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        common_denominator = self.denominator * other.denominator
        numerator = (self.numerator * other.denominator + 
                    other.numerator * self.denominator)
        return Fraction(numerator, common_denominator)
    
    def __sub__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        common_denominator = self.denominator * other.denominator
        numerator = (self.numerator * other.denominator - 
                    other.numerator * self.denominator)
        return Fraction(numerator, common_denominator)
    
    def __mul__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self.numerator * other.numerator, 
                       self.denominator * other.denominator)
    
    def __truediv__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        if other.numerator == 0:
            raise ValueError("除数不能为零")
        return Fraction(self.numerator * other.denominator, 
                       self.denominator * other.numerator)
    
    def __lt__(self, other):
        if other is None:
            return False
        if isinstance(other, int):
            other = Fraction(other)
        return (self.numerator * other.denominator < 
                other.numerator * self.denominator)
    
    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, int):
            other = Fraction(other)
        return (self.numerator * other.denominator == 
                other.numerator * self.denominator)
    
    def __le__(self, other):
        if other is None:
            return False
        return self < other or self == other
    
    def __gt__(self, other):
        if other is None:
            return False
        return not self <= other
    
    def __ge__(self, other):
        if other is None:
            return False
        return not self < other
    
    def __str__(self):
        return self.to_mixed_number()
    
    def __repr__(self):
        return f"Fraction({self.numerator}, {self.denominator})"
    
    @classmethod
    def random_fraction(cls, max_value):
        """生成随机分数"""
        if random.random() < 0.4:  # 40%概率生成整数
            return cls(random.randint(1, max_value - 1))  # 从1开始，避免0
        else:
            denominator = random.randint(2, max_value)
            numerator = random.randint(1, denominator - 1)  # 确保是真分数
            return cls(numerator, denominator)
    
    @classmethod
    def from_string(cls, s):
        """从字符串创建分数"""
        s = s.strip()
        if "'" in s:
            parts = s.split("'")
            whole = int(parts[0])
            frac_parts = parts[1].split('/')
            num = int(frac_parts[0])
            den = int(frac_parts[1])
            if whole < 0:
                return cls(whole * den - num, den)
            return cls(whole * den + num, den)
        elif '/' in s:
            parts = s.split('/')
            return cls(int(parts[0]), int(parts[1]))
        else:
            return cls(int(s))