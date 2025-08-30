def calculate_coincidence_count(ciphertext, key_length):
    """
    计算给定密钥长度下，相隔该长度的字符重合次数
    """
    coincidence_count = 0
    # 遍历密文，计算相隔key_length距离的字符重合次数
    for i in range(len(ciphertext) - key_length):
        if ciphertext[i] == ciphertext[i + key_length]:
            coincidence_count += 1

    return coincidence_count


def find_key_length_by_coincidence(ciphertext, min_key_length, max_key_length):
    """
    通过统计重合次数来寻找最可能的密钥长度
    """
    results = []
    print("正在分析密钥长度...")
    print("密钥长度 | 重合次数 | 重合率")
    print("-" * 35)
    for length in range(min_key_length, max_key_length + 1):
        coincidence_count = calculate_coincidence_count(ciphertext, length)
        # 计算重合率（重合次数/可比较的字符对数）
        total_pairs = len(ciphertext) - length
        coincidence_rate = coincidence_count / total_pairs if total_pairs > 0 else 0
        results.append((length, coincidence_count, coincidence_rate))
        print(f"{length:8d} | {coincidence_count:8d} | {coincidence_rate:.4f}")
    # 按重合次数排序，找出最可能的密钥长度
    results.sort(key=lambda x: x[1], reverse=True)
    print("\n" + "=" * 50)
    print("最可能的密钥长度（按重合次数排序）：")
    print("排名 | 密钥长度 | 重合次数 | 重合率")
    print("-" * 40)
    for i, (length, count, rate) in enumerate(results[:10]):
        print(f"{i+1:3d} | {length:8d} | {count:8d} | {rate:.4f}")
    return results


def calculate_index_of_coincidence(text):
    """
    计算重合指数（Index of Coincidence）
    用于验证密钥长度的正确性
    """
    from collections import Counter

    char_counts = Counter(text)
    n = len(text)
    if n <= 1:
        return 0
    ic = sum(count * (count - 1) for count in char_counts.values()) / (n * (n - 1))
    return ic


def analyze_key_length_with_ic(ciphertext, min_key_length, max_key_length):
    """
    结合重合指数分析密钥长度
    """
    print("\n使用重合指数分析：")
    print("密钥长度 | 平均重合指数")
    print("-" * 25)
    ic_results = []
    # 确保最大长度不超过密文长度
    effective_max = min(max_key_length, len(ciphertext) - 1)
    for length in range(min_key_length, effective_max + 1):
        # 将密文按密钥长度分组
        groups = ["" for _ in range(length)]
        for i, char in enumerate(ciphertext):
            groups[i % length] += char
        # 计算每组的重合指数
        group_ics = [calculate_index_of_coincidence(group) for group in groups if group]
        avg_ic = sum(group_ics) / len(group_ics) if group_ics else 0
        ic_results.append((length, avg_ic))
        print(f"{length:8d} | {avg_ic:.6f}")
    # 按重合指数排序（重合指数越高，越可能是正确的密钥长度）
    ic_results.sort(key=lambda x: x[1], reverse=True)
    print("\n最可能的密钥长度（按重合指数排序）：")
    print("排名 | 密钥长度 | 重合指数")
    print("-" * 30)
    for i, (length, ic) in enumerate(ic_results[:10]):
        print(f"{i+1:3d} | {length:8d} | {ic:.6f}")
    return ic_results


def get_user_input():
    """
    获取用户输入的密钥长度范围
    """
    try:
        print("请设置密钥长度搜索范围：")
        min_length = int(input("最小密钥长度 (默认: 1): ") or "1")
        max_length = int(input("最大密钥长度 (默认: 50): ") or "50")
        if min_length < 1:
            print("最小密钥长度设置为 1")
            min_length = 1
        if max_length < min_length:
            print(f"最大密钥长度不能小于最小值，设置为 {min_length}")
            max_length = min_length
        print(f"搜索范围: {min_length} - {max_length}")
        return min_length, max_length
    except ValueError:
        print("输入无效，使用默认值: 1 - 50")
        return 1, 50


def main():
    # 读取密文
    try:
        with open("cipher.txt", "r") as f:
            ciphertext = f.read()
        print(f"密文长度: {len(ciphertext)} 字符")
        print("=" * 60)
        # 获取用户输入的密钥长度范围
        min_key_length, max_key_length = get_user_input()
        print("=" * 60)
        # 方法1: 重合次数统计
        coincidence_results = find_key_length_by_coincidence(
            ciphertext, min_key_length, max_key_length
        )
        # 方法2: 重合指数分析
        ic_results = analyze_key_length_with_ic(
            ciphertext, min_key_length, max_key_length
        )
        print("\n" + "=" * 60)
        print("综合分析结果：")
        # 综合两种方法的结果
        top_coincidence = [x[0] for x in coincidence_results[:5]]
        top_ic = [x[0] for x in ic_results[:5]]
        # 找出在两个列表中都出现的密钥长度
        common_lengths = set(top_coincidence) & set(top_ic)
        if common_lengths:
            print(f"两种方法都支持的密钥长度: {sorted(common_lengths)}")
        print(f"重合次数法推荐: {top_coincidence}")
        print(f"重合指数法推荐: {top_ic}")
        # 给出最终建议
        if coincidence_results:
            most_likely = coincidence_results[0][0]
            print(f"\n建议尝试的密钥长度: {most_likely}")
    except FileNotFoundError:
        print("错误：找不到 cipher.txt 文件")
    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    main()
