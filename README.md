# Mycargologistik

Monthly company report dashboard — Excel → PostgreSQL → Metabase.

## Workflow

1. **Clean** raw monthly reports in Excel
2. **Load** into PostgreSQL (see `scripts/load.sql`)
3. **Visualize** in Metabase connected to the database

## Project structure

```
├── data/
│   └── ReportProject2025database_mock.csv   # anonymized sample data
├── scripts/
│   ├── anonymize.py     # generates mock CSV from real data
│   └── load.sql         # \copy commands to import into PostgreSQL
├── sql/
│   └── schema.sql       # table DDL
└── metabase/            # dashboard exports
```

## Setup

1. Create the database and table:
   ```bash
   psql -U postgres -d mycargologistik -f sql/schema.sql
   ```
2. Load the CSV:
   ```bash
   psql -U postgres -d mycargologistik -f scripts/load.sql
   ```
3. Open Metabase and connect to your database.
