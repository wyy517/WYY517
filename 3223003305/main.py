# main.py
"""
论文查重主程序
命令行调用方式：
    python main.py <原文路径> <抄袭文路径> <输出路径>
"""
import sys
from plagiarism_detector import calculate_similarity


def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <original_file> <plagiarized_file> <output_file>")
        sys.exit(1)

    orig_path = sys.argv[1]
    plag_path = sys.argv[2]
    output_path = sys.argv[3]

    try:
        similarity = calculate_similarity(orig_path, plag_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"{similarity:.2f}\n")
        print(f"查重完成，重复率: {similarity:.2f}%，结果已保存至 {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
