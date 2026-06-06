from app.ai.ai_service import (
    AIService
)

from app.graphs.graph_state import (
    AgentState
)


class QueryAnalysisAgent:

    @staticmethod
    async def execute(
        state: AgentState
    ) -> AgentState:

        try:

            ai_service = AIService()

            structured = await (
                ai_service.build_structured_response(
                    user_message=
                    state.get(
                        "query",
                        ""
                    ),

                    previous=None,

                    conversation_context=
                    state.get(
                        "conversation_context",
                        ""
                    )
                )
            )

            existing_filters = (
                state.get(
                    "filters",
                    {}
                )
            )

            new_filters = (
                structured.get(
                    "filters",
                    {}
                )
            )

            merged_filters = {
                **existing_filters,
                **new_filters
            }

            state["filters"] = (
                merged_filters
            )

            state["validation"] = (
                structured.get(
                    "validation",
                    {}
                )
            )

            state["search_payload"] = (
                structured.get(
                    "search_payload",
                    {}
                )
            )

            state["current_agent"] = (
                "query_analysis_agent"
            )

            workflow = (
                state.get(
                    "workflow_trace",
                    []
                )
            )

            workflow.append(
                {
                    "agent":
                    "query_analysis_agent",

                    "status":
                    "success"
                }
            )

            state["workflow_trace"] = (
                workflow
            )

            return state

        except Exception as e:

            errors = (
                state.get(
                    "errors",
                    []
                )
            )

            errors.append(
                str(e)
            )

            state["errors"] = errors

            workflow = (
                state.get(
                    "workflow_trace",
                    []
                )
            )

            workflow.append(
                {
                    "agent":
                    "query_analysis_agent",

                    "status":
                    "failed",

                    "error":
                    str(e)
                }
            )

            state["workflow_trace"] = (
                workflow
            )

            return state