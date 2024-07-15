import os
import random
import threading
import time

class WorkManager:
    def __init__(self, work_dir: str):
        self.work_dir = work_dir
        self.cache = []
        self.success_file = "results_success.txt"
        self.failure_file = "results_failure.txt"
        self.current_file_index = 0
        self.current_line_index = 0
        self.pointer_file = "pointer.txt"
        self.load_pointer()
        threading.Thread(target=self.save_pointers_periodically, daemon=True).start()
        threading.Thread(target=self.save_pointers_periodically, daemon=True).start()
        self.files = []
        self.load_work()
        if self.files:
            self.files.sort()  # 确保文件是按顺序排列

    def load_work(self):
        files = os.listdir(self.work_dir)
        # 只加载当前文件索引指定的文件
        self.cache = []
        if not self.files:
            self.files = [file for file in files if os.path.isfile(os.path.join(self.work_dir, file))]
            self.files.sort()
        if not self.files:
            return
        file = self.files[self.current_file_index]
        with open(os.path.join(self.work_dir, file), 'r') as f:
                # 从当前行开始读取
                f_content = f.read().splitlines()
                self.cache = f_content[self.current_line_index:]



    def split_file(self, file: str, lines: list):
        chunks = [lines[i:i + 1000] for i in range(0, len(lines), 1000)]
        for i, chunk in enumerate(chunks):
            new_file = f"{file}_part_{i}"
            with open(os.path.join(self.work_dir, new_file), 'w') as f:
                f.writelines(chunk)


    def get_work(self):
        # 保存当前指针
        self.save_pointer()

        # 当前文件和行指针结束时，尝试移动到下一个文件
        if self.current_line_index >= len(self.cache) and self.current_file_index < len(self.files) - 1:
            self.current_file_index += 1
            self.current_line_index = 0
            self.load_work()

        if not self.cache:
            return None

        # 获取当前行，并将指针下移
        work = self.cache[self.current_line_index]
        self.current_line_index += 1
        return work


    def save_pointer(self):
        with open(self.pointer_file, "w") as f:
            f.write(f"{self.current_file_index},{self.current_line_index}")

    def load_pointer(self):
        if os.path.exists(self.pointer_file):
            with open(self.pointer_file, "r") as f:
                data = f.read().strip().split(",")
                if len(data) == 2:
                    self.current_file_index = int(data[0])
                    self.current_line_index = int(data[1])

    def process_work(self, item: str, success: bool):
        if success:
            with open(self.success_file, 'a') as f:
                f.write(item + '\n')
        else:
            with open(self.failure_file, 'a') as f:
                f.write(item + '\n')

    def save_pointers_periodically(self):
        while True:
            time.sleep(5)
            self.save_pointer()

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
