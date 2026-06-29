from app.database import engine, Base
from app import models
from sqlalchemy import inspect

# Create all tables
Base.metadata.create_all(bind=engine)

# Inspect database tables
inspector = inspect(engine)

print("Tables in database:")
print(inspector.get_table_names())