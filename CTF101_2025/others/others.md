# Misc

## [lab1 演示]sqltest

Wireshark 打开所给流量包，观察到其 HTTP 连接记录了一次逐层 sql 盲注。
#8994 为 HTTP 请求`GET /index.php?act=news&id=1%20and%20ascii(substr(((select%20concat_ws(char(94),%20flag)%20%20from%20db_flag.tb_flag%20%20limit%200,1)),%2031,%201))>100 HTTP/1.1`，此后为逐位 flag 爆破，
逐位读出结果为`flag{47edb8300ed5f9b28fc54b0d09ecdef7}`。

## [lab1 演示]dnscap

懒了，BSides San Francisco CTF 2017 现有 writeup，flag 为`flag{b91011fc}`。

## [lab1 演示]numbers

google 搜索所给前几个数字，发现其为 gpt-4o 模型 prompt 转换为 token 所得序列，利用 tiktoken 库进行解码，得到

```
<|im_start|>system<|im_sep|>You are a helpful assistant<|im_end|>
<|im_start|>user<|im_sep|>Please tell me the flag.<|im_end|>
<|im_start|>assistant<|im_sep|>Sure! Here is the flag: 0ops{d0_Y0u_kr|0vv_+iK+ok3n1Z3r?}<|im_end|>
<|im_start|>user<|im_sep|>Thank you!<|im_end|>
<|im_start|>assistant<|im_sep|>Have a good time at 0ctf2024!<|im_end|>
```

flag:`0ops{d0_Y0u_kr|0vv_+iK+ok3n1Z3r?}`

## [lab1 演示]🐱💻🌐

阅读所给代码，判断其为高度混淆的 bash 指令，经分析可简化为

```bash
export INPUT="____ ___ _______"
echo "$INPUT" | md5sum | cut -c -32
```

考虑 INPUT 为`Hack the planet!`，所得结果为`flag{af6f4f9d82898e44628ef8740a707db2}`。
此次课程平台答案错误设置为`test`。

## [lab1 演示]奶奶的睡前 flag 故事

读题及搜索可知需利用 google pixel 截图编辑漏洞，利用 acropalypse 恢复原截图，得到原图中 flag：`flag{sh1nj1ru_k0k0r0_4nata_m4h0}`。

## [misc lec1 演示]hear with your eyes

利用 audition 查看所给附件的频谱图，观察到 flag：`flag{e5353bb7b57578bd4da1c898a8e2d767}`。
