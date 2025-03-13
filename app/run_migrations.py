import asyncio
import glob
import os

import asyncpg
from core.config import settings


async def run_migrations():
    conn = await asyncpg.connect(settings.db_url)
    try:
        # Get and sort all migration SQL files from the migrations folder.
        migration_files = sorted(glob.glob(os.path.join("", "migrations", "*.sql")))
        for migration in migration_files:
            with open(migration, "r") as file:
                migration_sql = file.read()
                await conn.execute(migration_sql)
                # TODO: Log the migration in the database.(PROLLY ADD TO README)
                # TODO: use logger instead of print
                print(f"✅ Executed migration: {migration}")
    except Exception as e:
        print("❌ Error running migrations:", e)
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(run_migrations())
