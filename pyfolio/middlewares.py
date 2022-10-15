from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

allow_origins = [
    "http://127.0.0.1:4200",
    "http://localhost:4200",
]

trusted_hosts = [
    'example.com',
    '*.example.com',
    '127.0.0.1',
    'localhost',
]


ROUTES_MIDDLEWARE = [
    Middleware(GZipMiddleware, minimum_size=1000),
    Middleware(CORSMiddleware, allow_origins=allow_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],),
    Middleware(TrustedHostMiddleware, allowed_hosts=trusted_hosts),
]
