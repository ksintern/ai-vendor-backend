from app.graphs.reasoning_graph import (
    reasoning_graph
)

from app.graphs.graph_state import AgentState

class GraphService:

    async def process(
        self,
        query: str,
        session_id: str,
        user_id: str,
        access_token: str | None,
        db
    ):

        state: AgentState = {

            "query": query,

            "session_id": session_id,

            "user_id": user_id,

            "access_token": access_token,

            "db": db,

            "workflow_trace": [],

            "errors": []

        }

        result = await reasoning_graph.ainvoke(
            state
        )

        return result