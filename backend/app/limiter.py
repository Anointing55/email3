from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import HTTPException

limiter = Limiter(key_func=get_remote_address)

def rate_limit_exceeded_handler(request, exc):
    """Custom handler for rate limit exceeded"""
    raise HTTPException(
        status_code=429,
        detail="Too many requests. Please try again later."
    )
