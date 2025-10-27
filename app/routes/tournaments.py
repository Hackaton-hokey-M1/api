from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..db import get_session
from ..crud import get_tournaments, get_tournament

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


@router.get("", response_model=list)
def list_tournaments(session: Session = Depends(get_session)):
    return get_tournaments(session)


@router.get("/{tournament_id}")
def read_tournament(tournament_id: int, session: Session = Depends(get_session)):
    t = get_tournament(session, tournament_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return t
