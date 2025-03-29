import socket
import numpy as np

def convert_switch_array_to_lights_array(switch_array: np.array) -> np.array:
    lights_array = np.zeros_like(switch_array)
    lights_array ^= switch_array
    lights_array[:-1, :, :] ^= switch_array[1:, :, :]
    lights_array[1:, :, :] ^= switch_array[:-1, :, :]
    lights_array[:, :-1, :] ^= switch_array[:, 1:, :]
    lights_array[:, 1:, :] ^= switch_array[:, :-1, :]
    lights_array[:, :, :-1] ^= switch_array[:, :, 1:]
    lights_array[:, :, 1:] ^= switch_array[:, :, :-1]
    return lights_array

def solve_lights_out(lights_array: np.array) -> str:
    n = lights_array.shape[0]
    size = n**3
    A = np.zeros((size, size), dtype=int)
    b = lights_array.flatten()

    def index(x, y, z):
        return x * n * n + y * n + z

    for x in range(n):
        for y in range(n):
            for z in range(n):
                idx = index(x, y, z)
                A[idx, idx] = 1
                if x > 0:
                    A[idx, index(x-1, y, z)] ^= 1
                if x < n-1:
                    A[idx, index(x+1, y, z)] ^= 1
                if y > 0:
                    A[idx, index(x, y-1, z)] ^= 1
                if y < n-1:
                    A[idx, index(x, y+1, z)] ^= 1
                if z > 0:
                    A[idx, index(x, y, z-1)] ^= 1
                if z < n-1:
                    A[idx, index(x, y, z+1)] ^= 1

    A = A % 2
    b = b % 2

    for i in range(size):
        if A[i, i] == 0:
            for j in range(i+1, size):
                if A[j, i] == 1:
                    A[[i, j]] = A[[j, i]]
                    b[i], b[j] = b[j], b[i]
                    break
        if A[i, i] == 0:
            continue
        for j in range(i+1, size):
            if A[j, i] == 1:
                A[j] ^= A[i]
                b[j] ^= b[i]

    x = np.zeros(size, dtype=int)
    for i in range(size-1, -1, -1):
        if A[i, i] == 0:
            if b[i] == 1:
                raise ValueError("No solution exists")
            continue
        x[i] = b[i]
        for j in range(i+1, size):
            x[i] ^= A[i, j] & x[j]

    binary_string = ''.join(map(str, x))
    return binary_string


def main():
    host = '202.38.93.141'  # 替换为实际的主机名或IP地址
    port = 10098  # 替换为实际的端口号

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # 接收欢迎消息
        print(s.recv(1024).decode())

        # 输入 token
        token = "<token>"
        s.sendall(f"{token}\n".encode())

        for difficulty in [3]:
            # 接收并忽略 "Enter difficulty level (1~4):"
            while True:
                data = s.recv(1024).decode()
                if "Enter difficulty level (1~4):" in data:
                    break

            # 发送难度级别
            difficulty = 3
            s.sendall(f"{difficulty}\n".encode())

            # 接收灯光字符串，直到找到 "Enter your answer:"
            lights_string = ""
            while True:
                data = s.recv(1024).decode()
                if "Enter your answer:" in data:
                    lights_string += data.split("Enter your answer:")[0]
                    break
                lights_string += data

            lights_string = lights_string.strip()
            print(f"Received lights string: {lights_string}\n")

            # 过滤掉非数字字符
            filtered_lights_string = ''.join(filter(str.isdigit, lights_string))

            # 将灯光字符串转换为灯光数组
            n = 3 if difficulty == 1 else 5 if difficulty == 2 else 11
            lights_array = np.array(list(map(int, filtered_lights_string)), dtype=np.uint8).reshape(n, n, n)

            # 解决灯光问题
            answer_string = solve_lights_out(lights_array)
            print(f"Answer string: {answer_string}\n")

            # 发送答案
            s.sendall(f"{answer_string}\n".encode())

            # 接收并打印 flag
            flag = s.recv(1024).decode().strip()
            print(f"Flag for difficulty {difficulty}: {flag}")

if __name__ == "__main__":
    main()
