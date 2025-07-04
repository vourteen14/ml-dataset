import csv
import random
import uuid
from faker import Faker
from datetime import datetime

fake = Faker("id_ID")
Faker.seed(101)
random.seed(101)

total_rows = 91969
anomaly_ratio = 0.43
anomaly_count = int(total_rows * anomaly_ratio)

cities = [
    "Jakarta", "Bandung", "Surabaya", "Medan", "Semarang", "Yogyakarta",
    "Denpasar", "Makassar", "Palembang", "Manado"
]
normal_country = ["Indonesia"]
foreign_countries = ["Russia", "Netherlands", "Vietnam", "USA", "Brazil", "Iran", "North Korea"]

channels = ["app", "web", "qr", "pos"]
suspicious_channels = ["api", "scripted", "cli", "phantom"]

def random_datetime(normal=True):
    if normal:
        hour = random.randint(8, 22)
    else:
        hour = random.choice([0, 1, 2, 3, 4])
    return datetime(2024, random.randint(1, 6), random.randint(1, 28), hour, random.randint(0, 59)).isoformat()

def random_coords(city):
    mapping = {
        "Jakarta": (-6.2, 106.8),
        "Bandung": (-6.9, 107.6),
        "Surabaya": (-7.2, 112.7),
        "Medan": (3.6, 98.7),
        "Semarang": (-7.0, 110.4),
        "Yogyakarta": (-7.8, 110.4),
        "Denpasar": (-8.7, 115.2),
        "Makassar": (-5.1, 119.4),
        "Palembang": (-2.9, 104.7),
        "Manado": (1.4, 124.8)
    }
    lat, lon = mapping.get(city, (-6.2, 106.8))
    return round(lat + random.uniform(-0.01, 0.01), 6), round(lon + random.uniform(-0.01, 0.01), 6)

def random_far_coords():
    # Koordinat aneh untuk fraud (luar negeri / laut)
    return round(random.uniform(-45, 45), 6), round(random.uniform(-170, 170), 6)

def generate_row(is_anomaly=False):
    city = random.choice(cities)
    if is_anomaly:
        lat, lon = random_far_coords()
        channel = random.choice(suspicious_channels)
        country = random.choice(foreign_countries)
        amount = round(random.uniform(500000, 10000000), 2)
    else:
        lat, lon = random_coords(city)
        channel = random.choice(channels)
        country = "Indonesia"
        amount = round(random.uniform(10000, 250000), 2)

    return {
        "event_id": str(uuid.uuid4()),
        "user_id": fake.uuid4()[:8],
        "timestamp": random_datetime(normal=not is_anomaly),
        "amount": amount,
        "merchant_id": fake.uuid4()[:8],
        "channel": channel,
        "latitude": lat,
        "longitude": lon,
        "location_city": city,
        "location_country": country,
        "success": random.choices([True, False], weights=[0.85, 0.15])[0]
    }

# Generate data
rows = []

for _ in range(anomaly_count):
    rows.append(generate_row(is_anomaly=True))

for _ in range(total_rows - anomaly_count):
    rows.append(generate_row(is_anomaly=False))

random.shuffle(rows)

with open("transaksi_fintech.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)