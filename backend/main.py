from fastapi import FastAPI

app = FastAPI(title="D-Agent")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

