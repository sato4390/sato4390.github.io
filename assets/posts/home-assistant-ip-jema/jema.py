import os
import requests
from requests.auth import HTTPDigestAuth
from urllib.parse import urljoin

base_url = os.getenv("JEMA_BASE_URL")
username = "admin"
password = os.getenv("JEMA_PASSWORD")

def request(path):
    return requests.get(
        urljoin(base_url, path),
        auth=HTTPDigestAuth(username, password),
        timeout=10,
    )

if __name__ == '__main__':
    # 現在の状態を取得
    print("<body bgcolor=#ffffff>ON</body>" in request('/cgi-bin/jemaStat').text)

    # 開錠
    request('/cgi-bin/jemaStat?Jema=OFF')

    # 施錠
    request('/cgi-bin/jemaStat?Jema=ON')

