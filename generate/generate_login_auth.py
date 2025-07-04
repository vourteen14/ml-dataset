import csv
import random
import uuid
from faker import Faker
from datetime import datetime, time

fake = Faker("id_ID")
Faker.seed(42)
random.seed(42)

total_rows = 53521
anomaly_ratio = 0.43
anomaly_count = int(total_rows * anomaly_ratio)

channels = ["app", "web", "api"]
cities = [
    "Jakarta", "Bandung", "Surabaya", "Medan", "Semarang", "Yogyakarta",
    "Denpasar", "Balikpapan", "Pontianak", "Manado", "Makassar", "Padang",
    "Pekanbaru", "Batam", "Malang", "Banjarmasin"
]

normal_countries = ["Indonesia"]
foreign_countries = [
    "Indonesia", "Singapore", "Germany", "USA", "Netherlands", "Brazil",
    "India", "Vietnam", "China", "Thailand", "Russia", "Canada",
    "South Korea", "United Kingdom", "Australia"
]

normal_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Linux; Android 10; SM-G970F)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "curl/7.64.1",
    "okhttp/4.9.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4)",
    "Mozilla/5.0 (Linux; U; Android 9; en-US; Redmi Note 7)",
    "PostmanRuntime/7.28.0",
    "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X)"
]

suspicious_agents = [
    "curl/7.64.1",
    "okhttp/4.9.1",
    "PostmanRuntime/7.28.0",
    "python-requests/2.28.1"
]

devices = ["MOB", "TAB", "PC"]

def random_datetime(normal=True):
    if normal:
        hour = random.randint(7, 22)  # jam wajar
    else:
        hour = random.choice([0, 1, 2, 3, 4])
    return datetime(2024, random.randint(1, 6), random.randint(1, 28), hour, random.randint(0, 59)).isoformat()

def generate_row(is_anomaly=False):
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": fake.uuid4()[:8],
        "timestamp": random_datetime(normal=not is_anomaly),
        "ip_address": fake.ipv4_public(),
        "user_agent": random.choice(suspicious_agents if is_anomaly else normal_agents),
        "device_id": random.choice(devices) + str(random.randint(1000, 9999)),
        "login_channel": random.choice(channels),
        "location_city": random.choice(cities),
        "location_country": random.choice(foreign_countries if is_anomaly else normal_countries),
        "login_success": random.choices([True, False], weights=[0.8, 0.2])[0]
    }

rows = []

for _ in range(anomaly_count):
    rows.append(generate_row(is_anomaly=True))

for _ in range(total_rows - anomaly_count):
    rows.append(generate_row(is_anomaly=False))

random.shuffle(rows)

with open("login_auth.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)