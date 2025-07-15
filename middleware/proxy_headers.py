from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class ProxyHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        x_forwarded_for = request.headers.get("x-forwarded-for")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
            request.scope["client"] = (ip, 0)

        x_proto = request.headers.get("x-forwarded-proto")
        if x_proto:
            request.scope["scheme"] = x_proto.strip()

        return await call_next(request)