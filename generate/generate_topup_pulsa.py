import csv
import random
import uuid
from faker import Faker
from datetime import datetime

fake = Faker("id_ID")
Faker.seed(99)
random.seed(99)

total_rows = 79718
anomaly_ratio = 0.38
anomaly_count = int(total_rows * anomaly_ratio)

cities = [
    "Jakarta", "Bandung", "Surabaya", "Medan", "Semarang", "Yogyakarta",
    "Denpasar", "Makassar", "Manado", "Balikpapan", "Palembang", "Pontianak"
]
normal_country = ["Indonesia"]
foreign_countries = ["Russia", "Netherlands", "Vietnam", "China", "Brazil", "South Korea", "Germany"]

nominal_choices = [5000, 10000, 25000, 50000, 100000]
weird_nominal = [250000, 500000, 1000000]

payment_channels = ["e-wallet", "mobile-banking", "retail", "voucher"]
rare_channels = ["sms-gateway", "unknown", "cli"]

def random_datetime(normal=True):
    if normal:
        hour = random.randint(7, 22)
    else:
        hour = random.choice([0, 1, 2, 3, 4])
    return datetime(2024, random.randint(1, 6), random.randint(1, 28), hour, random.randint(0, 59)).isoformat()

def generate_msisdn():
    return "08999" + str(random.randint(10000000, 99999999))

def generate_serial_number(suspicious=False):
    if suspicious:
        return "SN-X-" + fake.lexify(text='????????')  # SN aneh
    return "SN-" + str(random.randint(10000000, 99999999))

def generate_row(is_anomaly=False):
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": fake.uuid4()[:8],
        "timestamp": random_datetime(normal=not is_anomaly),
        "msisdn": generate_msisdn(),
        "nominal": random.choice(weird_nominal if is_anomaly else nominal_choices),
        "serial_number": generate_serial_number(suspicious=is_anomaly),
        "payment_channel": random.choice(rare_channels if is_anomaly else payment_channels),
        "location_city": random.choice(cities),
        "location_country": random.choice(foreign_countries if is_anomaly else normal_country),
        "topup_success": random.choices([True, False], weights=[0.85, 0.15])[0]
    }

# Build dataset
rows = []

for _ in range(anomaly_count):
    rows.append(generate_row(is_anomaly=True))

for _ in range(total_rows - anomaly_count):
    rows.append(generate_row(is_anomaly=False))

random.shuffle(rows)

with open("topup_pulsa.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
