# main.py

from fastapi import FastAPI
from proxy_router import router

app = FastAPI()

# Root route for health check
@app.get("/")
async def root():
    return {"message": "Proxy server is running."}

# Include the proxy router
app.include_router(router)
