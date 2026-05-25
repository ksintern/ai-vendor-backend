class FallbackHandler:

    @staticmethod
    def get_fallback_response():

        return {

            "success": False,

            "response": None,

            "error": (

                "AI service temporarily unavailable. "

                "Please try again later."

            ),

            "metadata": {

                "fallback": True

            }

        }