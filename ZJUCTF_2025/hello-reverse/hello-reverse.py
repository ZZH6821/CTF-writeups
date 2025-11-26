import struct


def solve():
    # 从反编译代码中提取的硬编码数值
    v18 = 1129663066
    v19 = 0x6F6C6C65487B4654
    v20 = 0x525F732774654C5F
    v21 = 0x325F657372657665
    v22 = 0x7D898E9FF0353230
    flag_bytes = (
        struct.pack("<I", v18)
        + struct.pack("<Q", v19)
        + struct.pack("<Q", v20)
        + struct.pack("<Q", v21)
        + struct.pack("<Q", v22)
    )

    try:
        print(f"Flag: {flag_bytes.decode('utf-8')}")
    except UnicodeDecodeError:
        print(f"Raw bytes: {flag_bytes}")


if __name__ == "__main__":
    solve()
