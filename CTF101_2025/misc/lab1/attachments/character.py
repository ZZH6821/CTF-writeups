def split_binary_by_7(binary_string):
    """将二进制字符串按7位分割"""
    # 移除可能的空格和换行符
    binary_string = binary_string.replace(" ", "").replace("\n", "")
    # 按7位分割
    chunks = []
    for i in range(0, len(binary_string), 7):
        chunk = binary_string[i : i + 7]
        chunks.append(chunk)
    return chunks


if __name__ == "__main__":
    # 从你的代码中获取二进制字符串
    normal = "一二人入八几力十又口土士大子小山工手文方无日月木止比毛氏水玄玉生用目石示立竹老而自至色行言赤足身酉里金隶青非面革音骨鬲"
    kangxi = "⼀⼆⼈⼊⼋⼏⼒⼗⼜⼝⼟⼠⼤⼦⼩⼭⼯⼿⽂⽅⽆⽇⽉⽊⽌⽐⽑⽒⽔⽞⽟⽣⽤⽬⽯⽰⽴⽵⽼⽽⾃⾄⾊⾏⾔⾚⾜⾝⾣⾥⾦⾪⾭⾮⾯⾰⾳⾻⿀"
    text = open("字.txt", "r").read()
    binary_string = ""
    for char in text:
        if char in kangxi:
            binary_string += "1"
        if char in normal:
            binary_string += "0"
    print(f"二进制字符串长度: {len(binary_string)}")
    print(f"二进制字符串: {binary_string}")
    chunks = split_binary_by_7(binary_string)
    print(f"\n按7位分割 (共{len(chunks)}组):")
    for i, chunk in enumerate(chunks):
        print(f"第{i+1}组: {chunk} (长度: {len(chunk)})")
    # 去除 "0000011" 并处理剩余的二进制数据
    filtered_chunks = [chunk for chunk in chunks if chunk != "0000011"]
    print(f"\n去除 '0000011' 后剩余 {len(filtered_chunks)} 组:", filtered_chunks)
    # 按8位（1字节）分割并转换为ASCII字符
    ascii_chars = []
    result_string = ""
    print(f"\n按8位分割并转换为ASCII字符:")
    for i in range(0, len(filtered_chunks)):
        byte_chunk = filtered_chunks[i]
        decimal_value = int(byte_chunk, 2) + 32
        if 32 <= decimal_value <= 126:  # 可打印ASCII字符范围
            ascii_char = chr(decimal_value)
            ascii_chars.append(ascii_char)
            result_string += ascii_char
            print(
                f"第{len(ascii_chars)}组: {byte_chunk} -> {decimal_value} -> '{ascii_char}'"
            )
        else:
            print(f"第{i//8+1}组: {byte_chunk} -> {decimal_value} -> (不可打印字符)")
    print(f"\n最终结果字符串: '{result_string}'")