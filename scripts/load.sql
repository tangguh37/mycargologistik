\copy monthly_reports(month, jobtype, jobfile, customer, mkt, revenue, cost, profit, margin, newcustomer)
FROM '../data/ReportProject2025database_mock.csv'
DELIMITER ';'
CSV HEADER;
