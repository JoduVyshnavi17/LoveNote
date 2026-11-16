"""Read-only database inventory. This script never creates, alters, or deletes data."""
from sqlalchemy import inspect
from app.database import engine

if __name__ == "__main__":
    inspector = inspect(engine)
    print(f"Database dialect: {engine.dialect.name}")
    print("Tables found:")
    for table in inspector.get_table_names():
        print(f"\n[{table}]")
        for col in inspector.get_columns(table):
            print(f"  {col['name']}: {col['type']} nullable={col.get('nullable')}")
    print("\nRead-only inspection complete. No schema or data was changed.")
