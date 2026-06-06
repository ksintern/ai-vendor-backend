from app.ai.intent_extractor import (
    IntentExtractor
)

from app.graphs.graph_state import (
    AgentState
)


class SupervisorAgent:

    @staticmethod
    async def execute(
        state: AgentState
    ) -> AgentState:

        try:

            query = state.get(
                "query",
                ""
            )

            result = (
                IntentExtractor.extract(
                    query
                )
            )

            state["intent"] = (
                result.get(
                    "intent",
                    "generic_platform_query"
                )
            )

            state["secondary_intents"] = (
                result.get(
                    "secondary_intents",
                    []
                )
            )

            state["confidence"] = (
                result.get(
                    "confidence",
                    0.0
                )
            )

            state["filters"] = (
                result.get(
                    "filters",
                    {}
                )
            )

            state["current_agent"] = (
                "supervisor_agent"
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
                    "supervisor_agent",

                    "status":
                    "success",

                    "intent":
                    state["intent"]
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
                    "supervisor_agent",

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