import gmpy2
from Crypto.Util.number import long_to_bytes
from itertools import combinations


def low_exponent_attack(c, n, e=3):
    """低指数攻击：当e较小且m^e < n时，可以直接开立方根"""
    # 尝试直接开立方根
    m, is_exact = gmpy2.iroot(c, e)
    if pow(m, e, n) == c:
        return int(m)
    # 如果直接开根不行，尝试加上n的倍数
    for k in range(1, 1000):
        m_candidate, _ = gmpy2.iroot(c + k * n, e)
        if pow(m_candidate, e, n) == c:
            return int(m_candidate)
    return None


def hastad_attack(cipher_pairs, e=3):
    """Håstad广播攻击：当同一消息用不同的n但相同的e加密时"""
    if len(cipher_pairs) < e:
        return None
    # 取前e个密文进行攻击
    moduli = [pair[1] for pair in cipher_pairs[:e]]
    ciphers = [pair[0] for pair in cipher_pairs[:e]]
    # 检查模数是否互质
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            gcd_val = gmpy2.gcd(moduli[i], moduli[j])
            if gcd_val != 1:
                print(f"警告：模数 {i} 和 {j} 不互质，gcd = {gcd_val}")
                return None
    # 使用中国剩余定理
    try:
        # 计算N = n1 * n2 * ... * ne
        N = 1
        for n in moduli:
            N *= n
        # 计算Mi和yi
        x = 0
        for i in range(e):
            Mi = N // moduli[i]
            yi = gmpy2.invert(Mi, moduli[i])
            x = (x + ciphers[i] * Mi * yi) % N
        # 开e次方根
        m, is_exact = gmpy2.iroot(x, e)
        m = int(m)
        # 修复：如果不是精确根，尝试m和m+1
        candidates = [m, m + 1] if not is_exact else [m]
        for candidate in candidates:
            # 验证结果
            valid = True
            for i in range(e):
                if pow(candidate, e, moduli[i]) != ciphers[i]:
                    valid = False
                    break
            if valid:
                return candidate
        return None
    except Exception as ex:
        print(f"Håstad攻击失败: {ex}")
        return None


# 从文件读取数据
data = []
with open("/home/zzh/coding/python/a.txt", "r") as f:
    content = f.read()
# 解析数据
lines = content.strip().split("\n")
current_data = {}
for line in lines:
    line = line.strip()
    if line.startswith("n = "):
        if current_data:
            data.append(current_data)
        current_data = {"n": int(line[4:])}
    elif line.startswith("e = "):
        current_data["e"] = int(line[4:])
    elif line.startswith("c = "):
        current_data["c"] = int(line[4:])
if current_data:
    data.append(current_data)
print(f"找到 {len(data)} 组加密数据")
# 验证所有数据都有相同的e值
e_values = set(item["e"] for item in data)
if len(e_values) != 1:
    print(f"警告：发现不同的e值: {e_values}")
    exit(1)
else:
    e = list(e_values)[0]
    print(f"所有数据使用相同的e值: {e}")
messages = []
# 方法1: 对每条信息尝试低指数攻击
print("\n=== 对每条信息尝试低指数攻击 ===")
for i, item in enumerate(data):
    print(f"\n处理消息 {i+1}...")
    n, e_val, c = item["n"], item["e"], item["c"]
    m = low_exponent_attack(c, n, e_val)
    if m:
        try:
            message = long_to_bytes(m)
            messages.append((i + 1, message, "低指数攻击"))
            print(f"✅ 消息 {i+1} 低指数攻击成功: {message}")
        except Exception as ex:
            print(f"⚠️ 消息 {i+1} 低指数攻击成功但转换为字节失败: {ex}")
            print(f"原始数字: {m}")
            messages.append((i + 1, f"数字: {m}", "低指数攻击"))
    else:
        print(f"❌ 消息 {i+1} 低指数攻击失败")
# 方法2: 对每条信息尝试广播攻击（与其他所有信息组合）
print(f"\n=== 对每条信息尝试广播攻击 ===")
for target_idx in range(len(data)):
    print(f"\n以消息 {target_idx+1} 为目标进行广播攻击...")
    # 尝试与其他消息的所有可能组合
    other_indices = [i for i in range(len(data)) if i != target_idx]
    # 尝试所有包含目标消息的3元组合
    for combo_size in range(3, min(len(data) + 1, 6)):  # 限制组合大小避免过度计算
        print(f"  尝试 {combo_size} 元组合...")
        success = False
        for combo in combinations(other_indices, combo_size - 1):
            full_combo = [target_idx] + list(combo)
            cipher_pairs = [(data[i]["c"], data[i]["n"]) for i in full_combo]
            m = hastad_attack(cipher_pairs, e=e)
            if m:
                try:
                    message = long_to_bytes(m)
                    # 检查是否已经找到过这条消息
                    found = False
                    for existing in messages:
                        if existing[1] == message:
                            found = True
                            break
                    if not found:
                        messages.append(
                            (target_idx + 1, message, f"广播攻击({combo_size}元组合)")
                        )
                        print(f"✅ 消息 {target_idx+1} 广播攻击成功: {message}")
                        print(f"   使用组合: {[i+1 for i in full_combo]}")
                    success = True
                    break
                except Exception as ex:
                    print(f"⚠️ 消息 {target_idx+1} 广播攻击成功但转换失败: {ex}")
                    print(f"   原始数字: {m}")
                    messages.append(
                        (target_idx + 1, f"数字: {m}", f"广播攻击({combo_size}元组合)")
                    )
                    success = True
                    break
        if success:
            break
    if not success:
        print(f"❌ 消息 {target_idx+1} 所有广播攻击都失败")
# 方法3: 尝试所有可能的组合（不针对特定消息）
print(f"\n=== 尝试所有可能的广播攻击组合 ===")
print("尝试所有可能的3元组合...")
for combo in combinations(range(len(data)), 3):
    cipher_pairs = [(data[i]["c"], data[i]["n"]) for i in combo]
    m = hastad_attack(cipher_pairs, e=e)
    if m:
        try:
            message = long_to_bytes(m)
            # 检查是否已经找到过这条消息
            found = False
            for existing in messages:
                if existing[1] == message:
                    found = True
                    break
            if not found:
                messages.append((f"组合{combo}", message, "广播攻击(3元组合)"))
                print(f"✅ 组合 {[i+1 for i in combo]} 广播攻击成功: {message}")
        except Exception as ex:
            print(f"⚠️ 组合 {combo} 广播攻击成功但转换失败: {ex}")
            print(f"原始数字: {m}")
# 输出所有成功恢复的消息
print(f"\n=== 总结 ===")
print(f"总共恢复了 {len(messages)} 条消息:")
for i, (msg_id, msg, method) in enumerate(messages):
    print(f"{i+1}. 消息 {msg_id} ({method}): {msg}")
if len(messages) == 0:
    print("所有攻击方法都失败了。可能的原因：")
    print("1. 消息不相同")
    print("2. 某些模数不互质")
    print("3. 消息太大，不适用于低指数攻击")
# 提取唯一的消息内容
unique_messages = []
for _, msg, _ in messages:
    if msg not in [um[1] for um in unique_messages]:
        unique_messages.append((msg, [method for _, m, method in messages if m == msg]))
print(f"\n=== 唯一消息内容 ===")
for i, (msg, methods) in enumerate(unique_messages):
    print(f"{i+1}. {msg}")
    print(f"=找到方法: {', '.join(set(methods))}")
