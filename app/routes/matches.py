from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..db import get_session
from ..crud import get_matches, get_match, get_matches_for_tournament

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("", response_model=list)
def list_matches(session: Session = Depends(get_session)):
    return get_matches(session)


@router.get("/{match_id}")
def read_match(match_id: int, session: Session = Depends(get_session)):
    m = get_match(session, match_id)
    if not m:
        raise HTTPException(status_code=404, detail="Match not found")
    return m


@router.get("/tournament/{tournament_id}")
def read_matches_for_tournament(tournament_id: int, session: Session = Depends(get_session)):
    return get_matches_for_tournament(session, tournament_id)
