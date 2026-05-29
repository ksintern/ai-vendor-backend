from typing import Dict
from typing import Any
from typing import Optional


class StructuredResponseBuilder:

    DEFAULT_STRUCTURE = {

        "intent": "vendor_recommendation",

        "filters": {},

        "missing_fields": [],

        "confidence": 0.0

    }

    @classmethod
    def build(

        cls,

        parser_filters: Dict[str, Any],

        llm_filters: Optional[Dict[str, Any]],

        intent: str,

        confidence: float

    ) -> Dict[str, Any]:

        final_filters = {

            **parser_filters

        }

        if llm_filters:

            for key, value in llm_filters.items():

                if (

                    value is not None

                    and

                    value != ""

                ):

                    final_filters[key] = value

        missing = cls._find_missing(

            final_filters

        )

        return {

            "intent":

            intent,

            "filters":

            final_filters,

            "missing_fields":

            missing,

            "confidence":

            round(

                confidence,

                2

            )

        }

    @staticmethod
    def _find_missing(

        filters

    ):

        missing = []

        category = (

            filters.get(

                "category"

            )

        )

        if not category:

            missing.append(

                "category"

            )

            return missing

        if not filters.get(

            "city"

        ):

            missing.append(

                "city"

            )

        if (

            category

            ==

            "catering"

        ):

            if not filters.get(

                "budget"

            ):

                missing.append(

                    "budget"

                )

            if not filters.get(

                "guest_count"

            ):

                missing.append(

                    "guest_count"

                )

        return missing