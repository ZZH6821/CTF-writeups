from pwn import *

r = remote("127.0.0.1", 2655)

context.log_level = "debug"

r.recvuntil(b"decimal")
r.sendline(b"100")
r.recvuntil(b"turn")
r.sendline(b"0")
flag = r.recvuntil(b"}")
print(flag)