import csv
import random
import re
from pathlib import Path

random.seed(42)

INPUT = Path(__file__).parent / "ReportProject2025database.csv"
OUTPUT = Path(__file__).parent / "ReportProject2025database_mock.csv"

PREFIXES = ["PT", "CV"]
ADJECTIVES = [
    "MAJU", "SEJAHTERA", "ABADI", "MANDIRI", "BERSAMA", "CEMERLANG",
    "MULIA", "SENTOSA", "AGUNG", "NUSANTARA", "BINTANG", "BERKAH",
    "KARYA", "SEJATI", "SUKSES", "HARMONI", "GLOBAL",
    "MITRA", "TUNAS", "BAHARI", "CAHAYA", "KENCANA", "PRIMA",
    "JAYA", "PURI", "ASRI", "INDAH", "SARI",
]
NOUNS = [
    "LOGISTIK", "NIAGA", "DISTRIBUSI", "TRANSPORT", "PERKASA",
    "BANGUNAN", "FURNITURE", "TEKNIK", "INDUSTRI", "KONSULTAN",
    "SENTRAL", "USAHA", "DAGANG", "ANUGRAH", "BERKAT",
    "PERSADA", "KREASI", "BUANA", "SAMUDRA", "ENERGI",
]

FAKE_MKT = {
    "HANOM": "SANTOSO",
    "DANIEL": "BUDIMAN",
    "BILLY": "FERNANDO",
    "BASUKI": "PRASETYO",
    "ANDRI": "KUSUMA",
    "DIANA": "WULANDARI",
    "CAHAYA": "HADI",
    "BIMO": "TEJAKUSUMA",
    "ANDIKA": "WIJAYA",
}

with open(INPUT, newline="", encoding="utf-8-sig") as f:
    reader = list(csv.DictReader(f, delimiter=";"))

rows = reader
fieldnames = list(rows[0].keys())
print(f"Fields: {fieldnames}")

real_customers = sorted(set(r["CUSTOMER"].strip() for r in rows))
random.shuffle(ADJECTIVES)
random.shuffle(NOUNS)

fake_customers = {}
for i, real in enumerate(real_customers):
    prefix = random.choice(PREFIXES)
    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    fake_customers[real] = f"{prefix}. {adj} {noun}"

mock_rows = []
for r in rows:
    jobtype = r["JOBTYPE"].strip()
    month_str = r["MONTH"].strip().replace("/", "")
    seq = re.search(r"(\d+)$", r["JOBFILE"].strip())
    seq_str = seq.group(1) if seq else str(random.randint(1, 9999))
    cust = r["CUSTOMER"].strip()
    mkt = r["MKT"].strip()
    revenue_raw = r["REVENUE"].strip().replace(",", "")
    cost_raw = r["COST"].strip().replace(",", "")

    try:
        revenue = float(revenue_raw)
    except ValueError:
        revenue = 0
    try:
        cost = float(cost_raw)
    except ValueError:
        cost = 0

    jitter = random.uniform(0.85, 1.15)
    new_revenue = round(revenue * jitter, 2)
    new_cost = round(cost * jitter, 2)
    new_profit = round(new_revenue - new_cost, 2)
    new_margin = round((new_profit / new_revenue * 100) if new_revenue else 0, 4)

    mock_rows.append({
        "MONTH": r["MONTH"].strip(),
        "JOBTYPE": jobtype,
        "JOBFILE": f"MOCK-{month_str}{seq_str}",
        "CUSTOMER": fake_customers[cust],
        "MKT": FAKE_MKT.get(mkt, "UNKNOWN"),
        "REVENUE": str(new_revenue),
        "COST": str(new_cost),
        "PROFIT": str(new_profit),
        "MARGIN": str(new_margin),
        "NEWCUSTOMER": r["NEWCUSTOMER"].strip(),
    })

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    writer.writerows(mock_rows)

print(f"Written {len(mock_rows)} rows to {OUTPUT}")
print(f"Mapping: {len(real_customers)} customers, {len(FAKE_MKT)} salespeople")
