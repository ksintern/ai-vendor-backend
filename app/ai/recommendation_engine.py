from sqlalchemy.orm import (
    Session
)


class RecommendationEngine:

    MAX_RESULTS = 5


    @staticmethod
    def get_recommendations(

        db: Session,

        context: dict,

        filters: dict

    ):

        recommendations = {}

        vendors = (

            context.get(

                "vendors",

                []

            )

        )

        if vendors:

            recommendations[

                "vendors"

            ] = (

                RecommendationEngine

                .rank_vendors(

                    vendors,

                    filters

                )

            )

        categories = (

            context.get(

                "categories",

                []

            )

        )

        if categories:

            recommendations[

                "categories"

            ] = categories[:10]

        return {

            "recommendations":

            recommendations,

            "metadata": {

                "total_vendors":

                len(

                    recommendations.get(

                        "vendors",

                        []

                    )

                )

            }

        }


    @staticmethod
    def rank_vendors(

        vendors,

        filters

    ):

        budget = (

            filters.get(

                "budget"

            )

        )

        city = (

            filters.get(

                "city"

            )

        )

        category = (

            filters.get(

                "category"

            )

        )


        def score(

            vendor

        ):

            total = 0

            rating = getattr(

                vendor,

                "avg_rating",

                0

            ) or 0

            reviews = getattr(

                vendor,

                "review_count",

                0

            ) or 0

            min_price = getattr(

                vendor,

                "price_min",

                0

            ) or 0

            vendor_city = (

                getattr(

                    vendor,

                    "city",

                    ""

                )

                or

                ""

            )

            vendor_category = (

                getattr(

                    vendor,

                    "category",

                    ""

                )

                or

                ""

            )

            total += rating * 10

            total += min(

                reviews,

                20

            )

            if (

                budget

                and

                min_price

                and

                min_price <= budget

            ):

                total += 20

            if (

                city

                and

                city.lower()

                in

                vendor_city.lower()

            ):

                total += 10

            if (

                category

                and

                category.lower()

                in

                vendor_category.lower()

            ):

                total += 10

            return total


        ranked = sorted(

            vendors,

            key=score,

            reverse=True

        )

        return ranked[

            :

            RecommendationEngine

            .MAX_RESULTS

        ]