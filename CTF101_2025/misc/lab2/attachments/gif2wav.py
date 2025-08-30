import librosa
import soundfile
import numpy as np
from PIL import Image, ImageSequence
import os

# 音频参数常量
SAMPLE_RATE = 22050
NUM_FREQ_BINS = 32
QUANTIZE_FACTOR = 2
MIN_DB = -60
MAX_DB = 30
FFT_WINDOW_SIZE = 2048
FRAME_STEP_SIZE = 512
WINDOW_FUNCTION = "hann"
# 新增：内存安全限制
MAX_FRAMES = 1000  # 严格限制最大帧数
MAX_AUDIO_LENGTH_SEC = 30  # 最大音频时长（秒）


def load_gif_frames(gif_path):
    """从GIF文件加载所有帧并转换为RGB数组"""
    if not os.path.exists(gif_path):
        raise FileNotFoundError(f"GIF文件不存在: {gif_path}")
    gif_image = Image.open(gif_path)
    frames = []
    print(f"GIF信息: {gif_image.format}, 尺寸: {gif_image.size}")
    frame_count = 0
    for frame in ImageSequence.Iterator(gif_image):
        rgb_frame = frame.copy().convert("RGB")
        frame_array = np.array(rgb_frame.getdata(), dtype=np.uint8).reshape(
            rgb_frame.height, rgb_frame.width, 3
        )
        frames.append(frame_array)
        frame_count += 1
        # 更严格的帧数限制
        if frame_count >= MAX_FRAMES:
            print(f"警告: 达到最大帧数限制 {MAX_FRAMES}，停止加载")
            break
    print(f"加载了 {len(frames)} 帧")
    return np.array(frames)


def extract_mel_spectrogram_from_frames(frames):
    """从图像帧中提取梅尔频谱图数据"""
    log_mel_spec = np.zeros((len(frames), NUM_FREQ_BINS))
    print(f"开始提取频谱图，帧数: {len(frames)}, 频率bins: {NUM_FREQ_BINS}")
    for frame_idx, frame in enumerate(frames):
        if frame_idx % 100 == 0:
            print(f"处理帧 {frame_idx}/{len(frames)}")
        for freq_bin in range(NUM_FREQ_BINS):
            # 计算当前频率bin对应的列索引
            col_index = freq_bin * (QUANTIZE_FACTOR * 2) + QUANTIZE_FACTOR
            # 检查列索引是否超出范围
            if col_index >= frame.shape[1]:
                print(f"警告: 列索引 {col_index} 超出图像宽度 {frame.shape[1]}")
                continue
            # 提取红色通道值
            red_channel_values = frame[::QUANTIZE_FACTOR, col_index, 0]
            # 计算黑色像素（值为0）的数量
            black_pixel_count = np.sum(red_channel_values == 0)
            # 将像素计数转换为dB值，并限制在合理范围内
            db_value = black_pixel_count * QUANTIZE_FACTOR + MIN_DB
            db_value = np.clip(db_value, MIN_DB, MAX_DB)  # 限制范围
            log_mel_spec[frame_idx, freq_bin] = db_value
    print(f"频谱图形状: {log_mel_spec.shape}")
    print(f"dB值范围: {log_mel_spec.min():.2f} 到 {log_mel_spec.max():.2f}")
    # 转置以匹配librosa的格式 (频率 x 时间)
    return log_mel_spec.T


def convert_db_to_power(log_mel_spec):
    """将dB值转换为功率谱"""
    power_spec = librosa.db_to_power(log_mel_spec)
    print(f"功率谱形状: {power_spec.shape}")
    print(f"功率值范围: {power_spec.min():.2e} 到 {power_spec.max():.2e}")
    return power_spec


def reconstruct_audio_from_mel_safe(power_mel_spec):
    """安全的音频重构，包含多重检查"""
    print(f"开始音频重构，输入形状: {power_mel_spec.shape}")
    # 检查输入数据合理性
    if power_mel_spec.shape[1] > MAX_FRAMES:
        print(f"警告: 时间帧数过多 ({power_mel_spec.shape[1]})，截取前 {MAX_FRAMES} 帧")
        power_mel_spec = power_mel_spec[:, :MAX_FRAMES]
    # 估计输出音频长度
    estimated_length = librosa.frames_to_samples(
        power_mel_spec.shape[1], hop_length=FRAME_STEP_SIZE
    )
    estimated_duration = estimated_length / SAMPLE_RATE
    print(f"预估音频长度: {estimated_length} 样本 ({estimated_duration:.2f} 秒)")
    # 多重安全检查
    estimated_memory_gb = estimated_length * 8 / (1024**3)
    if estimated_memory_gb > 0.5:  # 降低到500MB限制
        raise MemoryError(f"预估内存使用过大: {estimated_memory_gb:.2f} GB")
    if estimated_duration > MAX_AUDIO_LENGTH_SEC:
        raise ValueError(
            f"音频时长过长: {estimated_duration:.2f} 秒，超过限制 {MAX_AUDIO_LENGTH_SEC} 秒"
        )
    # 检查功率谱数据是否异常
    if np.any(np.isinf(power_mel_spec)) or np.any(np.isnan(power_mel_spec)):
        print("警告: 检测到无效数据，进行清理")
        power_mel_spec = np.nan_to_num(power_mel_spec, nan=0.0, posinf=1.0, neginf=0.0)
    # 限制功率谱的最大值，防止极端值
    max_power = np.percentile(power_mel_spec, 99)  # 使用99%分位数作为上限
    power_mel_spec = np.clip(
        power_mel_spec, 0, max_power * 10
    )  # 允许一些超出但不要太极端
    print("尝试使用较小的参数进行重构...")
    # 使用较小的FFT窗口和步长
    small_fft = min(FFT_WINDOW_SIZE, 1024)
    small_hop = min(FRAME_STEP_SIZE, 256)
    reconstructed_audio = librosa.feature.inverse.mel_to_audio(
        power_mel_spec,
        sr=SAMPLE_RATE,
        n_fft=small_fft,
        hop_length=small_hop,
        window=WINDOW_FUNCTION,
    )
    print(f"音频重构完成，长度: {len(reconstructed_audio)} 样本")
    return reconstructed_audio


def save_audio(audio_data, output_path):
    """保存音频数据到文件"""
    # 确保音频数据在合理范围内
    if len(audio_data) == 0:
        raise ValueError("音频数据为空")
    # 归一化音频数据
    max_val = np.abs(audio_data).max()
    if max_val > 0:
        audio_data = audio_data / max_val * 0.95  # 归一化到95%避免削波
    soundfile.write(output_path, audio_data, SAMPLE_RATE)
    print(f"音频已保存到: {output_path}")
    print(f"音频时长: {len(audio_data)/SAMPLE_RATE:.2f} 秒")


def gif_to_audio(gif_path, output_audio_path):
    """完整的GIF到音频转换流程"""
    print(f"开始转换: {gif_path} -> {output_audio_path}")
    # 1. 加载GIF帧
    frames = load_gif_frames(gif_path)
    # 2. 从图像帧提取梅尔频谱图
    log_mel_spec = extract_mel_spectrogram_from_frames(frames)
    # 3. 转换dB到功率谱
    power_mel_spec = convert_db_to_power(log_mel_spec)
    # 4. 安全的音频重构
    reconstructed_audio = reconstruct_audio_from_mel_safe(power_mel_spec)
    # 5. 保存音频
    save_audio(reconstructed_audio, output_audio_path)
    print("转换完成!")


if __name__ == "__main__":
    gif_to_audio("flag-2.gif", "flag-2.wav")
