import math
from api import API
from cards import Cards
import time
import logging
import uuid
from pathlib import Path
import json

from fastapi import FastAPI, BackgroundTasks, HTTPException

logging.basicConfig(level=logging.INFO)

isGameRunning = False

def game(game_id: str, interval: float = 60):
    global isGameRunning
    isGameRunning = True
    api = API("cmi", "password")
    cards = Cards()
    api.reset_trading()
    api.init_exchange()
    api.start_trading()

    for round in range(1, 21, 1):
        if not isGameRunning:
            print("End Game early!")
            return
        print("Round ", round)
        n_cards = cards.get_nth_card(round)
        api.news(n_cards)
        time.sleep(interval)

    api.settlement_prices(
        cards.get_future_price(), cards.get_call_price(), cards.get_put_price()
    )
    api.stop_trading()

    with open(f"market_trades_{game_id}", "w") as file:
        json.dump(api.download_market_trades(), file)
    isGameRunning = False


app = FastAPI()

@app.post("/start_game/{interval}")
async def start_game(interval: float, background_tasks: BackgroundTasks):
    global isGameRunning

    if isGameRunning:
        raise HTTPException(status_code=409, detail="Game is running")
    if interval < 1 or interval > 60 or math.isnan(interval):
        raise HTTPException(status_code=400, detail="Nice try")
    game_id = str(uuid.uuid4())

    isGameRunning = True
    background_tasks.add_task(game, game_id, interval)
    return {"game_id": game_id}


@app.post("/end_game")
def end_game():
    global isGameRunning
    isGameRunning = False


@app.get("/trades/{game_id}")
def trades(game_id: str):
    my_file = Path(f"./market_trades_{game_id}")

    if not my_file.is_file():
        raise HTTPException(status_code=400, detail="Invalid game id")

    with open(my_file, "r") as file:
        return file.read()

