import os
import random

class WorkManager:
    def __init__(self, work_dir: str):
        self.work_dir = work_dir
        self.cache = []
        self.success_file = "results_success.txt"
        self.failure_file = "results_failure.txt"
        self.load_work()

    def load_work(self):
        files = os.listdir(self.work_dir)
        for file in files:
            with open(os.path.join(self.work_dir, file), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    self.cache.append(line.strip())
                # 分割文件如果超过1000行
                if len(lines) > 1000:
                    self.split_file(file, lines)

    def split_file(self, file: str, lines: list):
        os.remove(os.path.join(self.work_dir, file))
        chunks = [lines[i:i + 1000] for i in range(0, len(lines), 1000)]
        for i, chunk in enumerate(chunks):
            new_file = f"{file}_part_{i}"
            with open(os.path.join(self.work_dir, new_file), 'w') as f:
                f.writelines(chunk)

    def get_work(self):
        if not self.cache:
            self.load_work()
        if not self.cache:
            return None
        return self.cache.pop(0)

    def process_work(self, item: str, success: bool):
        if success:
            with open(self.success_file, 'a') as f:
                f.write(item + '\n')
        else:
            with open(self.failure_file, 'a') as f:
                f.write(item + '\n')

    def get_pending_work(self):
        return self.cache

    def get_successful_work(self):
        if os.path.exists(self.success_file):
            with open(self.success_file, 'r') as f:
                return f.read().splitlines()
        return []

    def get_failed_work(self):
        if os.path.exists(self.failure_file):
            with open(self.failure_file, 'r') as f:
                return f.read().splitlines()
        return []
