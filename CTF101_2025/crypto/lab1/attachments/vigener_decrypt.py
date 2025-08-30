text_list = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\t\n"
mod = len(text_list)


def mod_inv(a, m=mod):
    """使用扩展欧几里得算法计算乘法逆元"""

    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None
    return (x % m + m) % m


def break_single_key(cipher_group):
    """爆破单个密钥"""
    opt_key = 0
    max_score = -1
    for k in range(1, mod):
        k_inv = mod_inv(k)
        decrypted = []
        for c in cipher_group:
            c_idx = text_list.index(c)
            p_idx = (c_idx * k_inv) % mod
            decrypted.append(text_list[p_idx])
        decrypted_text = "".join(decrypted)
        score = 0
        for char in decrypted_text:
            if char.islower():
                score += 1
        if score > max_score:
            max_score = score
            opt_key = k
    return opt_key


def break_whole_key(ciphertext, key_length):
    """爆破整个Vigenère密钥（已知密钥长度）"""
    groups = [""] * key_length
    for i, char in enumerate(ciphertext):
        groups[i % key_length] += char
    key = []
    for group in groups:
        key.append(break_single_key(group))
    return key


def decrypt(ciphertext, key):
    """用密钥解密密文"""
    key_inv = [mod_inv(k) for k in key]
    plaintext = []
    for i, char in enumerate(ciphertext):
        c_idx = text_list.index(char)
        p_idx = (c_idx * key_inv[i % len(key)]) % mod
        plaintext.append(text_list[p_idx])
    return "".join(plaintext)


if __name__ == "__main__":
    cipher = open("cipher.txt", "r").read()
    key_length = 29
    key = break_whole_key(cipher, key_length)
    print(f"爆破得到的密钥: {key}")
    for i in key:
        print(text_list[i], end="")
    plaintext = decrypt(cipher, key)
    open("decrypted.txt", "w").write(plaintext)
    print()
    print("解密结果已保存到 decrypted.txt")
