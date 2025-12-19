# Tool Đào Proxy By Phan Trọng Phúc

import requests
import os
from colorama import Fore, init

init(autoreset=True)

PROXY_SOURCES = {
    'VN': [
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=VN',
        'https://www.proxy-list.download/api/v1/get?type=http&country=VN'
    ],
    'SG': [
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=SG',
        'https://www.proxy-list.download/api/v1/get?type=http&country=SG'
    ],
    'GER': [
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=DE',
        'https://www.proxy-list.download/api/v1/get?type=http&country=DE'
    ],
    'RU': [
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=RU',
        'https://www.proxy-list.download/api/v1/get?type=http&country=RU'
    ],
    'JP': [
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=JP',
        'https://www.proxy-list.download/api/v1/get?type=http&country=JP'
    ]
}

def fetch_proxies(country_code):
    proxies = []
    for url in PROXY_SOURCES[country_code]:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                new_proxies = response.text.splitlines()
                proxies.extend(new_proxies)
        except Exception as e:
            print(Fore.RED + f"Lỗi lấy proxy từ {url}: {e}")
    return list(set(proxies))

def check_proxy(proxy):
    try:
        response = requests.get(
            "http://httpbin.org/ip",
            proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
            timeout=5
        )
        if response.status_code == 200:
            print(Fore.GREEN + f"[LIVE] {proxy}")
            return proxy
    except:
        print(Fore.RED + f"[DEAD] {proxy}")
    return None

def main():
    os.system("clear")
    print("\033[91mTool Đào Proxy By Phan Trọng Phúc\033[0m")
    print("Chọn quốc gia để lấy proxy:")
    print("1. Việt Nam (VN)")
    print("2. Singapore (SG)")
    print("3. Đức (GER)")
    print("4. Nga (RU)")
    print("5. Nhật Bản (JP)")
    
    choice = input("Nhập lựa chọn (1–5): ").strip()
    country_map = {"1": "VN", "2": "SG", "3": "GER", "4": "RU", "5": "JP"}

    if choice not in country_map:
        print(Fore.RED + "Lựa chọn không hợp lệ!")
        return

    country_code = country_map[choice]
    print(f"\nĐang lấy proxy từ {country_code}...")
    proxies = fetch_proxies(country_code)

    if not proxies:
        print(Fore.RED + "Không lấy được proxy nào!")
        return

    # Giới hạn tối đa 100 proxy
    proxies = proxies[:100]
    print(f"Đã lấy được {len(proxies)} proxy (giới hạn 100). Đang kiểm tra...\n")

    live_proxies = []
    for proxy in proxies:
        result = check_proxy(proxy)
        if result:
            live_proxies.append(result)

    print(Fore.CYAN + f"\nTổng cộng {len(live_proxies)} proxy sống!")
    if live_proxies:
        with open("live_proxies.txt", "w") as f:
            f.write("\n".join(live_proxies))
        print(Fore.YELLOW + "Proxy sống đã lưu vào live_proxies.txt")

if __name__ == "__main__":
    main()