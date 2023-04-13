from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import socketio

from app.socket.socket_handler import sio
from app.socket.event_handler import startup_event_app, shutdown_event_app

def create_app():
    app = FastAPI(title="ConcurrentAccessAPI", version="0.1")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get(path="/health", tags=["health"])
    async def health_check():
        return JSONResponse(
            content="UP",
            status_code=200
        )

    # async socket app + kafka consumer
    sio_app = socketio.ASGIApp(socketio_server=sio, other_asgi_app=app, socketio_path='/socket/v1/concurrent',
                               on_startup=startup_event_app, on_shutdown=shutdown_event_app)

    return sio_app


app = create_app()
