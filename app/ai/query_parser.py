import re

from typing import (

    List,
    Optional,
    TypedDict

)


class QueryFilters(

    TypedDict,

    total=False

):

    category: Optional[str]

    budget: Optional[int]

    city: Optional[str]

    guest_count: Optional[int]

    cuisine: Optional[str]

    event_type: Optional[str]

    event_date: Optional[str]

    service_style: Optional[str]

    rating: Optional[float]

    vendor_names: List[str]

    comparison_request: bool

    pricing_preference: Optional[str]

    service_request: bool


class QueryParser:

    CATEGORY_PATTERNS = {

        "catering":[

            "catering",
            "caterer",
            "food"

        ],

        "photography":[

            "photography",
            "photographer",
            "photographers"

        ],

        "decoration":[

            "decoration",
            "decor",
            "decorator"

        ],

        "venue":[

            "venue",
            "banquet",
            "hall"

        ],

        "music":[

            "music",
            "dj",
            "band"

        ]

    }

    CITY_MAP = {

        "delhi":"delhi",

        "new delhi":"delhi",

        "mumbai":"mumbai",

        "bangalore":"bangalore",

        "noida":"noida",

        "gurgaon":"gurgaon",

        "greater noida":"greater noida"

    }

    CUISINES={

        "north indian",

        "south indian",

        "continental",

        "chinese",

        "italian",

        "mexican"

    }

    EVENTS={

        "wedding",

        "birthday",

        "corporate",

        "engagement",

        "conference",

        "party"

    }

    CHEAPER_TERMS={

        "cheap",

        "cheaper",

        "affordable",

        "budget"

    }

    PREMIUM_TERMS={

        "premium",

        "luxury"

    }

    SERVICE_TERMS={

        "service",

        "services",

        "provide",

        "provides",

        "offering",

        "offer"

    }

    COMPARISON_TERMS={

        "compare",

        "comparison",

        "versus",

        "vs",

        "better"

    }

    @staticmethod
    def extract_filters(

        query:str,

        previous:dict|None=None

    )->QueryFilters:

        filters=dict(

            previous or {}

        )

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

        category=(

            QueryParser
            ._extract_category(

                query_lower

            )

        )

        if category:

            filters["category"]=category

        city=(

            QueryParser
            ._extract_city(

                query_lower

            )

        )

        if city:

            filters["city"]=city

        budget=(

            QueryParser
            ._extract_budget(

                query_lower

            )

        )

        if budget:

            filters["budget"]=budget

        guests=(

            QueryParser
            ._extract_guest_count(

                query_lower,

                filters

            )

        )

        if guests:

            filters["guest_count"]=guests

        cuisine=next(

            (

                item

                for item

                in QueryParser.CUISINES

                if item in query_lower

            ),

            None

        )

        if cuisine:

            filters["cuisine"]=cuisine

        event=next(

            (

                item

                for item

                in QueryParser.EVENTS

                if item in query_lower

            ),

            None

        )

        if event:

            filters["event_type"]=event

        if any(

            term in query_lower

            for term

            in QueryParser.SERVICE_TERMS

        ):

            filters["service_request"]=True

        if any(

            term in tokens

            for term

            in QueryParser.COMPARISON_TERMS

        ):

            filters["comparison_request"]=True

        if any(

            term in query_lower

            for term

            in QueryParser.CHEAPER_TERMS

        ):

            filters[

                "pricing_preference"

            ]="budget"

        if any(

            term in query_lower

            for term

            in QueryParser.PREMIUM_TERMS

        ):

            filters[

                "pricing_preference"

            ]="premium"

        return filters

    @staticmethod
    def _extract_city(

        query:str

    ):

        for city,value in (

            QueryParser
            .CITY_MAP
            .items()

        ):

            if city in query:

                return value

        return None

    @staticmethod
    def _extract_category(

        query:str

    ):

        for category,terms in (

            QueryParser
            .CATEGORY_PATTERNS
            .items()

        ):

            if any(

                term in query

                for term in terms

            ):

                return category

        return None

    @staticmethod
    def _extract_budget(

        query:str

    ):

        lakh=re.search(

            r"(\d+(?:\.\d+)?)\s*lakh",

            query

        )

        if lakh:

            return int(

                float(

                    lakh.group(1)

                )

                *100000

            )

        k_format=re.search(

            r"(\d+)\s*k",

            query

        )

        if k_format:

            return (

                int(

                    k_format.group(1)

                )

                *1000

            )

        numbers=re.findall(

            r"\d{4,7}",

            query

        )

        for number in numbers:

            value=int(number)

            if value>1000:

                return value

        return None

    @staticmethod
    def _extract_guest_count(

        query:str,

        filters:dict

    ):

        explicit=re.search(

            r"(\d+)\s*(guest|guests|people|persons)",

            query

        )

        if explicit:

            return int(

                explicit.group(1)

            )

        numbers=re.findall(

            r"\d+",

            query

        )

        budget=(

            filters.get(

                "budget"

            )

        )

        for number in numbers:

            value=int(number)

            if (

                1

                <=

                value

                <=

                1000

            ):

                if (

                    budget

                    and

                    value==budget

                ):

                    continue

                return value

        return None