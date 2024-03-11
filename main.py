from fastapi import FastAPI
import uvicorn

from routes import router


app = FastAPI(
    docs_url="/docs"
)


app.include_router(router)


if __name__ == '__main__':
    uvicorn.run('main:app', port=8002, host='localhost')
