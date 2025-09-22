# batch_test.py
"""
批量运行论文查重测试，针对 orig.txt 和 5 个抄袭版本
"""
import os
import subprocess
import sys

# 配置文件路径
ORIGINAL_FILE = "orig.txt"
PLAGIARIZED_FILES = [
    "orig_0.8_add.txt",
    "orig_0.8_del.txt",
    "orig_0.8_dis_1.txt",
    "orig_0.8_dis_10.txt",
    "orig_0.8_dis_15.txt"
]
OUTPUT_DIR = "results"  # 存放每个结果文件的目录

def main():
    # 创建结果目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"{'抄袭文件':<20} {'重复率(%)':<10}")
    print("-" * 30)

    for plag_file in PLAGIARIZED_FILES:
        if not os.path.exists(plag_file):
            print(f"{plag_file:<20} 文件不存在")
            continue

        # 构造输出文件路径
        output_file = os.path.join(OUTPUT_DIR, f"ans_{os.path.basename(plag_file)}.txt")

        # 调用主程序
        result = subprocess.run([
            sys.executable, "main.py",
            ORIGINAL_FILE,
            plag_file,
            output_file
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"{plag_file:<20} 错误: {result.stderr.strip()}")
        else:
            # 读取结果
            with open(output_file, 'r', encoding='utf-8') as f:
                sim = f.read().strip()
            print(f"{plag_file:<20} {sim:<10}")

if __name__ == "__main__":
    main()