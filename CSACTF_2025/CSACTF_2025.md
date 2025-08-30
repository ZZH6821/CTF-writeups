# Result

- Score: 551
  - Misc: 250
  - Crypto: 201
  - Pwn: 0
  - Web: 0
  - Reverse: 100
- Total Rank: 21/30

# Misc

## ChecekIn

`Q1NBQ1RGe00xbmRzXzFudGVydHcxbmVkXyZfU2VjdXIxdHlfRDNzMWduM2R9`经 base64 解码后得到 flag`CSACTF{M1nds_1ntertw1ned_&_Secur1ty_D3s1gn3d}`。

## HidenWorld

容易发现图片高度异常，010 Editor 打开`welcome.png`，修改`IHDR`中的高为`1000`，保存后用图片查看器打开，得到 flag`Flag{W31c0m3_70_M15C}`，据 hint 修改为`CSACTF{W31c0m3_70_M15C}`。

# Crypto

## ezCrypto

根据提供的源码编写[crack_ezcrypto.py](ezCrypto/crack_ezcrypto.py)，运行得到`secret`为`R28wZF9Kb0IhX1dlMUMwbUVfdDBfb1VSX2NzQUN0Rl8ybzI1IQ==`，base64 解码后添加前缀得到 flag`CSACTF{Go0d_JoB!_We1C0mE_t0_oUR_csACtF_2o25!}`。

# Reverse

## babyRev

IDA 打开所给程序，逐步分析`main`函数；程序读入输入；`sub_12D3`函数先验证存入`src`的输入字符串长度是否为 16，之后经`sub_1241`函数转换为字符串对应的 32 位整数存入`v4`；`sub_1439`函数两次调用`sub_134E`进行 TEA 加密并与预定义的整数进行比较，通过所有验证后输出 flag 为添加前缀的输入值。
据此编写[decrypt_TEA.py](babyRev/decrypt_TEA.py)，运行结果为`Password: W0w_u_kN0w_t3A!!`，原程序验证正确，得到 flag`CSACTF{W0w_u_kN0w_t3A!!}`。
