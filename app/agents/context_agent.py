from app.graphs.graph_state import (
    AgentState
)

from app.services.conversation_service import (
    ConversationService
)

from app.services.user_preference_service import (
    UserPreferenceService
)


class ContextAgent:

    @staticmethod
    async def execute(
        state: AgentState
    ) -> AgentState:

        try:

            db = state.get(
                "db"
            )

            user_id = state.get(
                "user_id"
            )

            session_id = state.get(
                "session_id"
            )

            conversation_context = ""

            user_preferences = {}

            # -----------------------------------
            # CONVERSATION CONTEXT
            # -----------------------------------

            if db and session_id:

                conversation_context = (
                    ConversationService
                    .build_context_summary(
                        db,
                        session_id
                    )
                )

            # -----------------------------------
            # USER PREFERENCES
            # -----------------------------------

            if db and user_id:

                user_preferences = (
                    UserPreferenceService
                    .get_user_preferences(
                        db,
                        user_id
                    )
                )

            state["conversation_context"] = (
                conversation_context
            )

            state["user_preferences"] = (
                user_preferences
            )

            state["current_agent"] = (
                "context_agent"
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
                    "context_agent",

                    "status":
                    "success"
                }
            )

            state["workflow_trace"] = (
                workflow
            )

            return state

        except Exception as e:

            db = state.get("db")

            if db:
                db.rollback()

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
                    "context_agent",

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