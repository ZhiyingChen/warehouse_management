from fastapi import FastAPI
from fast_api.routers import algorithm_api

app = FastAPI(title="Optimization API")
app.include_router(algorithm_api.router)

# 启动命令：
# uvicorn fast_api.main:app --reload
