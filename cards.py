import random
import logging
logger = logging.getLogger(__name__)


def format_card(n: int):
    if n >= 2 and n <= 10:
        return str(n)
    if n == 1:
        return "A"
    if n == 11:
        return "J"
    if n == 12:
        return "Q"
    if n == 13:
        return "K"
    raise RuntimeError("Invalid card", n)


class Cards:
    all_cards = [
        1,
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        3,
        3,
        3,
        3,
        4,
        4,
        4,
        4,
        5,
        5,
        5,
        5,
        6,
        6,
        6,
        6,
        7,
        7,
        7,
        7,
        8,
        8,
        8,
        8,
        9,
        9,
        9,
        9,
        10,
        10,
        10,
        10,
        11,
        11,
        11,
        11,
        12,
        12,
        12,
        12,
        13,
        13,
        13,
        13,
    ]

    def __init__(self) -> None:
        self.cards = self.all_cards.copy()
        self.shuffle()
        logger.info("A set of cards have been initialized")
        logger.info(f"Future price: {self.get_future_price()}")
        logger.info(f"Call price: {self.get_call_price()}")
        logger.info(f"Put price: {self.get_put_price()}")

    def shuffle(self):
        random.shuffle(self.cards)

    def get_future_price(self):
        return sum(self.cards[:20])

    def get_first_n_cards(self, n: int):
        return self.cards[:n]

    def get_nth_card(self, n: int) -> str:
        return format_card(self.cards[n - 1])

    def get_call_price(self):
        future_price = self.get_future_price()
        if future_price <= 150:
            return 0
        return future_price - 150

    def get_put_price(self):
        future_price = self.get_future_price()
        if future_price >= 130:
            return 0
        return 130 - future_price


if __name__ == "__main__":
    cards = Cards()
    print(cards.get_first_n_cards(20))
