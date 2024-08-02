import requests

import urllib3

urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

STANDARD_HEADERS = {"Content-Type": "application/json; charset=utf-8"}


def _get_headers(auth_token: str):
    return {**STANDARD_HEADERS, "Authorization": auth_token}


def round():
    return {
        "rounds": [
            {
                "name": "DEFAULT",
                "productSymbols": ["FUTURE", "150 CALL", "150 PUT"],
                "sessionCount": 1,
                "positionLimits": [
                    {"productSymbol": "FUTURE", "shortLimit": 100, "longLimit": 100},
                    {"productSymbol": "150 CALL", "shortLimit": 250, "longLimit": 250},
                    {"productSymbol": "150 PUT", "shortLimit": 250, "longLimit": 250},
                ],
            }
        ],
        "defaultRound": "DEFAULT",
        "products": [
            {"symbol": "FUTURE", "tickSize": 1, "startingPrice": 0, "contractSize": 1},
            {
                "symbol": "150 CALL",
                "tickSize": 0.25,
                "startingPrice": 0,
                "contractSize": 1,
            },
            {
                "symbol": "150 PUT",
                "tickSize": 0.25,
                "startingPrice": 0,
                "contractSize": 1,
            },
        ],
    }


class API:

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self._cmi_url = "https://staging-cmi-exchange"
        self._auth = self._authenticate()

    def init_exchange(self):
        url = f"{self._cmi_url}/api/configuration"
        response = requests.put(
            url, headers=_get_headers(self._auth), json=round(), verify=False
        )
        print(response.json())

    def start_trading(self):
        url = f"{self._cmi_url}/api/round/start-trading"
        response = requests.put(url, headers=_get_headers(self._auth), verify=False)
        print("Start trading ", response.ok)

    def stop_trading(self):
        url = f"{self._cmi_url}/api/round/stop-trading"
        response = requests.put(url, headers=_get_headers(self._auth), verify=False)
        print("Stop trading ", response.ok)

    def settlement_prices(
        self, future_price: float, call_price: float, put_price: float
    ):
        url = f"{self._cmi_url}/api/round/settlement-prices"
        json = [
            {"productSymbol": "FUTURE", "settlementPrice": future_price},
            {"productSymbol": "150 CALL", "settlementPrice": call_price},
            {"productSymbol": "150 PUT", "settlementPrice": put_price},
        ]
        response = requests.post(
            url, headers=_get_headers(self._auth), json=json, verify=False
        )
        print(response.json())

    def full_reset(self):
        url = f"{self._cmi_url}/api/configuration/full-reset"
        response = requests.put(url, headers=_get_headers(self._auth), verify=False)
        print("Full reset ", response.ok)

    def news(self, message: str):
        url = f"{self._cmi_url}/api/news"
        response = requests.post(
            url, headers=_get_headers(self._auth), json={"message": message}, verify=False
        )
        print("Message ", response.ok)

    def download_market_trades(self):
        url = f"{self._cmi_url}/api/trade?"
        response = requests.get(
            url, headers=_get_headers(self._auth), verify=False
        )
        return response.json()

    def _authenticate(self):
        auth = {"username": self.username, "password": self.password}
        url = f"{self._cmi_url}/api/user/authenticate"
        response = requests.post(url, headers=STANDARD_HEADERS, json=auth, verify=False)
        response.raise_for_status()
        return response.headers["Authorization"]


if __name__ == "__main__":
    api = API("cmi", "password")