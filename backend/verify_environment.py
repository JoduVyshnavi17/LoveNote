"""Read-only preflight: checks DB connectivity and expected legacy tables."""
from sqlalchemy import inspect, text
from app.database import engine

EXPECTED = {"users", "documents", "pages", "revisions", "study_materials", "suggestions"}
print("LoveNotes database preflight (read-only)")
print("Dialect:", engine.dialect.name)
with engine.connect() as connection:
    connection.execute(text("SELECT 1"))
print("Database connection: PASS")
tables = set(inspect(engine).get_table_names())
print("Tables:", ", ".join(sorted(tables)) or "(none)")
missing = EXPECTED - tables
if missing:
    print("NOTICE: expected tables not found:", ", ".join(sorted(missing)))
else:
    print("Expected table names: PASS")
print("No data or schema was modified.")
