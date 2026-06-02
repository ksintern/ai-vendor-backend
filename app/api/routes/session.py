from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.api.dependencies.auth_dependency import (
    get_current_user
)

from app.models.user import User

from app.services.chat_session_service import (
    ChatSessionService
)

from app.services.conversation_service import (
    ConversationService
)

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)


@router.get("/{session_id}")
def get_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    session = ChatSessionService.get_session(
        db,
        session_id
    )

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return session


@router.get("/{session_id}/history")
def get_session_history(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    history = (
        ConversationService.get_session_history(
            db,
            session_id
        )
    )

    return history


@router.get("/{session_id}/context")
def get_session_context(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    context = (
        ConversationService.build_context_summary(
            db,
            session_id
        )
    )

    return {
        "session_id": session_id,
        "context": context
    }