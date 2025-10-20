#!/usr/bin/env python3
import sys
import argparse
import os

# 添加当前目录到 Python 路径，确保可以导入模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator import ProblemGenerator
from checker import AnswerChecker

def main():
    parser = argparse.ArgumentParser(description='小学四则运算题目生成器')
    
    # 生成模式参数
    parser.add_argument('-n', '--count', type=int, help='生成题目的数量')
    parser.add_argument('-r', '--range', type=int, dest='number_range', help='数值范围')
    
    # 批改模式参数
    parser.add_argument('-e', '--exercise', type=str, help='题目文件')
    parser.add_argument('-a', '--answer', type=str, help='答案文件')
    
    args = parser.parse_args()
    
    # 检查参数
    if args.exercise and args.answer:
        # 批改模式
        print(f"正在批改题目文件: {args.exercise}, 答案文件: {args.answer}")
        checker = AnswerChecker()
        result = checker.check_answers(args.exercise, args.answer)
        if result:
            correct, wrong = result
            checker.save_grade(correct, wrong)
    elif args.count and args.number_range:
        # 生成模式
        if args.count <= 0 or args.number_range <= 0:
            print("错误: 参数必须为正整数")
            return
        
        if args.count > 10000:
            print("警告: 生成题目数量较多，可能需要较长时间")
        
        print(f"正在生成 {args.count} 道题目，数值范围: 1-{args.number_range}")
        generator = ProblemGenerator()
        problems, answers = generator.generate_problems(args.count, args.number_range)
        generator.save_to_files(problems, answers)
    else:
        print("错误: 参数不完整")
        print("生成模式: -n <题目数量> -r <数值范围>")
        print("批改模式: -e <题目文件> -a <答案文件>")
        print("\n示例:")
        print("  python main.py -n 10 -r 10")
        print("  python main.py -e Exercises.txt -a Answers.txt")
        sys.exit(1)

if __name__ == '__main__':
    main()