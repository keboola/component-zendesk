import duckdb

duck = duckdb.connect('../src/dlt_zendesk_pipeline.duckdb')
print(duck.sql("DESCRIBE;"))
tables = duck.sql("SELECT table_name FROM information_schema.tables;").fetchall()
for table in tables:
    print(table[0])


duck.close()
