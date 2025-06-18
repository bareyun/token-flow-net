import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ETHERSCAN_API_KEY")
GAS_THRESHOLD = int(os.getenv("GAS_PRICE_THRESHOLD_GWEI", 15))
ETHERSCAN_URL = "https://api.etherscan.io/api"

def get_gas_price():
    params = {
        "module": "gastracker",
        "action": "gasoracle",
        "apikey": API_KEY
    }
    response = requests.get(ETHERSCAN_URL, params=params)
    data = response.json()
    if data["status"] != "1":
        raise Exception("Failed to get gas price")
    return int(data["result"]["SafeGasPrice"])

def main():
    print(f"🎯 Monitoring Ethereum gas price... (target ≤ {GAS_THRESHOLD} Gwei)")
    while True:
        try:
            price = get_gas_price()
            print(f"⛽ Current SafeGasPrice: {price} Gwei")
            if price <= GAS_THRESHOLD:
                print(f"✅ Gas price is low! ({price} Gwei) — great time to snipe!")
            time.sleep(60)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(120)

if __name__ == "__main__":
    main()
