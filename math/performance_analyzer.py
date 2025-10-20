# performance_analyzer.py
import cProfile
import pstats
import io
import time
from generator import ProblemGenerator
from checker import AnswerChecker
import matplotlib.pyplot as plt

def performance_test_generation():
    """测试题目生成性能"""
    print("=== 题目生成性能测试 ===")
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    start_time = time.time()
    generator = ProblemGenerator()
    problems, answers = generator.generate_problems(100, 10)
    end_time = time.time()
    
    profiler.disable()
    
    print(f"生成100道题目耗时: {end_time - start_time:.2f}秒")
    
    # 输出性能分析结果
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(10)  # 显示前10个最耗时的函数
    
    print("性能分析结果:")
    print(s.getvalue())
    
    return profiler

def performance_test_checking():
    """测试答案批改性能"""
    print("\n=== 答案批改性能测试 ===")
    
    # 先生成测试文件
    generator = ProblemGenerator()
    problems, answers = generator.generate_problems(50, 10)
    generator.save_to_files(problems, answers, 'test_exercises.txt', 'test_answers.txt')
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    start_time = time.time()
    checker = AnswerChecker()
    correct, wrong = checker.check_answers('test_exercises.txt', 'test_answers.txt')
    end_time = time.time()
    
    profiler.disable()
    
    print(f"批改50道题目耗时: {end_time - start_time:.2f}秒")
    
    # 输出性能分析结果
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(10)
    
    print("性能分析结果:")
    print(s.getvalue())
    
    return profiler

def generate_performance_chart():
    """生成性能分析图表"""
    # 模拟性能数据（根据实际分析结果调整）
    functions = [
        'Expression._generate_expression_tree',
        'Fraction.simplify', 
        'AnswerChecker._evaluate_expression',
        'Fraction.random_fraction',
        'ProblemGenerator.generate_problems'
    ]
    
    time_percentage = [45, 25, 20, 5, 5]  # 百分比
    cumulative_time = [120, 80, 50, 15, 10]  # 累计时间(秒)
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 饼图 - 时间占比
    ax1.pie(time_percentage, labels=functions, autopct='%1.1f%%', startangle=90)
    ax1.set_title('函数时间占比分析')
    
    # 柱状图 - 累计时间
    bars = ax2.bar(functions, cumulative_time, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'])
    ax2.set_title('函数累计执行时间')
    ax2.set_ylabel('时间 (秒)')
    ax2.tick_params(axis='x', rotation=45)
    
    # 在柱子上显示数值
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}s',
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('performance_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def detailed_analysis():
    """详细性能分析"""
    print("=== 详细性能分析 ===")
    
    profiler = performance_test_generation()
    
    # 分析最耗时的函数
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s)
    
    print("\n最耗时的函数 (按执行时间排序):")
    ps.sort_stats('time').print_stats(10)
    
    print("\n调用次数最多的函数:")
    ps.sort_stats('calls').print_stats(10)
    
    print("\n每个函数的平均执行时间:")
    ps.sort_stats('tottime').print_stats(10)

if __name__ == "__main__":
    # 运行性能测试
    performance_test_generation()
    performance_test_checking()
    
    # 生成图表
    generate_performance_chart()
    
    # 详细分析
    detailed_analysis()