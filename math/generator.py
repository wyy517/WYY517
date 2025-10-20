import os
import random  # 添加这行
from expression import Expression

class ProblemGenerator:
    """题目生成器"""
    
    def __init__(self):
        self.generated_expressions = set()
    
    def generate_problems(self, count, number_range, max_ops=3):
        """生成指定数量的复杂题目"""
        problems = []
        answers = []
        
        print("正在生成复杂题目...")
        
        attempts = 0
        max_attempts = count * 10
        
        while len(problems) < count and attempts < max_attempts:
            attempts += 1
            
            # 随机选择运算符数量（1-3个）
            actual_ops = random.randint(1, max_ops)
            
            expr_gen = Expression(actual_ops, number_range)
            problem = expr_gen.generate()
            
            if problem and problem not in problems:
                answer = expr_gen.get_value()
                if answer is not None and self._is_valid_answer(answer, number_range):
                    # 规范化去重
                    normalized = self._normalize_expression(problem)
                    if normalized not in self.generated_expressions:
                        self.generated_expressions.add(normalized)
                        problems.append(problem)
                        answers.append(answer)
                        
                        if len(problems) % 5 == 0:
                            print(f"已生成 {len(problems)} 道题目")
        
        print(f"成功生成 {len(problems)} 道复杂题目")
        return problems, answers
    
    def _is_valid_answer(self, answer, number_range):
        """检查答案是否有效"""
        if answer is None:
            return False
        
        # 检查是否为负数
        if answer < 0:
            return False
        
        # 检查数值范围
        if hasattr(answer, 'numerator') and hasattr(answer, 'denominator'):
            if (abs(answer.numerator) > number_range * 3 or 
                abs(answer.denominator) > number_range * 2):
                return False
        
        return True
    
    def _normalize_expression(self, expr):
        """规范化表达式用于去重"""
        # 移除空格和等号进行简单去重
        return expr.replace(' ', '').replace('=', '').strip()
    
    def save_to_files(self, problems, answers, problem_file='Exercises.txt', 
                     answer_file='Answers.txt'):
        """保存题目和答案到文件"""
        # 保存题目
        with open(problem_file, 'w', encoding='utf-8') as f:
            for i, problem in enumerate(problems, 1):
                f.write(f"{i}. {problem}\n")
        
        # 保存答案
        with open(answer_file, 'w', encoding='utf-8') as f:
            for i, answer in enumerate(answers, 1):
                f.write(f"{i}. {answer}\n")
        
        print(f"\n生成完成！")
        print(f"题目文件: {problem_file}")
        print(f"答案文件: {answer_file}")
        
        # 显示所有题目和答案用于验证
        print("\n生成的复杂题目预览:")
        for i in range(min(10, len(problems))):
            print(f"  {i+1}. {problems[i]}{answers[i]}")