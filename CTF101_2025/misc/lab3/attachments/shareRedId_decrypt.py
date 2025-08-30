import base64
from urllib.parse import urlparse, parse_qs
from typing import Dict, Union, Optional


class ShareUrlDecoder:
    """小红书分享链接解码器"""

    # URL安全Base64字符映射
    URL_SAFE_BASE64_MAP = {"-": "+", "_": "/", ".": "="}
    # 解码密钥数组
    RESHAPE_KEY = [
        2,
        6,
        2,
        0,
        3,
        5,
        4,
        9,
        6,
        7,
        5,
        2,
        9,
        8,
        0,
        6,
        6,
        3,
        9,
        7,
        4,
        5,
        6,
        9,
    ]

    def __init__(self):
        pass

    def _extract_share_id(self, share_url: str) -> Optional[str]:
        """从分享URL中提取shareRedId参数"""
        try:
            parsed_url = urlparse(share_url)
            query_params = parse_qs(parsed_url.query)
            encoded = query_params.get("shareRedId")
            if not encoded or not encoded[0]:
                return None
            return encoded[0]
        except Exception:
            return None

    def _decode_url_safe_base64(self, encoded_str: str) -> str:
        """解码URL安全的Base64字符串"""
        # 替换URL安全字符为标准Base64字符
        for url_char, std_char in self.URL_SAFE_BASE64_MAP.items():
            encoded_str = encoded_str.replace(url_char, std_char)
        # 执行Base64解码
        decoded_bytes = base64.b64decode(encoded_str)
        return decoded_bytes.decode("latin-1")

    def _convert_to_lowercase(self, char_code: int) -> int:
        """将字符码转换为小写（如果适用）"""
        return char_code + 32 if char_code > 65 else char_code

    def _apply_character_transformation(self, text: str) -> str:
        """应用字符变换算法"""
        decoded_chars = []
        for i, char in enumerate(text):
            if i < len(self.RESHAPE_KEY):
                # 减去对应位置的密钥值
                char_code = ord(char) - self.RESHAPE_KEY[i]
                # 转换为小写
                transformed_code = self._convert_to_lowercase(char_code)
                decoded_chars.append(chr(transformed_code))
            else:
                # 超出密钥长度时保持原字符
                decoded_chars.append(char)
        return "".join(decoded_chars)

    def decode(self, share_url: str) -> Union[Dict[str, Union[bool, str]], bool]:
        """
        解码分享链接
        Args:
            share_url: 包含shareRedId参数的分享链接
        Returns:
            成功时返回包含解码结果的字典，失败时返回False
        """
        # 提取编码字符串
        encoded_str = self._extract_share_id(share_url)
        if not encoded_str:
            return False
        try:
            # 执行解码流程
            base64_decoded = self._decode_url_safe_base64(encoded_str)
            final_decoded = self._apply_character_transformation(base64_decoded)
            # 确保最终结果为小写
            final_decoded = final_decoded.lower()
            return {"show_decode": True, "shareer": final_decoded}
        except Exception as e:
            print(f"解码过程中发生错误: {e}")
            return False


def submit_decode(share_url: str) -> Union[Dict[str, Union[bool, str]], bool]:
    """
    解码分享链接的便捷函数
    Args:
        share_url: 包含shareRedId参数的分享链接
    Returns:
        成功时返回包含解码结果的字典，失败时返回False
    """
    decoder = ShareUrlDecoder()
    return decoder.decode(share_url)


def main():
    url = ""
    result = submit_decode(url)
    if result:
        print(f"解码成功: {result['shareer']}")
        print(f"显示解码: {result['show_decode']}")
    else:
        print("解码失败：未找到有效的编码参数或解码过程出错")


if __name__ == "__main__":
    main()
