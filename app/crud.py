from typing import List
from datetime import datetime
from sqlmodel import select
from sqlmodel import Session

from .models import Team, Tournament, Match


def get_teams(session: Session) -> List[Team]:
    return session.exec(select(Team)).all()


def get_team(session: Session, team_id: int) -> Team | None:
    return session.get(Team, team_id)


def get_tournaments(session: Session):
    return session.exec(select(Tournament)).all()


def get_tournament(session: Session, tournament_id: int):
    return session.get(Tournament, tournament_id)


def _apply_live_scores(match: Match) -> Match:
    """Apply live scores to all matches of the day."""
    now = datetime.now()

    # Apply live scores to all matches scheduled for today
    if match.played_at and match.played_at.date() == now.date():
        match.home_score = now.hour  # Hours (0-23)
        match.away_score = now.minute  # Minutes (0-59)

    return match


def get_matches(session: Session):
    matches = session.exec(select(Match)).all()
    return [_apply_live_scores(m) for m in matches]


def get_match(session: Session, match_id: int):
    match = session.get(Match, match_id)
    if match:
        return _apply_live_scores(match)
    return None


def get_matches_for_tournament(session: Session, tournament_id: int):
    stmt = select(Match).where(Match.tournament_id == tournament_id)
    matches = session.exec(stmt).all()
    return [_apply_live_scores(m) for m in matches]
