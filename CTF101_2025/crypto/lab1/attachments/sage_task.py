from sage.all import *
import random


def generate_random_flag():
    # 生成符合格式的随机 flag (AAA{...})
    prefix = "AAA{"
    suffix = "}"
    # 生成 25 个随机字符（所有ASCII可打印字符：32-126）
    printable_chars = "".join(chr(i) for i in range(32, 127))
    middle = "".join(random.choices(printable_chars, k=25))
    return prefix + middle + suffix


# 任务1：随机生成可逆矩阵 MT 并求逆矩阵
def task1():
    while True:
        # 生成随机 3x3 矩阵（元素范围 0-255）
        MT = matrix(
            Zmod(256), [[random.randint(0, 255) for _ in range(3)] for _ in range(3)]
        )
        if MT.is_invertible():
            MT_inv = MT.inverse()
            return MT, MT_inv


# 任务2：生成 flag 并验证加解密过程
def task2(MT):
    flag = generate_random_flag()
    # 将 flag 转换为 3x10 矩阵（按列填充）
    FT = matrix(Zmod(256), 3, 10)
    for i in range(3):
        for j in range(10):
            FT[i, j] = ord(flag[i + j * 3])
    # 计算 RT = MT * FT
    RT = MT * FT
    # 通过 RT 和 MT 恢复 FT
    FT_recovered = MT.inverse() * RT
    # 验证恢复的 FT 是否与原 FT 一致
    return FT, FT_recovered, flag


# 主程序
def main():
    print("任务1: 随机生成可逆矩阵 MT 并求逆矩阵")
    MT, MT_inv = task1()
    print("\n生成的 MT 矩阵:")
    print(MT)
    print("\nMT 的逆矩阵:")
    print(MT_inv)
    print("\n验证 MT * MT_inv = 单位矩阵:")
    print(MT * MT_inv)  # 应显示单位矩阵
    print("任务2: 生成 flag 并验证加解密过程")
    FT, FT_recovered, flag = task2(MT)
    print("\n原始 flag:", flag)
    print("\n原始 FT 矩阵:")
    print(FT)
    print("\n恢复的 FT 矩阵:")
    print(FT_recovered)
    print("\n验证结果:", "成功" if FT == FT_recovered else "失败")
    # 从恢复的 FT 矩阵重构 flag
    recovered_flag = ""
    for j in range(10):
        for i in range(3):
            char_code = FT_recovered[i, j].lift_centered()
            if char_code < 0:  # 处理负值
                char_code += 256
            recovered_flag += chr(char_code)
    print("\n重构的 flag:", recovered_flag)
    print("flag 匹配:", "成功" if flag == recovered_flag else "失败")


if __name__ == "__main__":
    main()
