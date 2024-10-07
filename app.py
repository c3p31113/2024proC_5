from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world! access v1 directory"}

@app.get("/v1/")
async def v1root():
    return {"message": "incorrect usage"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="debug")
