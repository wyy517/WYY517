# plagiarism_detector.py
import os
import sys
import re
from typing import List


def preprocess(text: str) -> List[str]:
    """
    对文本进行预处理：去标点、转小写、分词（按字或词）。
    这里采用“按字”分词，适合中文。
    """
    # 去除标点符号和空白字符，保留汉字、字母、数字
    cleaned = re.sub(r'[^\w\s]', '', text)
    cleaned = re.sub(r'\s+', '', cleaned)  # 合并空格
    return list(cleaned.lower())


def longest_common_subsequence_length(seq1: List[str], seq2: List[str]) -> int:
    """
    计算两个序列的最长公共子序列（LCS）长度。
    使用动态规划，时间复杂度 O(m*n)，空间优化为 O(min(m,n))
    """
    if len(seq1) > len(seq2):
        seq1, seq2 = seq2, seq1  # 保证 seq1 是较短的

    m, n = len(seq1), len(seq2)
    if m == 0:
        return 0

    # 只用两行滚动数组
    prev = [0] * (m + 1)
    curr = [0] * (m + 1)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq2[i - 1] == seq1[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev  # 滚动

    return prev[m]


def calculate_similarity(orig_path: str, plagiarized_path: str) -> float:
    """
    计算重复率：LCS长度 / 原文长度
    """
    if not os.path.exists(orig_path):
        raise FileNotFoundError(f"原文文件不存在: {orig_path}")
    if not os.path.exists(plagiarized_path):
        raise FileNotFoundError(f"抄袭文件不存在: {plagiarized_path}")

    try:
        with open(orig_path, 'r', encoding='utf-8') as f:
            orig_text = f.read()
        with open(plagiarized_path, 'r', encoding='utf-8') as f:
            plag_text = f.read()
    except Exception as e:
        raise IOError(f"读取文件失败: {e}")

    if not orig_text.strip():
        raise ValueError("原文文件为空")

    orig_tokens = preprocess(orig_text)
    plag_tokens = preprocess(plag_text)

    lcs_len = longest_common_subsequence_length(orig_tokens, plag_tokens)
    similarity = lcs_len / len(orig_tokens)

    return round(similarity * 100, 2)  # 百分比，保留两位小数