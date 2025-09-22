# test_plagiarism.py
import pytest
import os
from plagiarism_detector import preprocess, longest_common_subsequence_length, calculate_similarity

# 临时测试文件
TEST_ORIG = "test_orig.txt"
TEST_PLAG = "test_plag.txt"


def setup_function():
    """每条测试前创建测试文件"""
    with open(TEST_ORIG, "w", encoding="utf-8") as f:
        f.write("今天是星期天，天气晴，今天晚上我要去看电影。")
    with open(TEST_PLAG, "w", encoding="utf-8") as f:
        f.write("今天是周天，天气晴朗，我晚上要去看电影。")


def teardown_function():
    """每条测试后删除测试文件"""
    for f in [TEST_ORIG, TEST_PLAG]:
        if os.path.exists(f):
            os.remove(f)


# 1. 测试预处理函数
def test_preprocess():
    text = "今天是星期天！！天气 晴。"
    result = preprocess(text)
    assert result == list("今天是星期天天气晴")


# 2. LCS 空序列
def test_lcs_empty():
    assert longest_common_subsequence_length([], ['a', 'b']) == 0


# 3. LCS 完全相同
def test_lcs_identical():
    a = ['a', 'b', 'c']
    assert longest_common_subsequence_length(a, a) == 3


# 4. LCS 无交集
def test_lcs_no_match():
    a = ['a', 'b']
    b = ['c', 'd']
    assert longest_common_subsequence_length(a, b) == 0


# 5. LCS 部分匹配
def test_lcs_partial():
    a = list("abcde")
    b = list("axcye")
    assert longest_common_subsequence_length(a, b) == 3  # a,c,e


# 6. 正常查重
def test_calculate_similarity_normal():
    sim = calculate_similarity(TEST_ORIG, TEST_PLAG)
    assert 0 <= sim <= 100


# 7. 原文为空
def test_empty_original():
    with open("empty.txt", "w", encoding="utf-8") as f:
        f.write("")
    with pytest.raises(ValueError):
        calculate_similarity("empty.txt", TEST_PLAG)
    os.remove("empty.txt")


# 8. 文件不存在
def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        calculate_similarity("not_exist.txt", TEST_PLAG)


# 9. 读取失败（模拟权限问题等）
def test_io_error(monkeypatch):
    def mock_read(*args, **kwargs):
        raise OSError("Permission denied")

    monkeypatch.setattr("builtins.open", mock_read)
    with pytest.raises(IOError):
        calculate_similarity(TEST_ORIG, TEST_PLAG)


# 10. 完全一致，重复率100%
def test_full_match():
    with open("orig.txt", "w", encoding="utf-8") as f:
        f.write("abc")
    with open("copy.txt", "w", encoding="utf-8") as f:
        f.write("abc")
    sim = calculate_similarity("orig.txt", "copy.txt")
    assert sim == 100.00
    os.remove("orig.txt")
    os.remove("copy.txt")


# 11. 完全不同，重复率0%
def test_no_match():
    with open("a.txt", "w", encoding="utf-8") as f:
        f.write("abc")
    with open("b.txt", "w", encoding="utf-8") as f:
        f.write("xyz")
    sim = calculate_similarity("a.txt", "b.txt")
    assert sim == 0.00
    os.remove("a.txt")
    os.remove("b.txt")


# 12. 抄袭文比原文长
def test_plagiarized_longer():
    with open("short.txt", "w", encoding="utf-8") as f:
        f.write("a")
    with open("long.txt", "w", encoding="utf-8") as f:
        f.write("abcde")
    sim = calculate_similarity("short.txt", "long.txt")
    assert sim == 100.00  # 因为原文"a"在抄袭文中存在
    os.remove("short.txt")
    os.remove("long.txt")