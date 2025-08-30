from pwn import *
import re

# context.log_level = 'debug'

r = remote("10.214.160.13", 11002)

for i in range(10):
    expr = None
    while not expr:
        data = r.recv().decode()
        match = re.search(r"([0-9+\-\s]+)=", data)
        if match:
            expr = match.group(1).strip()
    answer = str(eval(expr)) + "\n"
    r.send(answer.encode())

result = r.recvall()
print(result.decode())

r.close()
