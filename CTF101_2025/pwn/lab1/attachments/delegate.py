from pwn import *

ADD = asm(
    """
    mov eax, edi
    add eax, esi
    ret
    """
)
SUB = asm(
    """
    mov eax, edi
    sub eax, esi
    ret
    """
)
AND = asm(
    """
    mov eax, edi
    and eax, esi
    ret
    """
)
OR = asm(
    """
    mov eax, edi
    or eax, esi
    ret
    """
)
XOR = asm(
    """
    mov eax, edi
    xor eax, esi
    ret
    """
)

r = remote("127.0.0.1", 12957)
opcodes = [ADD, SUB, AND, OR, XOR]
for i, opcode in enumerate(opcodes, start=1):
    r.recvuntil(f"Request-{i}: ".encode())
    r.send(opcode)
r.recvuntil(b"first part of flag:\n")
flag = r.recvline().decode().strip()
print(f"Flag: {flag}")
r.close()