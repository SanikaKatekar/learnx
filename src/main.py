from fastapi import FastAPI
from api.routes.routes import router

app = FastAPI(title="LearnX")  # Set the title to "LearnX"

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
