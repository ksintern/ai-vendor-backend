import uuid

from sqlalchemy.orm import Session

from app.ai.ai_service import AIService
from app.ai.intent_extractor import IntentExtractor
from app.ai.data_orchestrator import DataOrchestrator
from app.ai.session_manager import SessionManager
from app.ai.followup_generator import FollowUpGenerator
from app.ai.conversation_orchestrator import ConversationOrchestrator
from app.services.chat_session_service import ChatSessionService

from app.schemas.chat_schema import ChatRequest


class ChatService:

    QUICK_REPLIES = {
        "hi": "Hello 👋 Tell me your event requirements and I'll help find vendors.",
        "hello": "Hello 👋 Tell me what vendor you're looking for.",
        "hey": "Hey 👋 What can I help you find today?"
    }

    SERVICE_TERMS = {
        "service",
        "services",
        "provide",
        "provides",
        "offering",
        "offer",
        "other",
        "else"
    }

    REFINEMENT_TERMS = {
        "luxury",
        "premium",
        "cheap",
        "budget",
        "affordable"
    }

    MAX_VENDOR_CARDS = 3

    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()

    async def process_message(self, payload: ChatRequest):

        session_id = payload.session_id or str(uuid.uuid4())

        # -----------------------------------
        # PERSISTENT CHAT SESSION
        # -----------------------------------

        db_session = ChatSessionService.get_session(
            self.db,
            session_id
        )

        if not db_session:

            ChatSessionService.create_session(
                db=self.db,
                user_id=None,
                session_id=session_id
            )

        try:
            user_message = payload.message.strip()
            lower = user_message.lower()

            # -----------------------------------
            # QUICK REPLIES
            # -----------------------------------

            if lower in self.QUICK_REPLIES:
                return {
                    "success": True,
                    "message": self.QUICK_REPLIES[lower],
                    "session_id": session_id,
                    "response_type": "chat",
                    "recommendations": [],
                    "error": None
                }

            # -----------------------------------
            # STORE USER MESSAGE
            # -----------------------------------

            SessionManager.add_message(
                session_id,
                "user",
                user_message
            )

            previous = SessionManager.get_filters(session_id)

            remembered = SessionManager.get_vendor_memory(session_id)

            # -----------------------------------
            # SERVICE REQUEST FLOW
            # -----------------------------------

            service_request = any(
                term in lower
                for term in self.SERVICE_TERMS
            )

            if remembered and service_request:

                assistant = self._service_reply(remembered)

                return {
                    "success": True,
                    "message": assistant,
                    "session_id": session_id,
                    "response_type": "chat",
                    "recommendations": [
                        self._vendor_card(vendor)
                        for vendor in remembered[:self.MAX_VENDOR_CARDS]
                    ],
                    "error": None
                }

            # -----------------------------------
            # STRUCTURED EXTRACTION
            # -----------------------------------

            try:
                structured = await self.ai_service.build_structured_response(
                    user_message,
                    previous
                )

            except Exception:
                structured = {
                    "filters": previous or {},
                    "intent": "vendor_recommendation",
                    "missing_fields": []
                }

            filters = structured.get("filters", {})
            intent = structured.get("intent")

            filters = {
                k: v
                for k, v in filters.items()
                if v is not None
            }

            SessionManager.set_filters(
                session_id,
                filters
            )

            # -----------------------------------
            # REFINEMENT FLOW
            # -----------------------------------

            refinement = any(
                word in lower
                for word in self.REFINEMENT_TERMS
            )

            if refinement and previous:
                filters = {
                    **previous,
                    **filters
                }

            # -----------------------------------
            # MISSING FIELD DETECTION
            # -----------------------------------

            missing = structured.get(
                "missing_fields",
                []
            )

            if missing:
                missing = missing[0]
            else:
                missing = self._find_missing(filters)

            recommendations = []

            # -----------------------------------
            # FOLLOWUP FLOW
            # -----------------------------------

            if missing:

                missing_fields = (
                    [missing]
                    if isinstance(missing, str)
                    else missing
                )

                session_state = (
                    ConversationOrchestrator.build_session_state(
                        filters=filters,
                        missing_fields=missing_fields,
                        intent=intent
                    )
                )

                assistant = (
                    session_state.get("current_question")
                    or "Could you provide more details?"
                )

                ChatSessionService.update_session(
                    db=self.db,
                    session_id=session_id,
                    context_data=filters,
                    missing_fields=missing_fields,
                    current_question=assistant,
                    detected_intent=intent,
                    status="ACTIVE"
                )

                response_type = "followup"

            else:

                response_type = "recommendation"

                # -----------------------------------
                # FALLBACK INTENT
                # -----------------------------------

                if not intent:
                    intent = (
                        IntentExtractor.extract(user_message)
                        .get(
                            "intent",
                            "vendor_recommendation"
                        )
                    )

                # -----------------------------------
                # DATABASE CONTEXT
                # -----------------------------------

                print(
                    "FINAL FILTERS:",
                    filters
                )
                
                context = DataOrchestrator.fetch_context(
                    self.db,
                    intent,
                    filters
                )

                recommendations = (
                    context.get(
                        "recommendations",
                        {}
                    ).get(
                        "vendors",
                        []
                    )
                )

                print(
                    "FOUND VENDORS:",
                    len(recommendations)
                )

                # -----------------------------------
                # RECOMMENDATION FLOW
                # -----------------------------------

                if recommendations:

                    SessionManager.set_vendor_memory(
                        session_id,
                        recommendations
                    )

                    ChatSessionService.mark_completed(
                        self.db,
                        session_id
                    )

                    assistant = (
                        "Perfect. I found vendor options matching your requirements."
                    )

                else:

                    ChatSessionService.update_session(
                        db=self.db,
                        session_id=session_id,
                        context_data=filters,
                        detected_intent=intent,
                        status="ACTIVE"
                    )

                    assistant = (
                        "Sorry, I couldn't find matching vendors."
                    )

            # -----------------------------------
            # STORE ASSISTANT MESSAGE
            # -----------------------------------

            SessionManager.add_message(
                session_id,
                "assistant",
                assistant
            )

            # -----------------------------------
            # FINAL RESPONSE
            # -----------------------------------

            return {
                "success": True,
                "message": assistant,
                "session_id": session_id,
                "response_type": response_type,
                "current_question": (
                    assistant
                    if response_type == "followup"
                    else None
                ),
                "missing_fields": (
                    missing_fields
                    if response_type == "followup"
                    else []
                ),
                "recommendations": [
                    self._vendor_card(vendor)
                    for vendor in recommendations[:self.MAX_VENDOR_CARDS]
                ],
                "error": None
            }

        except Exception as e:

            print(
                "CHAT ERROR:",
                str(e)
            )

            return {
                "success": False,
                "message": "",
                "session_id": session_id,
                "response_type": "error",
                "recommendations": [],
                "error": str(e)
            }

    def _service_reply(self, vendors):

        vendor = vendors[0]

        sections = []

        teams = (
            getattr(
                vendor,
                "managed_teams",
                []
            )
            or []
        )

        for team in teams:

            category_name = getattr(
                team,
                "name",
                ""
            )

            service_names = [
                service.service_name
                for service in getattr(
                    team,
                    "service_records",
                    []
                )
                if getattr(
                    service,
                    "service_name",
                    None
                )
            ]

            if service_names:

                sections.append(
                    f"{category_name}: "
                    + ", ".join(service_names)
                )

            elif category_name:

                sections.append(
                    category_name
                )

        if not sections:
            return "No service information available."

        return (
            f"{vendor.name} provides:\n\n"
            + "\n".join(sections)
        )

    def _find_missing(self, filters):

        category = filters.get("category")

        if not category:
            return None

        if not filters.get("city"):
            return "city"

        if category == "catering":

            if not filters.get("budget"):
                return "budget"

            if not filters.get("guest_count"):
                return "guest_count"

        return None

    def _vendor_card(self, vendor):

        return {
            "vendor_id": str(vendor.vendor_id),
            "name": vendor.name,
            "city": vendor.city,
            "rating": getattr(
                vendor,
                "avg_rating",
                0
            ),
            "price_min": vendor.price_min,
            "price_max": vendor.price_max
        }