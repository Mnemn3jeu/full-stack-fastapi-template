from fastapi import APIRouter, Request
from fastapi.responses import Response
import httpx
import os

router = APIRouter()

NIM_API_BASE = "https://integrate.api.nvidia.com/v1"
API_KEY = os.getenv("NIM_API_KEY")

@router.api_route("/v1/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    if not API_KEY:
        return Response(content="Missing NVIDIA API key", status_code=500)

    target_url = f"{NIM_API_BASE}/{path}"
    headers = dict(request.headers)

    headers.pop("host", None)
    headers.pop("content-length", None)
    headers["Authorization"] = f"Bearer {API_KEY}"

    async with httpx.AsyncClient() as client:
        method = request.method.lower()
        req_method = getattr(client, method)

        try:
            if method in ["post", "put", "patch"]:
                body = await request.body()
                proxied_response = await req_method(target_url, headers=headers, content=body)
            else:
                proxied_response = await req_method(target_url, headers=headers, params=request.query_params)

            return Response(
                content=proxied_response.content,
                status_code=proxied_response.status_code,
                media_type=proxied_response.headers.get("content-type")
            )
        except Exception as e:
            return Response(content=f"Proxy error: {str(e)}", status_code=500)
