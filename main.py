from fastapi.staticfiles import StaticFiles
import uvicorn
from proxy_manager import ProxyManager
from work_manager import WorkManager
import os
import time

app = FastAPI()

# 初始化IP池管理和工作管理
proxy_manager = ProxyManager()
work_manager = WorkManager(work_dir="work")

@app.post("/report_proxy")
async def report_proxy(proxy: str):
    proxy_manager.report_proxy(proxy)
    return {"status": "success"}

@app.get("/get_proxy")
async def get_proxy():
    proxy = proxy_manager.get_proxy()
    return {"proxy": proxy}

@app.get("/get_work")
async def get_work():
    work = work_manager.get_work()
    return {"work": work}

@app.post("/process_work")
async def process_work(item: str, success: bool):
    work_manager.process_work(item, success)
    return {"status": "success"}

@app.get("/pending_work")
async def pending_work():
    pending = work_manager.get_pending_work()
    return {"pending_work": pending}

@app.get("/successful_work")
async def successful_work():
    successful = work_manager.get_successful_work()
    return {"successful_work": successful}

@app.get("/failed_work")
async def failed_work():
    failed = work_manager.get_failed_work()
    return {"failed_work": failed}

app.mount("/", StaticFiles(directory="crawler-frontend/build", html=True), name="frontend")

if __name__ == "__main__":
    # 创建工作目录
    if not os.path.exists("work"):
        os.makedirs("work")
    
    # 启动FastAPI应用
    uvicorn.run(app, host="0.0.0.0", port=8000)
