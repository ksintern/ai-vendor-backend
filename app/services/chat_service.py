import uuid

from sqlalchemy.orm import (
    Session
)

from app.ai.ai_service import (
    AIService
)

from app.ai.intent_extractor import (
    IntentExtractor
)

from app.ai.data_orchestrator import (
    DataOrchestrator
)

from app.ai.session_manager import (
    SessionManager
)

from app.schemas.chat_schema import (
    ChatRequest
)


class ChatService:

    QUICK_REPLIES = {

        "hi":
        "Hello 👋 Tell me your event requirements and I'll help find vendors.",

        "hello":
        "Hello 👋 Tell me what vendor you're looking for.",

        "hey":
        "Hey 👋 What can I help you find today?"

    }

    FOLLOWUP_QUESTIONS = {

        "city":
        "Sure. Which city should I look in?",

        "budget":
        "What's your approximate budget?",

        "guest_count":
        "Around how many guests are expected?"

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

    def __init__(

        self,

        db: Session

    ):

        self.db = db

        self.ai_service = AIService()

    async def process_message(

        self,

        payload: ChatRequest

    ):

        session_id = (

            payload.session_id

            or

            str(

                uuid.uuid4()

            )

        )

        try:

            user_message = (

                payload.message
                .strip()

            )

            lower = (

                user_message
                .lower()

            )

            # -----------------------------------
            # QUICK REPLIES
            # -----------------------------------

            if lower in self.QUICK_REPLIES:

                return {

                    "success": True,

                    "message":
                    self.QUICK_REPLIES[
                        lower
                    ],

                    "session_id":
                    session_id,

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

            previous = (

                SessionManager
                .get_filters(

                    session_id

                )

            )

            remembered = (

                SessionManager
                .get_vendor_memory(

                    session_id

                )

            )

            # -----------------------------------
            # SERVICE REQUEST FLOW
            # -----------------------------------

            service_request = any(

                term in lower

                for term

                in self.SERVICE_TERMS

            )

            if (

                remembered

                and

                service_request

            ):

                assistant = (

                    self._service_reply(

                        remembered

                    )

                )

                return {

                    "success": True,

                    "message":
                    assistant,

                    "session_id":
                    session_id,

                    "recommendations": [

                        self._vendor_card(

                            vendor

                        )

                        for vendor

                        in remembered[
                            :self.MAX_VENDOR_CARDS
                        ]

                    ],

                    "error": None

                }

            # -----------------------------------
            # STRUCTURED EXTRACTION
            # -----------------------------------

            try:

                structured = (

                    await self.ai_service
                    .build_structured_response(

                        user_message,

                        previous

                    )

                )

            except Exception:

                structured = {

                    "filters":

                    previous or {},

                    "intent":

                    "vendor_recommendation",

                    "missing_fields": []

                }

            filters = (

                structured.get(

                    "filters",

                    {}

                )

            )

            intent = (

                structured.get(

                    "intent"

                )

            )

            filters = {

                k: v

                for k, v

                in filters.items()

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

                for word

                in self.REFINEMENT_TERMS

            )

            if (

                refinement

                and

                previous

            ):

                filters = {

                    **previous,

                    **filters

                }

            # -----------------------------------
            # MISSING FIELD DETECTION
            # -----------------------------------

            missing = (

                structured.get(

                    "missing_fields",

                    []

                )

            )

            if missing:

                missing = missing[0]

            else:

                missing = (

                    self._find_missing(

                        filters

                    )

                )

            recommendations = []

            # -----------------------------------
            # FOLLOWUP FLOW
            # -----------------------------------

            if missing:

                assistant = (

                    self.FOLLOWUP_QUESTIONS.get(

                        missing,

                        "Please provide more details."

                    )

                )

            else:

                # -----------------------------------
                # FALLBACK INTENT
                # -----------------------------------

                if not intent:

                    intent = (

                        IntentExtractor
                        .extract(

                            user_message

                        )
                        .get(

                            "intent",

                            "vendor_recommendation"

                        )

                    )

                # -----------------------------------
                # DATABASE CONTEXT
                # -----------------------------------

                context = (

                    DataOrchestrator
                    .fetch_context(

                        self.db,

                        intent,

                        filters

                    )

                )

                recommendations = (

                    context
                    .get(

                        "recommendations",

                        {}

                    )
                    .get(

                        "vendors",

                        []

                    )

                )

                print(

                    "FOUND VENDORS:",

                    len(

                        recommendations

                    )

                )

                # -----------------------------------
                # RECOMMENDATION FLOW
                # -----------------------------------

                if recommendations:

                    SessionManager.set_vendor_memory(

                        session_id,

                        recommendations

                    )

                    # IMPORTANT:
                    # Safe static response
                    # Avoids ModelScope 401 crash

                    assistant = (

                        "Perfect. I found vendor options matching your requirements."

                    )

                else:

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

                "message":
                assistant,

                "session_id":
                session_id,

                "recommendations": [

                    self._vendor_card(

                        vendor

                    )

                    for vendor

                    in recommendations[
                        :self.MAX_VENDOR_CARDS
                    ]

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

                "session_id":
                session_id,

                "recommendations": [],

                "error":
                str(e)

            }

    def _service_reply(

        self,

        vendors

    ):

        vendor = vendors[0]

        sections = []

        teams = (

            getattr(

                vendor,

                "managed_teams",

                []

            )

            or

            []

        )

        for team in teams:

            category_name = (

                getattr(

                    team,

                    "name",

                    ""

                )

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

                    +

                    ", ".join(

                        service_names

                    )

                )

            elif category_name:

                sections.append(

                    category_name

                )

        if not sections:

            return (

                "No service information available."

            )

        return (

            f"{vendor.name} provides:\n\n"

            +

            "\n".join(

                sections

            )

        )

    def _find_missing(

        self,

        filters

    ):

        category = (

            filters.get(

                "category"

            )

        )

        if not category:

            return None

        if not filters.get(

            "city"

        ):

            return "city"

        if (

            category

            ==

            "catering"

        ):

            if not filters.get(

                "budget"

            ):

                return "budget"

            if not filters.get(

                "guest_count"

            ):

                return "guest_count"

        return None

    def _vendor_card(

        self,

        vendor

    ):

        return {

            "vendor_id":
            str(

                vendor.vendor_id

            ),

            "name":
            vendor.name,

            "city":
            vendor.city,

            "rating":
            getattr(

                vendor,

                "avg_rating",

                0

            ),

            "price_min":
            vendor.price_min,

            "price_max":
            vendor.price_max

        }