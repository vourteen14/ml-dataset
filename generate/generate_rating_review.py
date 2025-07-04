import csv
import uuid
import random
from faker import Faker
from datetime import datetime, timedelta
import ipaddress

fake = Faker("id_ID")
Faker.seed(303)
random.seed(303)

total_rows = 66542
noise_ratio = 0.64
noise_count = int(total_rows * noise_ratio)

cities = ["Jakarta", "Bandung", "Surabaya", "Medan", "Semarang", "Denpasar"]
foreign_countries = ["Russia", "Iran", "China", "Vietnam", "Ukraine"]
local_country = "Indonesia"

short_noise_texts = [
    "", "...", "gak suka", "buruk", "jelek", "meh", "nope", "tidak rekomendasi",
    "parah", "ampas", "gak jelas", "zonk", "asal kirim", "ngecewain", "gak sesuai", 
    "bohong", "kurang bagus", "asal-asalan", "tidak layak beli", "menyesal beli", 
    "fake", "gagal paham", "gak ngerti maksudnya apa", "ga mutu", "pelayanan buruk", 
    "tiba-tiba rusak", "kok bisa gini?", "udah jelek mahal lagi", "omong kosong", 
    "tidak seperti yang diiklankan", "jangan beli", "langsung refund", "gue kecewa banget",
    "gak worth it", "seller gak tanggung jawab", "bikin emosi", "kualitas parah",
    "aneh", "aneh banget", "masa sih begini?", "beneran zonk", "1 kata: nyesel",
    "katanya ori, tapi kok gini", "barang KW ya?", "buruk sekali", "bikin malu",
    "jelek bgt", "padahal berharap banyak", "tidak masuk akal"
]

normal_texts = [
    "Barang sampai tepat waktu dan sesuai deskripsi.",
    "Pelayanan sangat memuaskan, seller responsif.",
    "Pengemasan rapi dan produk berkualitas.",
    "Agak telat dikirim, tapi masih oke.",
    "Harga bersaing dan kualitas bagus.",
    "Paket rusak saat diterima, kecewa.",
    "Produk palsu, tidak sesuai gambar!",
    "Pengiriman sangat lama dan tidak sesuai ekspetasi."
]

# IP & Device pool buat simulate collision
shared_ip = "123.123.10."
shared_devices = ["dev001", "dev002", "dev003"]

def random_ip(shared=False):
    if shared:
        return f"{shared_ip}{random.randint(10, 99)}"
    return str(ipaddress.IPv4Address(random.randint(2**24, 2**32 - 1)))

def generate_row(is_noise=False):
    rating = random.choice([1, 2]) if is_noise else random.randint(3, 5)
    review_text = random.choice(short_noise_texts) if is_noise else random.choice(normal_texts)
    country = random.choice(foreign_countries) if is_noise and random.random() < 0.3 else local_country
    city = random.choice(cities)

    return {
        "event_id": str(uuid.uuid4()),
        "user_id": fake.uuid4()[:8],
        "timestamp": (datetime(2024, random.randint(1, 6), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59))).isoformat(),
        "rating": rating,
        "review_text": review_text,
        "seller_id": "SELLER01" if is_noise and random.random() < 0.7 else fake.uuid4()[:8],
        "ip_address": random_ip(shared=is_noise and random.random() < 0.7),
        "device_id": random.choice(shared_devices) if is_noise and random.random() < 0.6 else fake.uuid4()[:6],
        "location_city": city,
        "location_country": country
    }

# Generate data
rows = []

for _ in range(noise_count):
    rows.append(generate_row(is_noise=True))

for _ in range(total_rows - noise_count):
    rows.append(generate_row(is_noise=False))

random.shuffle(rows)

with open("rating_review.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)