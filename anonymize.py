import csv
import random
from pathlib import Path
from collections import defaultdict

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

# --- 180 customer pool, 2 whales ---
CUSTOMER_POOL = []
for _ in range(180):
    prefix = random.choice(PREFIXES)
    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    CUSTOMER_POOL.append(f"{prefix}. {adj} {noun}")

random.shuffle(CUSTOMER_POOL)
WHALES = set(CUSTOMER_POOL[:2])
OTHERS = CUSTOMER_POOL[2:]

# --- MKT tiers: 2 over, 4 under, 3 normal ---
MKT_NAMES = ["SANTOSO", "BUDIMAN", "FERNANDO", "PRASETYO", "KUSUMA",
             "WULANDARI", "HADI", "TEJAKUSUMA", "WIJAYA"]
random.shuffle(MKT_NAMES)

MKT_TIERS = {}
for n in MKT_NAMES[:2]:
    MKT_TIERS[n] = {"rev": 1.10, "cost": 0.95}
for n in MKT_NAMES[2:6]:
    MKT_TIERS[n] = {"rev": 0.90, "cost": 1.05}
for n in MKT_NAMES[6:]:
    MKT_TIERS[n] = {"rev": 1.0, "cost": 1.0}

# --- Jobtype pools (only types that exist in original data) ---
EXPORT_TYPES = ["EXPORT AF", "EXPORT FCL", "EXPORT LCL"]
IMPORT_TYPES = ["IMPORT AF", "IMPORT FCL", "IMPORT LCL"]
OTHER_TYPES = ["MDP"]

def pick_jobtype():
    r = random.random()
    if r < 0.40:
        return random.choice(EXPORT_TYPES)
    elif r < 0.65:
        return random.choice(IMPORT_TYPES)
    else:
        return random.choice(OTHER_TYPES)

# --- Seasonal multipliers (month 1-12) ---
def seasonal_mult(m):
    if m <= 3:
        return 1.30
    elif m <= 6:
        return 0.75
    elif m <= 9:
        return 0.85 + (m - 6) * 0.10
    else:
        return 1.15 + (m - 9) * 0.05

# --- Read input ---
with open(INPUT, newline="", encoding="utf-8-sig") as f:
    reader = list(csv.DictReader(f, delimiter=";"))

fieldnames = list(reader[0].keys())

month_groups = defaultdict(list)
for r in reader:
    month_groups[r["MONTH"].strip()].append(r)

sorted_months = sorted(month_groups.keys(), key=lambda m: (
    int(m.split("/")[2]),
    int(m.split("/")[1]),
    int(m.split("/")[0]),
))

mock_rows = []
seq_counter = 1

prev_month_revenue = 500_000_000 * random.uniform(0.8, 1.2)

for month_idx, month_key in enumerate(sorted_months):
    parts = month_key.split("/")
    month_num = int(parts[1])

    growth_rate = random.uniform(-0.05, 0.12)
    growth_jitter = random.uniform(0.8, 1.2)
    effective_growth = growth_rate * growth_jitter

    target_month_revenue = prev_month_revenue * (1 + effective_growth) * seasonal_mult(month_num)

    prev_month_revenue = target_month_revenue

    original_count = len(month_groups[month_key])
    target_rows = original_count * 2 + random.randint(-2, 2)
    target_rows = max(original_count, target_rows)

    orig_flags = [r["NEWCUSTOMER"].strip() for r in month_groups[month_key]]
    new_flags = []
    for f in orig_flags:
        new_flags.append(f)
        if random.random() < 0.1:
            new_flags.append("NEW" if f == "REGULAR" else "REGULAR")
        else:
            new_flags.append(f)
    while len(new_flags) < target_rows:
        new_flags.append("NEW" if random.random() < 0.3 else "REGULAR")
    new_flags = new_flags[:target_rows]

    num_whale_rows = max(int(target_rows * 0.08), 2)
    num_other_rows = target_rows - num_whale_rows

    whale_assignments = random.choices(list(WHALES), k=num_whale_rows)
    other_assignments = random.choices(OTHERS, k=num_other_rows)

    whale_rev_pool = target_month_revenue * 0.8
    other_rev_pool = target_month_revenue * 0.2

    whale_weights = [random.random() for _ in range(num_whale_rows)]
    total_ww = sum(whale_weights)
    whale_revs = [w / total_ww * whale_rev_pool for w in whale_weights]

    other_weights = [random.random() for _ in range(num_other_rows)]
    total_ow = sum(other_weights)
    other_revs = [w / total_ow * other_rev_pool for w in other_weights]

    all_mkt = random.choices(MKT_NAMES, k=target_rows)

    combined = list(zip(
        whale_assignments + other_assignments,
        whale_revs + other_revs,
        all_mkt,
        new_flags,
    ))
    random.shuffle(combined)

    for cust, rev, mkt, newcust_flag in combined:
        mkt_tier = MKT_TIERS[mkt]
        rev_with_mkt = rev * mkt_tier["rev"]

        margin_jitter = random.uniform(0.7, 1.3)
        actual_margin = 0.27 * margin_jitter
        actual_margin = max(0.05, min(0.50, actual_margin))

        cost = rev_with_mkt * (1 - actual_margin) * mkt_tier["cost"]
        profit = rev_with_mkt - cost
        margin = (profit / rev_with_mkt * 100) if rev_with_mkt else 0

        jobtype = pick_jobtype()
        jobfile = f"MOCK-{month_key.replace('/', '')}{seq_counter:06d}"
        seq_counter += 1

        mock_rows.append({
            "MONTH": month_key,
            "JOBTYPE": jobtype,
            "JOBFILE": jobfile,
            "CUSTOMER": cust,
            "MKT": mkt,
            "REVENUE": f"{rev_with_mkt:.2f}",
            "COST": f"{cost:.2f}",
            "PROFIT": f"{profit:.2f}",
            "MARGIN": f"{margin:.4f}",
            "NEWCUSTOMER": newcust_flag,
        })

output_path = Path(OUTPUT)
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    writer.writerows(mock_rows)

total_rev = sum(float(r["REVENUE"]) for r in mock_rows)
total_cost = sum(float(r["COST"]) for r in mock_rows)
total_profit = sum(float(r["PROFIT"]) for r in mock_rows)
overall_margin = (total_profit / total_rev * 100) if total_rev else 0
unique_customers = len(set(r["CUSTOMER"] for r in mock_rows))
whale_rev = sum(float(r["REVENUE"]) for r in mock_rows if r["CUSTOMER"] in WHALES)
whale_share = (whale_rev / total_rev * 100) if total_rev else 0

print(f"Written {len(mock_rows)} rows")
print(f"Total revenue: {total_rev:,.0f}")
print(f"Overall margin: {overall_margin:.2f}%")
print(f"Unique customers: {unique_customers}")
print(f"Whale revenue share: {whale_share:.1f}%")

jt_counts = defaultdict(int)
for r in mock_rows:
    jt_counts[r["JOBTYPE"]] += 1
export_total = sum(v for k, v in jt_counts.items() if k.startswith("EXPORT"))
import_total = sum(v for k, v in jt_counts.items() if k.startswith("IMPORT"))
print(f"\nJobtype: EXPORT {export_total} ({export_total/len(mock_rows)*100:.1f}%) | IMPORT {import_total} ({import_total/len(mock_rows)*100:.1f}%) | OTHER {len(mock_rows)-export_total-import_total} ({(len(mock_rows)-export_total-import_total)/len(mock_rows)*100:.1f}%)")

for mkt in MKT_NAMES:
    mkt_rev = sum(float(r["REVENUE"]) for r in mock_rows if r["MKT"] == mkt)
    mkt_profit = sum(float(r["PROFIT"]) for r in mock_rows if r["MKT"] == mkt)
    mkt_margin = (mkt_profit / mkt_rev * 100) if mkt_rev else 0
    tier_label = "OVER" if mkt in MKT_NAMES[:2] else ("UNDER" if mkt in MKT_NAMES[2:6] else "NORMAL")
    print(f"  MKT {mkt} [{tier_label}]: rev={mkt_rev:,.0f} margin={mkt_margin:.1f}%")
