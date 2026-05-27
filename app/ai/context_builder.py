class ContextBuilder:

    MAX_VENDORS = 5
    MAX_CATEGORIES = 10

    @staticmethod
    def _safe_value(value, default="N/A"):

        if value is None:
            return default

        if isinstance(value, str):

            cleaned = value.strip()

            if not cleaned:
                return default

            return cleaned

        return value

    @staticmethod
    def _serialize_vendor(vendor):

        rating = getattr(
            vendor,
            "avg_rating",
            0
        )

        return {
            "name": ContextBuilder._safe_value(
                getattr(
                    vendor,
                    "name",
                    None
                )
            ),

            "city": ContextBuilder._safe_value(
                getattr(
                    vendor,
                    "city",
                    None
                )
            ),

            "price_min": getattr(
                vendor,
                "price_min",
                0
            ),

            "price_max": getattr(
                vendor,
                "price_max",
                0
            ),

            "rating": round(
                float(rating or 0),
                1
            ),

            "category": ContextBuilder._safe_value(
                getattr(
                    vendor,
                    "category",
                    None
                )
            )
        }

    @staticmethod
    def build(context: dict):

        recommendations = (

            context
            .get(
                "recommendations",
                {}
            )
            .get(
                "recommendations",
                {}
            )

        )

        vendors = (

            recommendations
            .get(
                "vendors",
                []
            )

        )[:ContextBuilder.MAX_VENDORS]

        serialized_vendors = [

            ContextBuilder._serialize_vendor(
                vendor
            )

            for vendor in vendors

        ]

        categories = (

            context
            .get(
                "context",
                {}
            )
            .get(
                "categories",
                []

            )

        )[:ContextBuilder.MAX_CATEGORIES]

        category_names = [

            str(

                getattr(
                    category,
                    "name",
                    category
                )

            )

            for category in categories

        ]

        llm_context = {

            "STRICT_DB_RESULTS":

            serialized_vendors,

            "AVAILABLE_CATEGORIES":

            category_names,

            "RULES": [

                "ONLY use vendors from STRICT_DB_RESULTS",

                "DO NOT create vendor names",

                "DO NOT infer missing vendors",

                "If STRICT_DB_RESULTS empty say no vendors found",

                "Vendor cards rendered by frontend"

            ]

        }

        return str(
            llm_context
        )