import time
import threading

class Proxy:
    def __init__(self, ip: str):
        self.ip = ip
        self.available = True
        self.last_checked = time.time()

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.lock = threading.Lock()
        self.recheck_interval = 300  # 5分钟

    def add_proxy(self, proxy: str):
        with self.lock:
            self.proxies.append(Proxy(proxy))

    def report_proxy(self, proxy: str):
        with self.lock:
            for p in self.proxies:
                if p.ip == proxy:
                    p.available = False
                    p.last_checked = time.time()
                    threading.Timer(self.recheck_interval, self.recheck_proxy, args=[p]).start()

    def recheck_proxy(self, proxy: Proxy):
        with self.lock:
            proxy.available = True

    def get_proxy(self):
        with self.lock:
            available_proxies = [p for p in self.proxies if p.available]
            if not available_proxies:
                return None
            return available_proxies[0].ip
