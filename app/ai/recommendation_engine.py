from sqlalchemy.orm import (
    Session
)


class RecommendationEngine:

    MAX_RESULTS = 5

    @staticmethod
    def calculate_budget_fit_score(

        vendor,

        budget

    ):
        
        try:
            budget = int(budget) if budget is not None else None
        except (ValueError, TypeError):
            budget = None

        if not budget:
            return 25

        min_price = getattr(vendor, "price_min", 0) or 0
        max_price = getattr(vendor, "price_max", 0) or 0

        if not min_price or not max_price:
            return 10

        if min_price <= budget <= max_price:
            return 50

        if max_price <= budget:
            return 40

        if min_price <= budget:
            return 25

        return 0


    @staticmethod
    def calculate_quality_score(

        vendor

    ):

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

        # New vendor protection
        if reviews == 0:

            return 15

        rating_score = (

            rating / 5

        ) * 20

        if reviews >= 200:

            confidence_bonus = 10

        elif reviews >= 100:

            confidence_bonus = 7
        
        elif reviews >= 50:

            confidence_bonus = 5

        elif reviews >= 20:

            confidence_bonus = 3

        else:

            confidence_bonus = 0

        
        return (

            rating_score
            +
            confidence_bonus

        )


    @staticmethod
    def calculate_trust_score(

        vendor

    ):

        if getattr(

            vendor,

            "is_verified",

            False

        ):

            return 10

        return 0


    @staticmethod
    def calculate_activity_score(

        vendor

    ):

        followers = getattr(

            vendor,

            "followers_count",

            0

        ) or 0

        views = getattr(

            vendor,

            "profile_views",

            0

        ) or 0

        engagement = getattr(

            vendor,

            "engagement_score",

            0

        ) or 0

        followers_score = min(

            followers,

            100

        ) * 0.02

        views_score = min(

            views,

            1000

        ) * 0.002

        engagement_score = min(

            engagement,

            100

        ) * 0.05

        return (

            followers_score
            +
            views_score
            +
            engagement_score

        )


    @staticmethod
    def calculate_vendor_score(

        vendor,

        filters

    ):

        budget = filters.get(

            "budget"

        )

        budget_score = (

            RecommendationEngine

            .calculate_budget_fit_score(

                vendor,

                budget

            )

        )

        quality_score = (

            RecommendationEngine

            .calculate_quality_score(

                vendor

            )

        )

        trust_score = (

            RecommendationEngine

            .calculate_trust_score(

                vendor

            )

        )

        activity_score = (

            RecommendationEngine

            .calculate_activity_score(

                vendor

            )

        )

        return (

            budget_score
            +
            quality_score
            +
            trust_score
            +
            activity_score

        )

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
    def rank_vendors(vendors, filters):
    # Fix 3: Exclude root/parent vendors from ranking
        rankable = [
            v for v in vendors
            if getattr(v, "parent_vendor_id", None) is not None
        ]

        if not rankable:
            rankable = vendors  # fallback if filter removes everything

    # Fix 2: Isolate per-vendor scoring so one bad vendor never kills the sort
        def safe_score(vendor):
            try:
                return RecommendationEngine.calculate_vendor_score(vendor, filters)
            except Exception as e:
                print(f"SCORING ERROR for vendor '{getattr(vendor, 'name', '?')}': {e}")
                return 0

        ranked = sorted(rankable, key=safe_score, reverse=True)

        print("RANKED VENDORS:", [v.name for v in ranked])

        return ranked[:RecommendationEngine.MAX_RESULTS]