import os
import requests
from dotenv import load_dotenv

load_dotenv()
topic = os.getenv("NTFY_TOPIC")

r = requests.post(
f"https://ntfy.sh/{topic}",
data="StockLens is alive. Your daily briefing is coming soon.".encode("utf-8"),
headers={"Title": "StockLens"},
timeout=15,
)
print(r.status_code)