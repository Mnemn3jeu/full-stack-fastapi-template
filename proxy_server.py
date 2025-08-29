# proxy_router.py

from fastapi import APIRouter, Request
from fastapi.responses import Response
import httpx
import os

router = APIRouter()

JANITOR_API_URL = "https://integrate.api.nvidia.com/v1"
API_KEY = os.getenv("NIM_API_KEY")

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        method = request.method.lower()
        req_method = getattr(client, method)
        target_url = f"{JANITOR_API_URL}/{path}"
        headers = dict(request.headers)

        # Clean headers
        headers.pop("host", None)
        headers.pop("content-length", None)

        # Inject API key
        if API_KEY:
            headers["Authorization"] = f"Bearer {API_KEY}"
        else:
            return Response(content="API key missing", status_code=500)

        # Handle body or query
        if method in ["post", "put", "patch"]:
            body = await request.body()
            response = await req_method(target_url, headers=headers, content=body)
        else:
            response = await req_method(target_url, headers=headers, params=request.query_params)

        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type")
        )

app = FastAPI()
