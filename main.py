from api import API
from cards import Cards
import time
from datetime import datetime
import logging
import uuid
from fastapi import FastAPI, BackgroundTasks
import json
isGameRunning = False


def game(game_id: str, interval: float = 60):
    global isGameRunning
    isGameRunning = True
    api = API("cmi", "password")
    cards = Cards()
    api.full_reset()
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
    now = datetime.now()

    with open(f"market_trades_{game_id}", "w") as file:
        file.write(str(api.download_market_trades()))
    isGameRunning = False


app = FastAPI()


@app.post("/start_game/{interval}")
async def start_game(interval: float, background_tasks: BackgroundTasks):
    if isGameRunning:
        return {"error": "Game is running"}
    game_id = str(uuid.uuid4())
    background_tasks.add_task(game, game_id, interval)
    return {"game_id": game_id}


@app.post("/end_game")
def end_game():
    global isGameRunning
    isGameRunning = False


@app.get("/trades/{game_id}")
def trades(game_id: str):
    with open(f"market_trades_{game_id}", "r") as file:
        return json.load(file)
