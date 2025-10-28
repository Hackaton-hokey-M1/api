from pathlib import Path
from sqlmodel import text

def seed_data(session):
    """Seed the database with hockey data. Clears and reseeds every time."""

    print("🔄 Reseeding database...")

    # Clear existing data (respecting foreign keys order)
    session.exec(text("DELETE FROM match"))
    session.exec(text("DELETE FROM tournament"))
    session.exec(text("DELETE FROM team"))
    session.commit()

    # Read and execute SQL file
    sql_file = Path(__file__).parent / "seed_data.sql"

    if not sql_file.exists():
        print(f"⚠️  {sql_file} not found. Skipping seed.")
        return

    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Parse SQL statements (remove comments, split by semicolon)
    lines = [line.strip() for line in sql_content.split('\n')
             if line.strip() and not line.startswith('--')]

    statements = [stmt.strip() for stmt in ' '.join(lines).split(';') if stmt.strip()]

    # Execute statements
    for statement in statements:
        session.exec(text(statement))

    session.commit()
    print(f"✓ Database seeded with {len(statements)} statements")
