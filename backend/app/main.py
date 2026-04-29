from fastapi import FastAPI

app = FastAPI()

@app.get("/api/status")
def status():
    return {"status": "rodando"}