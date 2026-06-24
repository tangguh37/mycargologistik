import csv
import random
from pathlib import Path

random.seed(42)

INPUT = Path(__file__).parent / "data/ReportProject2025database.csv"
OUTPUT = Path(__file__).parent / "data/ReportProject2025database_mock.csv"

PREFIXES = ["PT", "CV"]

ADJECTIVES = [
    "MAJU", "SEJAHTERA", "ABADI", "MANDIRI", "BERSAMA", "CEMERLANG",
    "MULIA", "SENTOSA", "AGUNG", "NUSANTARA", "BINTANG", "BERKAH",
    "KARYA", "SEJATI", "SUKSES", "HARMONI", "GLOBAL",
    "MITRA", "TUNAS", "BAHARI", "CAHAYA", "KENCANA", "PRIMA",
    "JAYA", "PURI", "ASRI", "INDAH", "SARI",
    "DELIMA", "GADING", "INTAN", "MUTIARA", "PERMATA", "SAKTI",
    "WIRA", "YASA", "BUDI", "DAYA", "KARTIKA", "WANA",
]

NOUNS = [
    "LOGISTIK", "NIAGA", "DISTRIBUSI", "TRANSPORT", "PERKASA",
    "BANGUNAN", "FURNITURE", "TEKNIK", "INDUSTRI", "KONSULTAN",
    "SENTRAL", "USAHA", "DAGANG", "ANUGRAH", "BERKAT",
    "PERSADA", "KREASI", "BUANA", "SAMUDRA", "ENERGI",
    "ELEKTRIK", "KIMIA", "PANGAN", "TEKSTIL", "OTOMOTIF",
    "PROPERTI", "TAMBANG", "PERTANIAN", "KESEHATAN", "EDUKASI",
    "MARITIM", "DIRGANTARA", "TELKOM", "MEDIA", "KEUANGAN",
]

FAKE_MKT = ["SANTOSO", "BUDIMAN", "FERNANDO", "PRASETYO", "KUSUMA",
            "WULANDARI", "HADI", "TEJAKUSUMA", "WIJAYA"]

with open(INPUT, newline="", encoding="utf-8-sig") as f:
    reader = list(csv.DictReader(f, delimiter=";"))

rows = reader
fieldnames = list(rows[0].keys())
print(f"Fields: {fieldnames}")

mock_rows = []
seq_counter = 1

for r in rows:
    for _ in range(2):
        month_raw = r["MONTH"].strip()
        month_compact = month_raw.replace("/", "")

        prefix = random.choice(PREFIXES)
        adj = random.choice(ADJECTIVES)
        noun = random.choice(NOUNS)
        fake_customer = f"{prefix}. {adj} {noun}"

        mkt = random.choice(FAKE_MKT)

        jobfile = f"MOCK-{month_compact}{seq_counter:06d}"
        seq_counter += 1

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

        jitter = random.uniform(0.50, 1.50)
        new_revenue = round(revenue * jitter, 2)
        new_cost = round(cost * jitter, 2)
        new_profit = round(new_revenue - new_cost, 2)
        new_margin = round((new_profit / new_revenue * 100) if new_revenue else 0, 4)

        mock_rows.append({
            "MONTH": month_raw,
            "JOBTYPE": r["JOBTYPE"].strip(),
            "JOBFILE": jobfile,
            "CUSTOMER": fake_customer,
            "MKT": mkt,
            "REVENUE": str(new_revenue),
            "COST": str(new_cost),
            "PROFIT": str(new_profit),
            "MARGIN": str(new_margin),
            "NEWCUSTOMER": r["NEWCUSTOMER"].strip(),
        })

output_path = Path(OUTPUT)
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    writer.writerows(mock_rows)

print(f"Written {len(mock_rows)} rows to {OUTPUT}")
print(f"Unique customers generated: {len(set(r['CUSTOMER'] for r in mock_rows))}")
print(f"MKT pool: {len(FAKE_MKT)} salespeople")
