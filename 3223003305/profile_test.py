# profile_test.py
"""
使用 cProfile 对论文查重系统进行性能分析
"""
from plagiarism_detector import calculate_similarity
import cProfile
import pstats

def run_test():
    # 模拟调用 calculate_similarity
    # 请确保这些文件存在：orig.txt, orig_0.8_add.txt
    try:
        similarity = calculate_similarity("orig.txt", "orig_0.8_add.txt")
        print(f"相似度: {similarity:.2f}%")
    except Exception as e:
        print(f"测试出错: {e}")

if __name__ == "__main__":
    # 使用 cProfile 分析性能
    profiler = cProfile.Profile()
    profiler.enable()

    run_test()

    profiler.disable()
    # 保存性能数据到文件
    profiler.dump_stats('plagiarism_profile.prof')
    print("性能分析完成，数据已保存到 plagiarism_profile.prof")