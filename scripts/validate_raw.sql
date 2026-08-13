SELECT 'orders' table_name, COUNT(*) row_count FROM `YOUR_GCP_PROJECT_ID.retail_ai_raw.orders`
UNION ALL SELECT 'order_items', COUNT(*) FROM `YOUR_GCP_PROJECT_ID.retail_ai_raw.order_items`
UNION ALL SELECT 'payments', COUNT(*) FROM `YOUR_GCP_PROJECT_ID.retail_ai_raw.payments`
UNION ALL SELECT 'shipments', COUNT(*) FROM `YOUR_GCP_PROJECT_ID.retail_ai_raw.shipments`;

SELECT country_code, DATE(order_timestamp) order_date, COUNT(*) orders, ROUND(AVG(TIMESTAMP_DIFF(source_available_timestamp, order_timestamp, MINUTE)),1) avg_source_delay_minutes
FROM `YOUR_GCP_PROJECT_ID.retail_ai_raw.orders`
WHERE DATE(order_timestamp)='2026-06-18'
GROUP BY 1,2 ORDER BY avg_source_delay_minutes DESC;

SELECT * FROM `YOUR_GCP_PROJECT_ID.retail_ai_raw.pipeline_runs`
WHERE business_date='2026-06-18' AND pipeline_name='orders_ingestion';
