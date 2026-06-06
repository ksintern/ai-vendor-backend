from app.graphs.graph_state import (
    AgentState
)

from app.ai.data_orchestrator import (
    DataOrchestrator
)


class ComparisonAgent:

    @staticmethod
    async def execute(
        state: AgentState
    ) -> AgentState:

        try:

            db = state.get(
                "db"
            )

            if db is None:

                raise ValueError(
                    "Database session missing from AgentState"
                )

            filters = state.get(
                "filters",
                {}
            )

            result = (
                DataOrchestrator.fetch_context(
                    db=db,
                    intent="comparison_query",
                    filters=filters,
                    user_preferences={}
                )
            )

            comparison_data = (
                result.get(
                    "context",
                    {}
                )
            )

            vendors = (
                comparison_data.get(
                    "vendors",
                    []
                )
            )

            state["comparison_result"] = (
                comparison_data
            )

            state["vendors"] = (
                vendors
            )

            state["ranked_vendors"] = (
                vendors
            )

            state["current_agent"] = (
                "comparison_agent"
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
                    "comparison_agent",

                    "status":
                    "success",

                    "vendors_found":
                    len(vendors)
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

            state["errors"] = (
                errors
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
                    "comparison_agent",

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