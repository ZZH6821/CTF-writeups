from pwn import *
import hashlib
import itertools
import string
import threading
import time
import subprocess
import math

context.log_level = "debug"


def factorize_n(n):
    """因式分解n"""
    try:
        yafu_cmd = ["/home/zzh/coding/yafu/yafu/yafu", f"factor({n})"]
        result = subprocess.run(yafu_cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("yafu output:", result.stdout[:500])
            factors = []
            for line in result.stdout.split("\n"):
                if line.strip().startswith("P") and "=" in line:
                    factor_str = line.split("=")[1].strip()
                    try:
                        factors.append(int(factor_str))
                    except:
                        pass
            if len(factors) >= 2:
                return factors[0], factors[1]
    except Exception as e:
        print(f"yafu error: {e}")
    return None, None


def common_modulus_attack(n, e1, e2, c1, c2):
    """共模攻击 - 参考share_mod.py实现"""

    def exgcd(a, b):
        """扩展欧几里得算法"""
        if b == 0:
            return a, 0
        tempx, tempy = exgcd(b, a % b)
        x = tempy
        y = tempx - a // b * tempy
        return x, y

    print(f"Performing common modulus attack...")
    print(f"e1 = {e1}, e2 = {e2}")
    gcd_val = math.gcd(e1, e2)
    print(f"gcd(e1, e2) = {gcd_val}")
    if gcd_val != 1:
        print("e1 and e2 are not coprime, standard common modulus attack won't work")
        return None
    # 计算贝祖系数
    s1, s2 = exgcd(e1, e2)
    print(f"Extended GCD result: s1 = {s1}, s2 = {s2}")
    print(f"Verification: {s1}*{e1} + {s2}*{e2} = {s1 * e1 + s2 * e2}")
    # 处理负指数
    if s1 < 0:
        s1 = -s1
        c1 = pow(c1, -1, n)
        print(f"s1 was negative, now s1 = {s1}, c1 = c1^(-1)")
    if s2 < 0:
        s2 = -s2
        c2 = pow(c2, -1, n)
        print(f"s2 was negative, now s2 = {s2}, c2 = c2^(-1)")
    # 计算结果
    result = (pow(c1, s1, n) * pow(c2, s2, n)) % n
    print(f"Computed result: {hex(result)}")
    return result


def solve_hash_challenge(r):
    """解决hash挑战"""
    data = r.recvuntil(b"Give me XXXX").decode()
    print("Received hash challenge")
    # 提取目标hash和后缀
    suffix = target = ""
    for line in data.split("\n"):
        if "sha256(" in line and ".hexdigest()" in line:
            parts = line.split("'")
            suffix = parts[1] if len(parts) >= 2 else ""
            target = line.split(" == ")[1].strip()
            break
    print(f"Target: {target}")
    print(f"Suffix: {suffix}")
    # 暴力破解
    charset = string.ascii_letters + string.digits
    found_event = threading.Event()
    result = [None]

    def brute_force_worker(thread_id, total_threads):
        count = 0
        for candidate in itertools.product(charset, repeat=4):
            if found_event.is_set():
                return
            if count % total_threads != thread_id:
                count += 1
                continue
            prefix = "".join(candidate)
            s = prefix + suffix
            if hashlib.sha256(s.encode()).hexdigest() == target:
                result[0] = prefix
                found_event.set()
                return
            count += 1

    # 启动多线程
    threads = []
    start_time = time.time()
    num_threads = 8
    for i in range(num_threads):
        t = threading.Thread(target=brute_force_worker, args=(i, num_threads))
        t.daemon = True
        threads.append(t)
        t.start()
    found_event.wait(timeout=60)
    if not result[0]:
        print("Hash not found!")
        return False
    print(f"Found: {result[0]} in {time.time() - start_time:.2f}s")
    r.sendline(result[0].encode())
    return True


def parse_rsa_params(data, level_name):
    """解析RSA参数"""
    lines = data.split("\n")
    params = {}
    for line in lines:
        if "### n =" in line and "0x" in line:
            params["n"] = int(line.split("0x")[1], 16)
        elif "### n1 =" in line and "0x" in line:
            params["n1"] = int(line.split("0x")[1], 16)
        elif "### n2 =" in line and "0x" in line:
            params["n2"] = int(line.split("0x")[1], 16)
        elif "### n3 =" in line and "0x" in line:
            params["n3"] = int(line.split("0x")[1], 16)
        elif "### e =" in line and "0x" in line:
            params["e"] = int(line.split("0x")[1], 16)
        elif "### c =" in line and "0x" in line:
            params["c"] = int(line.split("0x")[1], 16)
        elif "### c1 =" in line and "0x" in line:
            params["c1"] = int(line.split("0x")[1], 16)
        elif "### c2 =" in line and "0x" in line:
            params["c2"] = int(line.split("0x")[1], 16)
        elif "### c3 =" in line and "0x" in line:
            params["c3"] = int(line.split("0x")[1], 16)
        elif "### p =" in line and "0x" in line:
            params["p"] = int(line.split("0x")[1], 16)
        elif "### q =" in line and "0x" in line:
            params["q"] = int(line.split("0x")[1], 16)
        elif "### e1 =" in line and "0x" in line:
            params["e1"] = int(line.split("0x")[1], 16)
        elif "### e2 =" in line and "0x" in line:
            params["e2"] = int(line.split("0x")[1], 16)
    print(f"{level_name} parameters:")
    for key, value in params.items():
        if isinstance(value, int) and value > 10**10:
            print(f"{key} = {hex(value)[:50]}...")
        else:
            print(f"{key} = {value}")
    return params


def solve_level0(r):
    """解决Level 0"""
    level0_data = r.recvuntil(b"@@@ m = ").decode()
    print("Level 0 data received")
    params = parse_rsa_params(level0_data, "Level 0")
    if not all(key in params for key in ["n", "e", "c", "p", "q"]):
        print("Failed to parse all Level 0 parameters")
        return False
    # 标准RSA解密
    phi_n = (params["p"] - 1) * (params["q"] - 1)
    d = pow(params["e"], -1, phi_n)
    m = pow(params["c"], d, params["n"])
    print(f"Level 0 solved: m = {hex(m)}")
    answer = hex(m)[2:]
    print(f"Sending Level 0 answer: {answer}")
    r.sendline(answer.encode())
    return True


def solve_level1(r):
    """解决Level 1"""
    level1_data = r.recvuntil(b"@@@ m = ", timeout=10).decode()
    print("Level 1 data received")
    params = parse_rsa_params(level1_data, "Level 1")
    if not all(key in params for key in ["n", "e", "c"]):
        print("Failed to parse all Level 1 parameters")
        return False
    # 因式分解
    print(f"Factorizing n ({params['n'].bit_length()} bits)...")
    p, q = factorize_n(params["n"])
    if not (p and q):
        print("Failed to factorize n1")
        return False
    if p * q != params["n"]:
        print("Factorization verification failed!")
        return False
    print(f"Found factors: p = {p}, q = {q}")
    print("Factorization verified!")
    # RSA解密
    phi_n = (p - 1) * (q - 1)
    d = pow(params["e"], -1, phi_n)
    m = pow(params["c"], d, params["n"])
    print(f"Level 1 solved: m = {hex(m)}")
    answer = hex(m)[2:]
    print(f"Sending Level 1 answer: {answer}")
    r.sendline(answer.encode())
    return True


def solve_level2(r):
    """解决Level 2"""
    level2_data = r.recvuntil(b"@@@ m =").decode()
    print("Level 2 data received")
    params = parse_rsa_params(level2_data, "Level 2")
    if not all(key in params for key in ["n", "e1", "e2", "c1", "c2"]):
        print("Failed to parse all Level 2 parameters")
        return False
    # 共模攻击
    m = common_modulus_attack(
        params["n"], params["e1"], params["e2"], params["c1"], params["c2"]
    )
    if m is None:
        print("Failed to solve Level 2")
        return False
    print(f"Level 2 solved: m = {hex(m)}")
    answer = hex(m)[2:]
    print(f"Sending Level 2 answer: {answer}")
    r.sendline(answer.encode())
    return True


def wiener_attack(n, e):
    """Wiener攻击 - 参考wiener_attack.py实现"""
    try:
        from gmpy2 import isqrt

        print("Attempting Wiener attack...")

        def ContinuousFraction(x, y):
            """计算连分数"""
            res = []
            while y != 0:
                res.append(x // y)
                x, y = y, x % y
            return res

        def evaluate_fraction(List):
            """计算连分数的值"""
            List.reverse()
            denominator = 0
            numerator = 1
            for i in List:
                denominator, numerator = numerator, i * numerator + denominator
            return denominator, numerator

        def Enumerate(x, y):
            """枚举连分数的收敛子"""
            CF = ContinuousFraction(x, y)
            denominators = []
            numerators = []
            for i in range(len(CF)):
                denominator, numerator = evaluate_fraction(CF)
                CF.reverse()
                denominators.append(denominator)
                numerators.append(numerator)
                CF = CF[:-1]
            return denominators, numerators

        def solve(a, b, c):
            """求解二次方程"""
            delta = b * b - 4 * a * c
            if delta < 0:
                return (0, 0)
            delta = isqrt(delta)
            if (-b + delta) % (2 * a) != 0 and (-b - delta) % (2 * a) != 0:
                return (0, 0)
            return ((-b + delta) // (2 * a), (-b - delta) // (2 * a))

        # Wiener攻击主逻辑
        el, nl = Enumerate(n, e)
        print(f"Testing {len(el)} convergents...")
        for i in range(len(el)):
            if el[i] == 0:
                continue
            if (nl[i] * e - 1) % el[i] != 0:
                continue
            phi = (e * nl[i] - 1) // el[i]
            p, q = solve(1, phi - n - 1, n)
            if p * q == n and p > 0 and q > 0:
                print(f"Found factors using convergent {i}!")
                print(f"p = {p}")
                print(f"q = {q}")
                return nl[i]  # 返回d值
        print("Wiener attack failed")
        return None
    except Exception as e:
        print(f"Error in Wiener attack: {e}")
        return None


def solve_level3(r):
    """解决Level 3 - Wiener攻击"""
    level3_data = r.recvuntil(b"@@@ m =").decode()
    print("Level 3 data received")
    params = parse_rsa_params(level3_data, "Level 3")
    if not all(key in params for key in ["n", "e", "c"]):
        print("Failed to parse all Level 3 parameters")
        return False
    print(
        f"Level 3: n has {params['n'].bit_length()} bits, e has {params['e'].bit_length()} bits"
    )
    print("This looks like a Wiener attack scenario...")
    # 尝试Wiener攻击
    d = wiener_attack(params["n"], params["e"])
    if d is None:
        print("Wiener attack failed, trying factorization...")
        # 如果Wiener攻击失败，尝试因式分解
        p, q = factorize_n(params["n"])
        if p and q:
            print(f"Found factors: p = {p}, q = {q}")
            phi_n = (p - 1) * (q - 1)
            d = pow(params["e"], -1, phi_n)
        else:
            print("All Level 3 methods failed")
            return False
    # RSA解密
    m = pow(params["c"], d, params["n"])
    print(f"Level 3 solved: m = {hex(m)}")
    answer = hex(m)[2:]
    print(f"Sending Level 3 answer: {answer}")
    r.sendline(answer.encode())
    return True


def broadcast_attack(n_list, c_list, e):
    """广播攻击 - 参考broadcast.py实现"""
    try:
        from gmpy2 import invert, iroot

        print("Attempting broadcast attack...")
        print(f"e = {e}, number of ciphertexts = {len(c_list)}")

        def CRT(a, b):
            """中国剩余定理"""
            pro = 1
            res = 0
            for i in b:
                pro *= i
            for i in range(len(b)):
                r = pro // b[i]
                res += a[i] * r * invert(r, b[i])
            return res % pro, pro

        # 使用中国剩余定理合并密文
        c, n = CRT(c_list, n_list)
        print(f"Combined using CRT, searching for k...")
        # 搜索正确的k值
        for k in range(10000000):
            if k % 1000000 == 0 and k > 0:
                print(f"Trying k = {k}...")
            tmp = c + k * n
            result = iroot(tmp, e)
            if result[1]:  # 如果是完全e次方
                m = result[0]
                print(f"Found solution at k = {k}")
                print(f"m = {hex(m)}")
                # 验证结果
                verification_passed = True
                for i in range(len(n_list)):
                    if pow(m, e, n_list[i]) != c_list[i]:
                        verification_passed = False
                        break
                if verification_passed:
                    print("Verification successful!")
                    return m
                else:
                    print("Verification failed, continuing search...")
        print("Broadcast attack failed - no solution found")
        return None
    except Exception as e:
        print(f"Error in broadcast attack: {e}")
        return None


def solve_level4(r):
    """解决Level 4 - 广播攻击"""
    try:
        level4_data = r.recvuntil(b"@@@ m =", timeout=30).decode()  # 增加超时时间
        print("Level 4 data received")
        # 添加调试：显示接收到的数据长度
        print(f"Received data length: {len(level4_data)} characters")
        params = parse_rsa_params(level4_data, "Level 4")
        required_keys = ["n1", "n2", "n3", "e", "c1", "c2", "c3"]
        if not all(key in params for key in required_keys):
            print("Failed to parse all Level 4 parameters")
            missing = [key for key in required_keys if key not in params]
            print(f"Missing keys: {missing}")
            # 调试：显示原始数据，检查参数是否存在
            print("Raw data for debugging:")
            lines = level4_data.split("\n")
            for i, line in enumerate(lines):
                if any(
                    keyword in line
                    for keyword in ["n1", "n2", "n3", "c1", "c2", "c3", "e"]
                ):
                    print(f"Line {i}: {line}")
            return False
        print(f"Level 4: e = {params['e']}, using 3 different moduli")
        print("This looks like a broadcast attack scenario...")
        # 验证参数完整性
        print(f"Parsed parameters:")
        print(f"e = {params['e']}")
        print(f"n1 bit length: {params['n1'].bit_length()}")
        print(f"n2 bit length: {params['n2'].bit_length()}")
        print(f"n3 bit length: {params['n3'].bit_length()}")
        # 准备数据
        n_list = [params["n1"], params["n2"], params["n3"]]
        c_list = [params["c1"], params["c2"], params["c3"]]
        e = params["e"]
        # 验证e是小指数（通常广播攻击需要小指数）
        if e > 10:
            print(
                f"Warning: e = {e} is not a small exponent, broadcast attack may fail"
            )
        # 进行广播攻击
        print("Starting broadcast attack computation...")
        m = broadcast_attack(n_list, c_list, e)
        if m is None:
            print("Failed to solve Level 4")
            return False
        print(f"Level 4 solved: m = {hex(m)}")
        answer = hex(m)[2:]
        print(f"Sending Level 4 answer: {answer}")
        r.sendline(answer.encode())
        # 等待服务器响应，确认答案被接收
        try:
            response = r.recv(timeout=5)
            print(f"Server response after Level 4: {response}")
        except:
            print("No immediate response from server, continuing...")
        return True
    except Exception as e:
        print(f"Error in solve_level4: {e}")
        import traceback

        traceback.print_exc()
        return False


def handle_remaining_data(r):
    """处理剩余数据并保持连接"""
    try:
        # 接收并显示所有剩余数据
        all_data = ""
        while True:
            try:
                data = r.recvall().decode()
                if not data:
                    break
                print("Received data:", data)
                all_data += data
                # 检查是否有下一关卡
                if "Level" in data and "@@@ m =" in data:
                    print("Found next level!")
                    break
            except:
                break
        # 进入交互模式
        print("Entering interactive mode...")
        r.interactive()
    except Exception as e:
        print(f"Error handling remaining data: {e}")


def main():
    """主函数"""
    r = remote("10.214.160.13", 12501)
    r.timeout = 60  # 增加全局超时时间
    try:
        print("Starting connection...")
        # 解决hash挑战
        print("Solving hash challenge...")
        if not solve_hash_challenge(r):
            print("Hash challenge failed")
            return
        # 解决Level 0
        print("Solving Level 0...")
        if not solve_level0(r):
            print("Level 0 failed")
            return
        # 解决Level 1
        print("Solving Level 1...")
        if not solve_level1(r):
            print("Level 1 failed")
            return
        # 解决Level 2
        print("Solving Level 2...")
        if not solve_level2(r):
            print("Level 2 failed")
            return
        # 解决Level 3
        print("Solving Level 3...")
        if not solve_level3(r):
            print("Level 3 failed")
            return
        # 解决Level 4
        print("Solving Level 4...")
        if not solve_level4(r):
            print("Level 4 failed")
            return
        # 处理剩余数据
        handle_remaining_data(r)
    except EOFError:
        print("Connection closed by server")
    except Exception as e:
        print(f"Error in main: {e}")
        import traceback

        traceback.print_exc()
    finally:
        if r.connected():
            print("Connection still active")
        else:
            print("Connection closed")
        try:
            r.close()
        except:
            pass


if __name__ == "__main__":
    main()
