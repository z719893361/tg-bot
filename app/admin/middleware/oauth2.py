from fastapi import Request, HTTPException
from fnmatch import fnmatch
from admin.auth.oauth2 import get_current_user

filter_black_list = [
    '/api/**'
]

filter_while_list = [
    '/api/login'
]


async def oauth2_middleware(request: Request, call_next):
    inwhile = any(fnmatch(request.url.path, path) for path in filter_while_list)
    if inwhile:
        return await call_next(request)
    inblack = any(fnmatch(request.url.path, path) for path in filter_black_list)
    if not inblack:
        return await call_next(request)
    token = request.headers.get('Authorization')
    if token is None or token == '':
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    request.state.current_user = await get_current_user(token)
    return await call_next(request)
