CREATE TABLE IF NOT EXISTS monthly_reports (
    id          SERIAL PRIMARY KEY,
    month       DATE NOT NULL,
    jobtype     VARCHAR(50),
    jobfile     VARCHAR(100),
    customer    VARCHAR(200),
    mkt         VARCHAR(100),
    revenue     NUMERIC(15,2),
    cost        NUMERIC(15,2),
    profit      NUMERIC(15,2),
    margin      NUMERIC(10,4),
    newcustomer VARCHAR(20)
);
