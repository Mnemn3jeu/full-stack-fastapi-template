from fastapi import FastAPI, Request
import httpx

app = FastAPI()

JANITOR_API_URL = "https://integrate.api.nvidia.com/v1"  # Replace with actual

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        req_method = getattr(client, request.method.lower())
        janitor_url = f"{JANITOR_API_URL}/{path}"
        headers = dict(request.headers)
        body = await request.body()

        response = await req_method(
            janitor_url,
            headers=headers,
            content=body
        )

        return {
            "status_code": response.status_code,
            "content": response.text
        }
