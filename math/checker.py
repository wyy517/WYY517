from fraction import Fraction
import re

class AnswerChecker:
    """答案批改器"""
    
    def __init__(self):
        pass
    
    def check_answers(self, exercise_file, answer_file):
        """批改答案并返回对错统计"""
        try:
            problems = self._read_file(exercise_file)
            user_answers = self._read_file(answer_file)
        except FileNotFoundError as e:
            print(f"错误: {e}")
            return None
        
        if len(problems) != len(user_answers):
            print(f"警告: 题目数量({len(problems)})和答案数量({len(user_answers)})不匹配")
        
        correct_indices = []
        wrong_indices = []
        
        print("正在批改答案...")
        
        for i, (problem, user_answer) in enumerate(zip(problems, user_answers), 1):
            # 计算正确答案
            correct_answer = self._calculate_problem(problem)
            
            if correct_answer is None:
                print(f"警告: 第 {i} 题计算失败 - {problem}")
                wrong_indices.append(i)
                continue
            
            # 比较答案
            if self._compare_answers(user_answer, str(correct_answer)):
                correct_indices.append(i)
                print(f"第 {i} 题: ✓ 正确")
            else:
                wrong_indices.append(i)
                print(f"第 {i} 题: ✗ 错误")
                print(f"  题目: {problem}")
                print(f"  正确答案: {correct_answer}")
                print(f"  用户答案: {user_answer}")
                print()
        
        return correct_indices, wrong_indices
    
    def _read_file(self, filename):
        """读取文件内容"""
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 提取内容（去除序号）
        contents = []
        for line in lines:
            line = line.strip()
            if '. ' in line:
                content = line.split('. ', 1)[1]
                contents.append(content)
            else:
                contents.append(line)
        
        return contents
    
    def _calculate_problem(self, problem):
        """计算题目答案"""
        try:
            # 移除 "= " 部分
            if problem.endswith('= '):
                expr = problem[:-2].strip()
            else:
                expr = problem.strip()
            
            print(f"计算表达式: {expr}")  # 调试信息
            result = self._safe_eval_expression(expr)
            print(f"计算结果: {result}")  # 调试信息
            return result
        except Exception as e:
            print(f"计算错误: {problem} -> {e}")
            return None
    
    def _safe_eval_expression(self, expr):
        """安全计算表达式"""
        # 替换运算符
        expr = expr.replace('×', '*').replace('÷', '/')
        
        # 使用栈计算表达式
        return self._evaluate_expression(expr)
    
    def _evaluate_expression(self, expr):
        """计算表达式值"""
        def parse_token(token):
            """解析token为分数"""
            token = token.strip()
            if "'" in token:
                # 带分数
                parts = token.split("'")
                whole = int(parts[0])
                frac_parts = parts[1].split('/')
                num = int(frac_parts[0])
                den = int(frac_parts[1])
                return Fraction(whole * den + num, den)
            elif '/' in token:
                # 分数
                parts = token.split('/')
                return Fraction(int(parts[0]), int(parts[1]))
            else:
                # 整数
                return Fraction(int(token))
        
        # 简单的表达式计算（支持 +, -, *, /）
        tokens = self._tokenize(expr)
        numbers = []
        operators = []
        
        print(f"分词结果: {tokens}")  # 调试信息
        
        for token in tokens:
            if token in '+-*/':
                while (operators and self._get_precedence(operators[-1]) >= self._get_precedence(token)):
                    self._apply_operator(numbers, operators)
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    self._apply_operator(numbers, operators)
                operators.pop()  # 移除 '('
            else:
                numbers.append(parse_token(token))
        
        while operators:
            self._apply_operator(numbers, operators)
        
        return numbers[0] if numbers else None
    
    def _tokenize(self, expr):
        """将表达式分词"""
        # 使用正则表达式分割
        tokens = re.findall(r'\d+\'?\d*/\d+|\d+|[()+*/\-]', expr)
        return tokens
    
    def _get_precedence(self, op):
        """获取运算符优先级"""
        if op in '*/':
            return 2
        elif op in '+-':
            return 1
        else:
            return 0
    
    def _apply_operator(self, numbers, operators):
        """应用运算符"""
        if len(numbers) < 2 or not operators:
            return
        
        op = operators.pop()
        right = numbers.pop()
        left = numbers.pop()
        
        if op == '+':
            numbers.append(left + right)
        elif op == '-':
            numbers.append(left - right)
        elif op == '*':
            numbers.append(left * right)
        elif op == '/':
            numbers.append(left / right)
    
    def _compare_answers(self, answer1, answer2):
        """比较两个答案是否相等"""
        try:
            # 规范化答案
            norm1 = self._normalize_answer(answer1)
            norm2 = self._normalize_answer(answer2)
            return norm1 == norm2
        except:
            return False
    
    def _normalize_answer(self, ans):
        """规范化答案"""
        ans = ans.strip()
        if ans == '':
            return Fraction(0)
        
        # 解析各种格式的答案
        if "'" in ans:
            parts = ans.split("'")
            whole = int(parts[0])
            frac_parts = parts[1].split('/')
            num = int(frac_parts[0])
            den = int(frac_parts[1])
            if whole < 0:
                return Fraction(whole * den - num, den)
            return Fraction(whole * den + num, den)
        elif '/' in ans:
            parts = ans.split('/')
            return Fraction(int(parts[0]), int(parts[1]))
        else:
            return Fraction(int(ans))
    
    def save_grade(self, correct_indices, wrong_indices, grade_file='Grade.txt'):
        """保存批改结果"""
        with open(grade_file, 'w', encoding='utf-8') as f:
            f.write(f"Correct: {len(correct_indices)} ({', '.join(map(str, correct_indices))})\n")
            f.write(f"Wrong: {len(wrong_indices)} ({', '.join(map(str, wrong_indices))})\n")
        
        print(f"\n批改结果已保存到: {grade_file}")  # 修复这里
        print(f"正确: {len(correct_indices)} 题")
        print(f"错误: {len(wrong_indices)} 题")
        
        # 显示详细统计
        if correct_indices:
            print(f"正确题目编号: {correct_indices}")
        if wrong_indices:
            print(f"错误题目编号: {wrong_indices}")