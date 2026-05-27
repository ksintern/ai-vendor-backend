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

from app.ai.query_parser import (
    QueryParser
)

from app.ai.data_orchestrator import (
    DataOrchestrator
)

from app.ai.context_builder import (
    ContextBuilder
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
        "Hello. How can I help with your event planning today?",

        "hello":
        "Hello. Tell me what kind of vendor you're looking for.",

        "hey":
        "Hey. What can I help you find today?"

    }

    MAX_VENDOR_CARDS = 3

    FOLLOWUP_QUESTIONS = {

        "city":[

            "Sure. Which city should I look in?",

            "Got it. Which city is your event in?"

        ],

        "budget":[

            "Got it. What's your approximate budget?",

            "Okay. What's your budget range?"

        ],

        "guest_count":[

            "Perfect. Around how many guests are expected?",

            "Okay. Roughly how many guests are you planning for?"

        ],

        "cuisine":[

            "Any preferred cuisine?"

        ],

        "event_type":[

            "What's the event type?"

        ]

    }

    ACKNOWLEDGEMENTS=[

        "Got it.",

        "Perfect.",

        "Okay.",

        "Sounds good."

    ]

    def __init__(

        self,

        db:Session

    ):

        self.db=db

        self.ai_service=AIService()

    async def process_message(

        self,

        payload:ChatRequest

    ):

        session_id=(

            payload.session_id

            or

            str(

                uuid.uuid4()

            )

        )

        try:

            user_message=(

                payload.message

                .strip()

            )

            lower=(

                user_message

                .lower()

            )

            if lower in self.QUICK_REPLIES:

                return {

                    "success":True,

                    "message":

                    self.QUICK_REPLIES[

                        lower

                    ],

                    "session_id":

                    session_id,

                    "recommendations":[],

                    "error":None

                }

            SessionManager.add_message(

                session_id,

                "user",

                user_message

            )

            previous_filters=(

                SessionManager

                .get_filters(

                    session_id

                )

            )

            extracted=(

                QueryParser

                .extract_filters(

                    user_message,

                    previous_filters

                )

            )

            SessionManager.set_filters(

                session_id,

                extracted

            )

            filters={

                k:v

                for k,v

                in extracted.items()

                if v is not None

            }

            missing=(

                self._find_missing_field(

                    filters

                )

            )

            recommendations=[]

            assistant=""

            if not missing:

                intent=(

                    IntentExtractor

                    .extract(

                        user_message

                    )

                    .get(

                        "intent",

                        "vendor_recommendation"

                    )

                )

                context=(

                    DataOrchestrator

                    .fetch_context(

                        self.db,

                        intent,

                        filters

                    )

                )

                recommendations=(

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

                if recommendations:

                    assistant=(

                        "Perfect. I found vendor options matching your requirements."

                    )

                else:

                    assistant=(

                        "Sorry, I couldn't find matching vendors."

                    )

            else:

                acknowledgement=(

                    self._acknowledge(

                        filters

                    )

                )

                question=(

                    self.FOLLOWUP_QUESTIONS[
                        missing
                    ][0]

                )

                assistant=(

                    f"{acknowledgement} {question}"

                    .strip()

                )

            SessionManager.add_message(

                session_id,

                "assistant",

                assistant

            )

            cards=[

                self._vendor_card(

                    vendor

                )

                for vendor

                in recommendations[
                    :self.MAX_VENDOR_CARDS
                ]

            ]

            return {

                "success":True,

                "message":

                assistant,

                "session_id":

                session_id,

                "recommendations":

                cards,

                "error":None

            }

        except Exception as e:

            return {

                "success":False,

                "message":"",

                "session_id":

                session_id,

                "recommendations":[],

                "error":

                str(e)

            }

    def _acknowledge(

        self,

        filters

    ):

        count=len(

            filters

        )

        if count<=1:

            return ""

        if count==2:

            return "Got it."

        if count==3:

            return "Perfect."

        return "Sounds good."

    def _find_missing_field(

        self,

        filters

    ):

        category=(

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