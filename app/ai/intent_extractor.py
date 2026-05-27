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

    SERVICE = {

        "service",
        "services",
        "provide",
        "provides",
        "offering",
        "offer"

    }

    COMPARE_PATTERNS=[

        r"\bcompare\b",

        r"\bvs\b",

        r"\bversus\b",

        r"\bbetter\b",

        r"\bdifference\b"

    ]

    @staticmethod
    def extract(

        query:str

    ):

        query_lower=(

            query
            .lower()
            .strip()

        )

        filters=(

            QueryParser
            .extract_filters(

                query

            )

        )

        vendor_names=(

            IntentExtractor
            ._extract_vendor_names(

                query

            )

        )

        if len(

            vendor_names

        )>=2:

            filters[

                "comparison_request"

            ]=True

            filters[

                "vendor_names"

            ]=vendor_names

        tokens=set(

            re.findall(

                r"\w+",

                query_lower

            )

        )

        intent=(

            IntentExtractor
            .detect_intent(

                query_lower,

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

        query:str,

        tokens:set,

        filters:dict

    ):

        if filters.get(

            "service_request"

        ):

            return (

                "service_query"

            )

        if filters.get(

            "comparison_request"

        ):

            return (

                "comparison_query"

            )

        for pattern in (

            IntentExtractor
            .COMPARE_PATTERNS

        ):

            if re.search(

                pattern,

                query

            ):

                return (

                    "comparison_query"

                )

        intent_priority=[

            (

                IntentExtractor.SERVICE,

                "service_query"

            ),

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

                "cuisine",

                "event_type"

            ]

        ):

            return (

                "vendor_recommendation"

            )

        return (

            "generic_platform_query"

        )

    @staticmethod
    def _extract_vendor_names(

        query:str

    ):

        lowered=(

            query.lower()

        )

        separators=[

            " vs ",

            " versus ",

            " and "

        ]

        for separator in separators:

            if separator in lowered:

                pieces=[

                    item.strip()

                    for item

                    in lowered.split(

                        separator

                    )

                ]

                cleaned=[]

                for piece in pieces:

                    piece=re.sub(

                        r"\b(compare|better|difference|between|which|is|vendor)\b",

                        "",

                        piece

                    )

                    piece=piece.strip()

                    if piece:

                        cleaned.append(

                            piece

                        )

                return cleaned

        return []