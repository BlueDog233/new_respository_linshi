import random
import time
import threading
import multiprocessing

import requests
from DrissionPage._pages.chromium_page import ChromiumPage

from multiprocessing import Lock

lock = Lock()



class Proxy:
    def __init__(self, ip: str,id:int):
        self.ip = ip
        self.available = True
        self.last_checked = time.time()
        self.id=id
        self.risk_value=0
def recheck_proxy( proxy):
    """
    更改代理IP
    :param proxy:
    :return:
    """
    with lock:
        page = ChromiumPage()
        page.get('https://www.hailiangip.com/')
        try:
            page.ele('@@class=new-before-close@@onClick=closeIpStaticCoupons()').click()
        except Exception as e:
            pass
        try:
            page.wait(2)
            page.ele('@text()=退出').click()
        except Exception as e:
            pass
        try:
            page.wait(2)

            page.ele('@text()=登录').click()
            page.wait(2)
            page.ele('@name=username-mobile').input('18180034455')
            page.ele('@name=password').input('bluedog233')
            page.wait(2)
            page.ele('@class=btn btn-primary login-button').click()
            page.wait(5)
        except Exception as e:
            pass
        page.listen.start('https://www.hailiangip.com/get/ladder/coupons')

        page.get('https://www.hailiangip.com/')

        i = 0
        for packet in page.listen.steps():
            i = i + 1
            cookie = packet.request.extra_info.headers.get('cookie')
            req = requests.post(
                url='https://www.hailiangip.com/update/new/lineConfig',
                headers={
                    'Cookie': cookie},
                params={'id': proxy.id, 'pid': -1, 'cid': -1}
            )
            print(req.content)
            page.wait(60)
            page.quit()
            if (i == 1):
                break
        proxy.available = True
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.lock = threading.Lock()
        self.recheck_interval = 300  # 5分钟

    def add_proxy(self, proxy: str,id:int):
        with self.lock:
            self.proxies.append(Proxy(proxy,id))

    def report_proxy(self, proxy: str):
        for p in self.proxies:
            if p.ip == proxy:
                p.available = False
                p.last_checked = time.time()
                multiprocessing.Process(target=recheck_proxy, args=(p,)).start()



    def get_proxy(self):
        with self.lock:
            available_proxies = [p for p in self.proxies if p.available]
            if not available_proxies:
                return None
            return random.choice(available_proxies).ip
proxy_manager = ProxyManager()