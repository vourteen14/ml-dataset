import csv
import uuid
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(202)
random.seed(202)

total_rows = 22612
anomaly_ratio = 0.38
anomaly_count = int(total_rows * anomaly_ratio)

token_symbols = ["ETH", "USDT", "BTC", "DAI", "UNI", "LINK", "AVAX"]
tx_types = ["transfer", "contract_call", "mint", "swap", "bridge"]
risky_tx_types = ["mixer", "bridge", "dark_contract", "unknown_proxy"]
risk_tags = ["mixer", "aml", "scam", "blacklisted", "suspicious"]

def random_eth_address():
    return "0x" + fake.lexify(text="????????????????????????????????????????")

def random_timestamp(normal=True):
    base = datetime(2024, random.randint(1, 6), random.randint(1, 28))
    if normal:
        return (base + timedelta(hours=random.randint(8, 22), minutes=random.randint(0, 59))).isoformat()
    else:
        return (base + timedelta(hours=random.choice([0, 1, 2, 3]), minutes=random.randint(0, 59))).isoformat()

def generate_row(is_anomaly=False):
    from_addr = random_eth_address()
    to_addr = from_addr if is_anomaly and random.random() < 0.5 else random_eth_address()
    value = round(random.uniform(0.01, 2.5), 6) if not is_anomaly else round(random.uniform(5000, 150000), 2)
    gas_fee = round(random.uniform(0.1, 3.0), 3) if not is_anomaly else round(random.uniform(50.0, 999.0), 2)

    return {
        "tx_hash": str(uuid.uuid4()),
        "timestamp": random_timestamp(normal=not is_anomaly),
        "from_address": from_addr,
        "to_address": to_addr,
        "value": value,
        "token_symbol": random.choice(token_symbols),
        "gas_fee_usd": gas_fee,
        "block_time": random_timestamp(normal=not is_anomaly),
        "tx_type": random.choice(risky_tx_types if is_anomaly else tx_types),
        "risk_tag": random.choice(risk_tags) if is_anomaly else ""
    }

rows = []

for _ in range(anomaly_count):
    rows.append(generate_row(is_anomaly=True))

for _ in range(total_rows - anomaly_count):
    rows.append(generate_row(is_anomaly=False))

random.shuffle(rows)

with open("bitcoin.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
