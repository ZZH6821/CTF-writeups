from PIL import Image
from typing import List, Tuple, Dict


def load_image_data(
    image_path: str,
) -> Tuple[Image.Image, List[Tuple[int, int, int]], int, int]:
    """加载图像并提取基本信息"""
    img = Image.open(image_path)
    palette = img.palette.getdata()[1]
    width, height = img.size
    # 提取调色板颜色
    colors = []
    for i in range(256):
        r, g, b = palette[3 * i], palette[3 * i + 1], palette[3 * i + 2]
        colors.append((r, g, b))
    return img, colors, width, height


def calculate_luminance_mapping(colors: List[Tuple[int, int, int]]) -> Dict[int, int]:
    """根据亮度值计算颜色索引映射"""
    # 计算每个颜色的亮度值
    luminance_with_id = []
    for i, (r, g, b) in enumerate(colors):
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        luminance_with_id.append((luminance, i))
    # 按亮度排序，获取新的索引顺序
    sorted_indices = [x[1] for x in sorted(luminance_with_id)]
    # 创建原索引到新索引的映射
    index_mapping = {}
    for i in range(256):
        index_mapping[i] = sorted_indices.index(i)
    return index_mapping


def extract_pixel_bits(
    img: Image.Image, index_mapping: Dict[int, int], width: int, height: int
) -> List[str]:
    """提取像素的最低位作为比特序列"""
    bits = []
    for y in range(height):
        for x in range(width):
            pixel_id = img.getpixel((x, y))
            mapped_id = index_mapping[pixel_id]
            bits.append(str(mapped_id & 1))
    return bits


def find_repeating_pattern(bits: List[str]) -> str:
    """找到重复模式并返回一个周期"""
    pattern_length = 1
    bits_str = "".join(bits)
    while bits_str[pattern_length:] != bits_str[:-pattern_length]:
        pattern_length += 1
    return bits_str[:pattern_length]


def bits_to_string(bit_pattern: str) -> str:
    """将比特序列转换为字符串"""
    result = []
    for i in range(0, len(bit_pattern), 8):
        byte_bits = bit_pattern[i : i + 8]
        if len(byte_bits) == 8:  # 确保是完整的字节
            char_code = int(byte_bits, 2)
            result.append(chr(char_code))
    return "".join(result)


def main():
    """主函数"""
    image_path = "chal-2.png"
    # 加载图像数据
    img, colors, width, height = load_image_data(image_path)
    # 计算亮度映射
    index_mapping = calculate_luminance_mapping(colors)
    # 提取像素比特
    pixel_bits = extract_pixel_bits(img, index_mapping, width, height)
    # 找到重复模式
    bit_pattern = find_repeating_pattern(pixel_bits)
    # 转换为字符串并输出
    flag = bits_to_string(bit_pattern)
    print(flag)


if __name__ == "__main__":
    main()
