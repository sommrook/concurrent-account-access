import uvicorn
from app.core.settings import API_HOST, API_PORT, API_WORKERS

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app",
        host=API_HOST,
        port=API_PORT,
        workers=API_WORKERS
    )