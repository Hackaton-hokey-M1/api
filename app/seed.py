from pathlib import Path
from sqlmodel import text
from datetime import datetime, timedelta
import random

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

    # Add matches every 10 minutes until 23:00
    add_matches_every_10_minutes(session)


def add_matches_every_10_minutes(session):
    """Add matches every 10 minutes until 23:00 today."""
    from .models import Match

    now = datetime.now()
    end_time = now.replace(hour=23, minute=0, second=0, microsecond=0)
    current_time = now

    # Round to next 10-minute slot
    minutes = (current_time.minute // 10 + 1) * 10
    if minutes >= 60:
        current_time = current_time.replace(hour=current_time.hour + 1, minute=0, second=0, microsecond=0)
    else:
        current_time = current_time.replace(minute=minutes, second=0, microsecond=0)

    # Available teams and tournaments
    teams = list(range(1, 9))  # 8 teams (IDs 1-8)
    tournaments = [1, 2]  # 2 tournaments

    match_count = 0

    while current_time <= end_time:
        # Random tournament
        tournament_id = random.choice(tournaments)

        # Two different teams
        home_team_id, away_team_id = random.sample(teams, 2)

        # Create match (NULL scores for future matches)
        match = Match(
            tournament_id=tournament_id,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            home_score=None,
            away_score=None,
            played_at=current_time
        )

        session.add(match)
        match_count += 1
        current_time += timedelta(minutes=10)

    session.commit()
    print(f"🏒 Added {match_count} matches (every 10 minutes until 23:00)")
