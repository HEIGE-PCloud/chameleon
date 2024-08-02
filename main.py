from api import API
from cards import Cards
import time
from datetime import datetime


if __name__ == "__main__":
    interval = 5
    api = API("cmi", "password")
    cards = Cards()
    api.full_reset()
    api.init_exchange()
    api.start_trading()

    for round in range(1, 21, 1):
        print("Round ", round)
        n_cards = cards.get_nth_card(round)
        api.news(n_cards)
        time.sleep(interval)

    api.settlement_prices(
        cards.get_future_price(), cards.get_call_price(), cards.get_put_price()
    )
    api.stop_trading()
    now = datetime.now()

    with open(f"market_trades_{now}", 'w') as file:
        file.write(str(api.download_market_trades()))
    api.full_reset()
