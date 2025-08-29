# main.py

from fastapi import FastAPI
from proxy_server import router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Janitor AI NVIDIA Proxy is running"}

# Attach the proxy routes
app.include_router(router)
