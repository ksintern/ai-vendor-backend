from sqlalchemy.orm import (
    Session
)

from app.repositories import (

    vendor_repository,

    category_repository

)

from app.ai.recommendation_engine import (

    RecommendationEngine

)


class DataOrchestrator:

    MAX_VENDORS = 5

    MAX_CATEGORIES = 10

    LIGHT_INTENTS = {

        "generic_platform_query"

    }

    RECOMMENDATION_INTENTS = {

        "vendor_search",

        "vendor_recommendation",

        "pricing_query",

        "comparison_query",

        "review_query"

    }

    @staticmethod
    def fetch_context(

        db: Session,

        intent: str,

        filters: dict

    ):

        if (

            intent

            in

            DataOrchestrator.LIGHT_INTENTS

        ):

            return (

                DataOrchestrator
                ._empty(

                    intent

                )

            )

        handlers = {

            "vendor_search":

            DataOrchestrator.vendor_context,

            "vendor_recommendation":

            DataOrchestrator.vendor_context,

            "pricing_query":

            DataOrchestrator.pricing_context,

            "comparison_query":

            DataOrchestrator.comparison_context,

            "review_query":

            DataOrchestrator.review_context,

            "analytics_query":

            DataOrchestrator.analytics_context,

            "category_query":

            DataOrchestrator.category_context

        }

        try:

            handler = (

                handlers.get(

                    intent,

                    DataOrchestrator
                    .generic_context

                )

            )

            raw_context = (

                handler(

                    db,

                    filters

                )

            )

        except Exception:

            raw_context = {}

        recommendations = {}

        if (

            intent

            in

            DataOrchestrator
            .RECOMMENDATION_INTENTS

            and

            raw_context

        ):

            try:

                recommendations = (

                    RecommendationEngine
                    .get_recommendations(

                        db,

                        raw_context,

                        filters

                    )

                )

            except Exception:

                recommendations = {}

        return {

            "intent":

            intent,

            "context":

            raw_context,

            "recommendations":

            recommendations

        }

    @staticmethod
    def vendor_context(

        db,

        filters

    ):

        result = (

            vendor_repository
            .search_vendors_ai(

                db,

                filters

            )

        )

        vendors = (

            result.get(

                "vendors",

                []

            )

        )

        return {

            "vendors":

            vendors[

                :DataOrchestrator
                .MAX_VENDORS

            ]

        }

    @staticmethod
    def pricing_context(

        db,

        filters

    ):

        budget = (

            filters.get(

                "budget"

            )

        )

        if not budget:

            return {}

        return {

            "vendors":

            vendor_repository
            .budget_vendors_ai(

                db,

                budget

            )[

                :DataOrchestrator
                .MAX_VENDORS

            ]

        }

    @staticmethod
    def comparison_context(

        db,

        filters

    ):

        names = (

            filters.get(

                "vendor_names",

                []

            )

        )

        if not names:

            return {}

        return {

            "vendors":

            vendor_repository
            .compare_vendors_ai(

                db,

                names

            )

        }

    @staticmethod
    def review_context(

        db,

        filters

    ):

        return {

            "vendors":

            vendor_repository
            .top_rated_vendors_ai(

                db

            )[

                :DataOrchestrator
                .MAX_VENDORS

            ]

        }

    @staticmethod
    def analytics_context(

        db,

        filters

    ):

        return {

            "analytics":

            vendor_repository
            .vendor_analytics_ai(

                db

            )

        }

    @staticmethod
    def category_context(

        db,

        filters

    ):

        return {

            "categories":

            category_repository
            .get_all_categories(

                db

            )[

                :DataOrchestrator
                .MAX_CATEGORIES

            ]

        }

    @staticmethod
    def generic_context(

        db,

        filters

    ):

        return {}

    @staticmethod
    def _empty(

        intent

    ):

        return {

            "intent":

            intent,

            "context": {},

            "recommendations": {}

        }