from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from online import MatchingRanking

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/search")
async def search(q: str, d: str):
    return MatchingRanking.search(d, q)