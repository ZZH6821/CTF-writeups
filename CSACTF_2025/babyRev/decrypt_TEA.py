import struct


def tea_decrypt(v, key):
    """TEA解密函数"""
    v0, v1 = v[0], v[1]
    sum_val = 0xC6EF3720  # 32轮后的sum值 (32 * 0x9E3779B9)
    delta = 0x9E3779B9
    for _ in range(32):
        v1 = (
            v1 - (((v0 << 4) + key[2]) ^ (v0 + sum_val) ^ ((v0 >> 5) + key[3]))
        ) & 0xFFFFFFFF
        v0 = (
            v0 - (((v1 << 4) + key[0]) ^ (v1 + sum_val) ^ ((v1 >> 5) + key[1]))
        ) & 0xFFFFFFFF
        sum_val = (sum_val - delta) & 0xFFFFFFFF
    return [v0, v1]


def ints_to_string(ints):
    """将4个32位整数转换为16字节字符串"""
    result = b""
    for i in range(4):
        # 按小端序转换每个32位整数为4字节
        result += struct.pack("<I", ints[i])
    return result


def main():
    # 目标加密值（转换为无符号32位整数）
    target1 = [(-1131689757) & 0xFFFFFFFF, (-1872115493) & 0xFFFFFFFF]
    target2 = [120706789, (-1858409781) & 0xFFFFFFFF]
    # 密钥 "this_isnot_a_key"
    key_str = b"this_isnot_a_key"
    # 将密钥字符串转换为4个32位整数
    key = []
    for i in range(4):
        key_val = 0
        for j in range(4):
            key_val += key_str[i * 4 + j] << (j * 8)
        key.append(key_val)
    print(f"Key values: {key[0]} {key[1]} {key[2]} {key[3]}")
    # 解密第一部分
    decrypted1 = tea_decrypt(target1.copy(), key)
    # 解密第二部分
    decrypted2 = tea_decrypt(target2.copy(), key)
    # 组合结果
    result = decrypted1 + decrypted2
    print(f"Decrypted values: {result[0]} {result[1]} {result[2]} {result[3]}")
    # 转换为字符串
    password_bytes = ints_to_string(result)
    print("Password: ", end="")
    for byte in password_bytes:
        if 32 <= byte <= 126:
            print(chr(byte), end="")
        else:
            print(f"\\x{byte:02x}", end="")
    print()


if __name__ == "__main__":
    main()
