import uvicorn
from src.metadata import API_HOST, API_PORT, API_WORKERS

if __name__ == "__main__":
    uvicorn.run(
        "src.server:app",
        host=API_HOST,
        port=API_PORT,
        workers=API_WORKERS
    )