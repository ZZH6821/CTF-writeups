import numpy as np
from typing import Tuple


class PowerAnalysisAttack:
    """侧信道功耗分析攻击类"""

    def __init__(self, data_file: str):
        """初始化攻击类
        Args:
            data_file: NPZ数据文件路径
        """
        self.charset = "abcdefghijklmnopqrstuvwxyz0123456789_{}"
        self.charset_size = len(self.charset)
        self.password_length = 27
        self.time_samples = 100
        # 加载功耗数据
        npz_data = np.load(data_file)
        self.power_traces = npz_data["power"]  # shape: (1053, 100)

    def find_statistical_outlier(self, values: list) -> Tuple[int, float]:
        """找到数组中偏离均值最远的元素
        Args:
            values: 数值列表
        Returns:
            tuple: (异常值索引, 最大偏离距离)
        """
        mean_value = np.mean(values)
        deviations = np.abs(np.array(values) - mean_value)
        outlier_index = np.argmax(deviations)
        max_deviation = deviations[outlier_index]
        return outlier_index, max_deviation

    def extract_position_traces(self, position: int, time_point: int) -> list:
        """提取指定位置和时间点的功耗数据
        Args:
            position: 密码位置 (0-26)
            time_point: 时间采样点 (0-99)
        Returns:
            list: 该位置所有字符在指定时间点的功耗值
        """
        start_idx = position * self.charset_size
        end_idx = (position + 1) * self.charset_size
        return [self.power_traces[i][time_point] for i in range(start_idx, end_idx)]

    def analyze_position(self, position: int) -> str:
        """分析指定位置的密码字符
        Args:
            position: 密码位置
        Returns:
            str: 推测的密码字符
        """
        max_deviation = -1
        best_char_index = 0
        best_time_point = 0
        # 遍历所有时间点，寻找最佳判别时机
        for time_point in range(self.time_samples):
            power_values = self.extract_position_traces(position, time_point)
            char_index, deviation = self.find_statistical_outlier(power_values)
            if deviation > max_deviation:
                max_deviation = deviation
                best_char_index = char_index
                best_time_point = time_point
        return self.charset[best_char_index]

    def recover_password(self) -> str:
        """恢复完整密码
        Returns:
            str: 恢复的密码字符串
        """
        password_chars = []
        print("开始密码恢复分析...")
        for position in range(self.password_length):
            recovered_char = self.analyze_position(position)
            password_chars.append(recovered_char)
            print(f"位置 {position:2d}: {recovered_char}")
        recovered_password = "".join(password_chars)
        return recovered_password


def main():
    """主函数"""
    # 创建攻击实例并执行密码恢复
    attack = PowerAnalysisAttack("data.npz")
    password = attack.recover_password()
    print(password)


if __name__ == "__main__":
    main()
