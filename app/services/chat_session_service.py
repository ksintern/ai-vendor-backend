from typing import Optional

from sqlalchemy.orm import Session

from app.models.chat_session import ChatSession


class ChatSessionService:

    @staticmethod
    def create_session(

        db: Session,

        user_id,

        session_id,

        context_data=None,

        missing_fields=None,

        current_question=None,

        detected_intent=None

    ):

        session = ChatSession(

            session_id=session_id,

            user_id=user_id,

            status="ACTIVE",

            context_data=context_data or {},

            missing_fields=missing_fields or [],

            current_question=current_question,

            detected_intent=detected_intent

        )

        db.add(session)

        db.commit()

        db.refresh(session)

        return session

    @staticmethod
    def get_session(

        db: Session,

        session_id

    ) -> Optional[ChatSession]:

        return (

            db.query(

                ChatSession

            )
            .filter(

                ChatSession.session_id
                == session_id

            )
            .first()

        )

    @staticmethod
    def update_session(

        db: Session,

        session_id,

        context_data=None,

        missing_fields=None,

        current_question=None,

        detected_intent=None,

        status=None

    ):

        session = (

            ChatSessionService
            .get_session(

                db,

                session_id

            )

        )

        if not session:

            return None

        if context_data is not None:

            session.context_data = context_data

        if missing_fields is not None:

            session.missing_fields = missing_fields

        if current_question is not None:

            session.current_question = current_question

        if detected_intent is not None:

            session.detected_intent = detected_intent

        if status is not None:

            session.status = status

        db.commit()

        db.refresh(session)

        return session

    @staticmethod
    def mark_completed(

        db: Session,

        session_id

    ):

        session = (

            ChatSessionService
            .get_session(

                db,

                session_id

            )

        )

        if not session:

            return None

        session.status = "COMPLETED"

        session.current_question = None

        session.missing_fields = []

        db.commit()

        db.refresh(session)

        return session