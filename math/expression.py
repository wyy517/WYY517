import random
from fraction import Fraction

class Expression:
    """表达式类，生成和计算四则运算表达式"""
    
    def __init__(self, max_ops=3, number_range=10):
        self.max_ops = max_ops
        self.number_range = number_range
        self.expression = ""
        self.value = None
    
    def generate(self):
        """生成复杂表达式"""
        operators = ['+', '-', '×', '÷']
        
        for attempt in range(100):
            try:
                # 生成运算符数量（1到max_ops个）
                num_operators = random.randint(1, self.max_ops)
                
                # 生成表达式树
                self.expression, self.value = self._generate_expression_tree(
                    num_operators, operators, self.number_range)
                
                if (self.expression and self.value is not None and 
                    self._check_constraints()):
                    return f"{self.expression} = "
            except:
                continue
        
        return None
    
    def _generate_expression_tree(self, depth, operators, number_range, force_paren=False):
        """递归生成表达式树"""
        if depth == 0:
            # 叶子节点：生成数字
            num = Fraction.random_fraction(number_range)
            return str(num), num
        
        # 随机决定左右子树的深度
        if depth == 1:
            left_depth, right_depth = 0, 0
        else:
            left_depth = random.randint(0, depth - 1)
            right_depth = depth - 1 - left_depth
        
        # 生成左右子树
        left_expr, left_val = self._generate_expression_tree(left_depth, operators, number_range)
        right_expr, right_val = self._generate_expression_tree(right_depth, operators, number_range)
        
        # 选择运算符，考虑运算约束
        op = self._choose_operator(left_val, right_val, operators)
        
        if op is None:
            # 没有合适的运算符，重新生成
            return self._generate_expression_tree(depth, operators, number_range)
        
        # 计算当前表达式值
        current_value = self._apply_operator(left_val, right_val, op)
        if current_value is None:
            return self._generate_expression_tree(depth, operators, number_range)
        
        # 决定是否加括号
        need_paren = force_paren or self._need_parentheses(left_depth, right_depth)
        
        if need_paren:
            expression = f"({left_expr} {op} {right_expr})"
        else:
            expression = f"{left_expr} {op} {right_expr}"
        
        return expression, current_value
    
    def _choose_operator(self, left_val, right_val, operators):
        """根据数值约束选择合适的运算符"""
        valid_operators = []
        
        for op in operators:
            if op == '+':
                valid_operators.append(op)
            elif op == '-':
                # 确保减法不产生负数
                if left_val >= right_val:
                    valid_operators.append(op)
            elif op == '×':
                valid_operators.append(op)
            elif op == '÷':
                # 确保除数不为零且结果为真分数
                if (right_val != Fraction(0) and 
                    self._is_proper_fraction(left_val / right_val)):
                    valid_operators.append(op)
        
        return random.choice(valid_operators) if valid_operators else None
    
    def _apply_operator(self, left, right, op):
        """应用运算符计算"""
        try:
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '×':
                return left * right
            elif op == '÷':
                return left / right
        except:
            return None
    
    def _is_proper_fraction(self, fraction):
        """检查是否为真分数"""
        if not hasattr(fraction, 'denominator'):
            return True
        return abs(fraction.numerator) < abs(fraction.denominator)
    
    def _need_parentheses(self, left_depth, right_depth):
        """判断是否需要括号"""
        # 如果子树有运算，有一定概率加括号
        if left_depth > 0 or right_depth > 0:
            return random.random() < 0.4  # 40%概率加括号
        return False
    
    def _calculate_expression(self, expr):
        """计算表达式值（备用方法）"""
        try:
            calc_expr = expr.replace('×', '*').replace('÷', '/')
            return eval(calc_expr, {"Fraction": Fraction, "__builtins__": {}}, {})
        except:
            return None
    
    def _check_constraints(self):
        """检查约束条件"""
        if self.value is None:
            return False
        
        # 检查无负数
        if self.value < Fraction(0):
            return False
        
        # 检查所有运算结果都合理
        return True
    
    def get_value(self):
        """获取表达式值"""
        return self.value