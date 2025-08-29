from fastapi import FastAPI, Request
from fastapi.responses import Response
import httpx
import os

app = FastAPI()

JANITOR_API_URL = "https://integrate.api.nvidia.com/v1"
API_KEY = os.getenv("NIM_API_KEY")  # Correct environment variable name

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        method = request.method.lower()
        req_method = getattr(client, method)
        target_url = f"{JANITOR_API_URL}/{path}"
        headers = dict(request.headers)

        # Remove potentially problematic headers
        headers.pop("host", None)
        headers.pop("content-length", None)

        # Inject Authorization header
        if API_KEY:
            headers["Authorization"] = f"Bearer {API_KEY}"

        # Decide whether to include body
        if method in ["post", "put", "patch"]:
            body = await request.body()
            response = await req_method(
                target_url,
                headers=headers,
                content=body
            )
        else:
            response = await req_method(
                target_url,
                headers=headers,
                params=request.query_params
            )

        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type")
        )

@app.get("/")
async def root():
    return {"message": "Proxy server is running."}
