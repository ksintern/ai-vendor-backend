import re

from app.ai.query_parser import (
    QueryParser
)


class IntentExtractor:

    COMPARISON = {

        "compare",

        "comparison",

        "difference",

        "better",

        "vs",

        "versus"

    }

    PRICING = {

        "price",

        "pricing",

        "budget",

        "cheap",

        "premium",

        "luxury",

        "cost",

        "affordable"

    }

    CATEGORY = {

        "category",

        "categories"

    }

    REVIEW = {

        "rating",

        "review",

        "reviews",

        "best",

        "top"

    }

    AVAILABILITY = {

        "available",

        "availability"

    }

    ANALYTICS = {

        "analytics",

        "trend",

        "statistics",

        "insights"

    }

    SAVED = {

        "saved",

        "wishlist",

        "bookmark"

    }

    @staticmethod
    def extract(

        query:str

    ):

        query_lower=(

            query
            .lower()
            .strip()

        )

        tokens=set(

            re.findall(

                r"\w+",

                query_lower

            )

        )

        filters=(

            QueryParser
            .extract_filters(

                query

            )

        )

        intent=(

            IntentExtractor
            .detect_intent(

                tokens,

                filters

            )

        )

        return {

            "intent":

            intent,

            "filters":

            filters

        }

    @staticmethod
    def detect_intent(

        tokens:set,

        filters:dict

    ):

        if (

            filters.get(

                "comparison_request"

            )

        ):

            return (

                "comparison_query"

            )

        intent_priority=[

            (

                IntentExtractor.COMPARISON,

                "comparison_query"

            ),

            (

                IntentExtractor.PRICING,

                "pricing_query"

            ),

            (

                IntentExtractor.CATEGORY,

                "category_query"

            ),

            (

                IntentExtractor.REVIEW,

                "review_query"

            ),

            (

                IntentExtractor.AVAILABILITY,

                "availability_query"

            ),

            (

                IntentExtractor.ANALYTICS,

                "analytics_query"

            ),

            (

                IntentExtractor.SAVED,

                "saved_vendor_query"

            )

        ]

        for keywords,intent in (

            intent_priority

        ):

            if tokens & keywords:

                return intent

        if any(

            filters.get(

                field

            )

            for field in [

                "category",

                "budget",

                "city",

                "guest_count",

                "cuisine"

            ]

        ):

            return (

                "vendor_recommendation"

            )

        return (

            "generic_platform_query"

        )