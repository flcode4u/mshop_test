from sqlalchemy import create_engine

DATABASE_URL = "postgresql://neondb_owner:npg_QG8KrAXgzp3f@ep-holy-hill-a2798f83-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require"

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("✅ Connected successfully!")
    connection.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
