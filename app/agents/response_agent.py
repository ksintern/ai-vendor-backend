from app.graphs.graph_state import AgentState
from app.ai.ai_service import AIService


class ResponseAgent:

    @staticmethod
    async def execute(state: AgentState) -> AgentState:

        try:

            ai_service = AIService()

            vendors = state.get("ranked_vendors", [])
            filters = state.get("filters", {})
            user_message = state.get("query", "")
            intent = state.get("intent", "")

            # -----------------------------------
            # COMPARISON RESPONSE
            # -----------------------------------

            if intent == "comparison_query" and len(vendors) >= 2:

                v1 = vendors[0]
                v2 = vendors[1]

                def fmt_price(mn, mx):
                    if mn and mx:
                        return f"₹{mn:,} - ₹{mx:,}"
                    return "N/A"

                def fmt_rating(v):
                    rating = getattr(v, "avg_rating", None) or 0
                    reviews = getattr(v, "review_count", None) or 0
                    return f"⭐ {rating} ({reviews} reviews)"

                def fmt_score(v):
                    score = getattr(v, "match_score", None)
                    return f"{score}%" if score else "N/A"

                def fmt_verified(v):
                    return "✅ Verified" if getattr(v, "is_verified", False) else "Not verified"

                # -----------------------------------
                # STRUCTURED TABLE
                # -----------------------------------

                table = (
                    f"Here's a comparison of both vendors:\n\n"
                    f"{'Attribute':<20} {getattr(v1, 'name', 'Vendor 1'):<25} {getattr(v2, 'name', 'Vendor 2'):<25}\n"
                    f"{'-'*70}\n"
                    f"{'Price':<20} {fmt_price(getattr(v1, 'price_min', None), getattr(v1, 'price_max', None)):<25} {fmt_price(getattr(v2, 'price_min', None), getattr(v2, 'price_max', None)):<25}\n"
                    f"{'Rating':<20} {fmt_rating(v1):<25} {fmt_rating(v2):<25}\n"
                    f"{'Match Score':<20} {fmt_score(v1):<25} {fmt_score(v2):<25}\n"
                    f"{'Trust':<20} {fmt_verified(v1):<25} {fmt_verified(v2):<25}\n"
                    f"{'City':<20} {getattr(v1, 'city', 'N/A') or 'N/A':<25} {getattr(v2, 'city', 'N/A') or 'N/A':<25}\n"
                )

                # -----------------------------------
                # WINNER
                # -----------------------------------

                score1 = getattr(v1, "match_score", 0) or 0
                score2 = getattr(v2, "match_score", 0) or 0
                winner = v1 if score1 >= score2 else v2
                loser = v2 if score1 >= score2 else v1

                verdict = f"\n🏆 {getattr(winner, 'name', 'Vendor')} is the better match based on your requirements.\n"

                # -----------------------------------
                # AI EXPLANATION
                # -----------------------------------

                explanation_prompt = (
                    f"You are a vendor comparison assistant.\n\n"
                    f"A user asked: {user_message}\n\n"
                    f"Vendor 1: {getattr(v1, 'name', 'Vendor 1')}\n"
                    f"- Price: {fmt_price(getattr(v1, 'price_min', None), getattr(v1, 'price_max', None))}\n"
                    f"- Rating: {getattr(v1, 'avg_rating', 0)} ({getattr(v1, 'review_count', 0)} reviews)\n"
                    f"- Match Score: {fmt_score(v1)}\n"
                    f"- Verified: {getattr(v1, 'is_verified', False)}\n\n"
                    f"Vendor 2: {getattr(v2, 'name', 'Vendor 2')}\n"
                    f"- Price: {fmt_price(getattr(v2, 'price_min', None), getattr(v2, 'price_max', None))}\n"
                    f"- Rating: {getattr(v2, 'avg_rating', 0)} ({getattr(v2, 'review_count', 0)} reviews)\n"
                    f"- Match Score: {fmt_score(v2)}\n"
                    f"- Verified: {getattr(v2, 'is_verified', False)}\n\n"
                    f"Winner: {getattr(winner, 'name', 'Vendor')}\n\n"
                    f"Write a short explanation of Why {getattr(winner, 'name', 'Vendor')} wins. "
                    f"Then explain when someone might still prefer {getattr(loser, 'name', 'Vendor')}. "
                    f"End with a Recommendation section with two bullet points — one for each vendor. "
                    f"Be concise, friendly, and natural. No intro line needed."
                    f"Do not use markdown headers like ### or **bold**. "  # ← add this
                    f"Use plain text only."
                )

                ai_result = await ai_service.execute_prompt(explanation_prompt)

                if ai_result.get("success"):
                    ai_explanation = f"\nWhy?\n\n{ai_result.get('response', '').strip()}"
                else:
                    # Fallback if Ollama fails
                    ai_explanation = (
                        f"\nWhy?\n\n"
                        f"{getattr(winner, 'name', 'Vendor')} stands out with a higher match score, "
                        f"better ratings, and more reviews — indicating stronger reliability.\n\n"
                        f"{getattr(loser, 'name', 'Vendor')} remains a solid choice if "
                        f"budget is your top priority.\n\n"
                        f"Recommendation:\n"
                        f"• Choose {getattr(winner, 'name', 'Vendor')} for quality and reliability.\n"
                        f"• Choose {getattr(loser, 'name', 'Vendor')} for cost optimization."
                    )

                response = table + verdict + ai_explanation

            else:

                # -----------------------------------
                # STANDARD RECOMMENDATION RESPONSE
                # -----------------------------------

                response = await (
                    ai_service.build_recommendation_response(
                        user_message=user_message,
                        recommendations_exist=len(vendors) > 0,
                        filters=filters
                    )
                )

            state["ai_response"] = response
            state["current_agent"] = "response_agent"

            workflow = state.get("workflow_trace", [])
            workflow.append({
                "agent": "response_agent",
                "status": "success"
            })
            state["workflow_trace"] = workflow

            return state

        except Exception as e:

            errors = state.get("errors", [])
            errors.append(str(e))
            state["errors"] = errors

            workflow = state.get("workflow_trace", [])
            workflow.append({
                "agent": "response_agent",
                "status": "failed",
                "error": str(e)
            })
            state["workflow_trace"] = workflow

            return state