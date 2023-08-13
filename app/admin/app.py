from pathlib import Path
from fastapi import FastAPI
from starlette.middleware.exceptions import ExceptionMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from admin.events import startup, shutdown
from admin.middleware.oauth2 import oauth2_middleware
from admin.routers import channel, config, recharge, robot, login

app = FastAPI(docs_url=None)

# 注册中间件
app.middleware('http')(oauth2_middleware)
app.add_middleware(ExceptionMiddleware)

# 注册路由
app.include_router(channel.router, prefix='/api')
app.include_router(config.router, prefix='/api')
app.include_router(recharge.router, prefix='/api')
app.include_router(robot.router, prefix='/api')
app.include_router(login.router, prefix='/api')

# 事件
app.add_event_handler('startup', startup.create_tables)
app.add_event_handler('startup', startup.robot_startup)
app.add_event_handler('shutdown', shutdown.robot_shutdown)

# 添加静态文件
app.mount('/', StaticFiles(directory=Path(__file__).parent / 'view'), name='static')


@app.get('/')
async def index():
    return RedirectResponse(url='/index.html')
