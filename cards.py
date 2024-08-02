import random


class Cards:
    all_cards = [
        "A",
        "A",
        "A",
        "A",
        "2",
        "2",
        "2",
        "2",
        "3",
        "3",
        "3",
        "3",
        "4",
        "4",
        "4",
        "4",
        "5",
        "5",
        "5",
        "5",
        "6",
        "6",
        "6",
        "6",
        "7",
        "7",
        "7",
        "7",
        "8",
        "8",
        "8",
        "8",
        "9",
        "9",
        "9",
        "9",
        "10",
        "10",
        "10",
        "10",
        "J",
        "J",
        "J",
        "J",
        "Q",
        "Q",
        "Q",
        "Q",
        "K",
        "K",
        "K",
        "K",
    ]

    def __init__(self) -> None:
        self.cards = self.all_cards.copy()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def get_future_price(self):
        return sum(self.cards[:20])

    def get_first_n_cards(self, n: int):
        return self.cards[:n]

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
