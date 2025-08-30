from pwn import *
import re

def solve_challenge(host='10.214.160.13', port=11002):
    # 使用pwntools创建连接
    conn = remote(host, port)

    # 连续解决10个挑战
    for i in range(10):
        expr_line = None
        while not expr_line:
            # 接收数据直到新行
            data = conn.recv().decode()
            print(data.strip())
            # 使用相同的正则表达式提取数学表达式
            match = re.search(r'([0-9+\-\s]+)=', data)
            if match:
                expr_line = match.group(1).strip()

        # 计算答案
        answer = str(eval(expr_line)) + '\n'
        print(answer)

        # 发送答案
        conn.send(answer.encode())

    # 接收最终结果
    result = conn.recv()
    print(result.decode())

    # 关闭连接
    conn.close()

if __name__ == '__main__':
    solve_challenge()