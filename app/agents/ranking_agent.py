from app.graphs.graph_state import (
    AgentState
)


class RankingAgent:

    @staticmethod
    async def execute(
        state: AgentState
    ) -> AgentState:

        try:

            vendors = state.get(
                "vendors",
                []
            )

            print(
                "RANKING AGENT INPUT:",
                len(vendors)
            )

            print(
                "RANKING AGENT VENDORS:",
                [
                    v.name if hasattr(v, "name")
                    else str(v)
                    for v in vendors
                ]
            )

            state["ranked_vendors"] = (
                vendors
            )

            state["current_agent"] = (
                "ranking_agent"
            )

            workflow = state.get(
                "workflow_trace",
                []
            )

            workflow.append(
                {
                    "agent":
                    "ranking_agent",

                    "status":
                    "success",

                    "vendors_ranked":
                    len(vendors)
                }
            )

            state["workflow_trace"] = workflow

            return state

        except Exception as e:

            errors = state.get(
                "errors",
                []
            )

            errors.append(
                str(e)
            )

            state["errors"] = errors

            workflow = state.get(
                "workflow_trace",
                []
            )

            workflow.append(
                {
                    "agent":
                    "ranking_agent",

                    "status":
                    "failed",

                    "error":
                    str(e)
                }
            )

            state["workflow_trace"] = workflow

            return state