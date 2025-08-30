from sage.all import *

p = 960494008017250155494739990397196249930200062145145133132556398221074529657304218221253517153928380265486339083177542201148993799925721673833333778621388110957986908045712612233794551809
g = 3
c = 505527904713564983625416248872210831215228354175257237841602581321675204643681129570897695080321118656513647239718859773976453054734892142640867733520305568808093022238369199760987416665


def solve_discrete_log():
    """使用 SageMath 求解离散对数问题"""
    # 已知值
    print("=== 离散对数问题分析 ===")
    print(f"模数 p 的位数: {p.nbits()}")
    print(f"p 是素数: {is_prime(p)}")
    # 分析 p-1 的因式分解
    print("\n=== 分析 p-1 的因式分解 ===")
    p_minus_1 = p - 1
    # 检查小因子
    small_factors = []
    temp = p_minus_1
    primes_list = prime_range(200)  # 获取前50个左右的素数
    for prime in primes_list:
        count = 0
        while temp % prime == 0:
            temp = temp // prime
            count += 1
        if count > 0:
            small_factors.append((prime, count))
    if small_factors:
        print(f"p-1 的小素数因子: {small_factors}")
    else:
        print("p-1 没有小素数因子")
    print(f"剩余因子大小: {temp.nbits()} 位")
    # 使用 SageMath 内置的离散对数函数
    print("\n=== 使用 SageMath discrete_log 求解 ===")
    try:
        # 创建有限域
        Fp = GF(p)
        g_fp = Fp(g)
        c_fp = Fp(c)
        print("开始计算离散对数...")
        # 使用 bsgs 算法
        x = discrete_log(c_fp, g_fp, operation="*")
        print(f"找到解: x = {x}")
        print(f"x 的位数: {x.nbits()}")
        # 验证结果
        verification = power_mod(g, x, p)
        print(f"\n验证: {g}^{x} ≡ {verification} (mod p)")
        print(f"目标值: {c}")
        print(f"验证成功: {verification == c}")
        return x
    except Exception as e:
        print(f"SageMath discrete_log 失败: {e}")
        return None


def manual_bsgs(g, h, p, m=None):
    """手动实现 Baby-step Giant-step 算法"""
    if m is None:
        m = ceil(sqrt(p))
    print(f"\n=== 手动 BSGS 算法 ===")
    print(f"搜索参数 m = {m}")
    print(f"预期复杂度: O({m})")
    # Baby steps: 存储 g^j mod p, j = 0, 1, ..., m-1
    print("计算 baby steps...")
    baby_steps = {}
    gamma = 1
    for j in range(m):
        if gamma == h:
            return j
        baby_steps[gamma] = j
        gamma = (gamma * g) % p
        if j % 100000 == 0 and j > 0:
            print(f"Baby steps 进度: {j}/{m}")
    # Giant steps
    print("计算 giant steps...")
    gm = power_mod(g, m, p)
    gm_inv = inverse_mod(gm, p)
    y = h
    for i in range(m):
        if y in baby_steps:
            x = i * m + baby_steps[y]
            print(f"在 giant step {i} 找到匹配")
            return x
        y = (y * gm_inv) % p
        if i % 100000 == 0 and i > 0:
            print(f"Giant steps 进度: {i}/{m}")
    return None


def main():
    """主函数"""
    print("正在求解离散对数问题...")
    # 尝试使用 SageMath 内置方法
    x = solve_discrete_log()
    # x = manual_bsgs(g, c, p)
    if x is not None:
        print(f"\n成功找到 x = {x}")
    else:
        print("未能求解离散对数")


if __name__ == "__main__":
    main()
