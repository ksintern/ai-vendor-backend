import logging
from app.graphs.graph_state import AgentState
from app.tools.tool_registry import ToolRegistry
from app.utils.vendor_adapter import VendorAdapter

logger = logging.getLogger(__name__)

class ToolCallingAgent:

    async def execute(
        self,
        state: AgentState
    ) -> AgentState:

        try:

            filters = state.get("filters", {})
            token = state.get("access_token")
            intent = state.get("intent")

            registry = ToolRegistry(token=token)

            tool_name = ""
            tool_input = {}
            tool_output = {}

            # ---------------------------------
            # Vendor Search
            # ---------------------------------

            if intent in ["vendor_recommendation", "service_query"]:

                tool_name = "search_vendors"
                tool_input = filters

                tool = registry.get_tool(tool_name)
                if not tool:
                    raise ValueError(f"Tool not found: {tool_name}")

                tool_output = await tool(
                    category=filters.get("category"),
                    city=filters.get("city"),
                    min_price=filters.get("price_min"),
                    max_price=filters.get("price_max")
                )

                logger.debug(f"[ToolCallingAgent] search_vendors raw output: {tool_output}")

                vendors = []
                if isinstance(tool_output, dict):
                    vendors = tool_output.get("vendors", [])
                    vendors = [VendorAdapter.adapt(v) for v in vendors]

                state["vendors"] = vendors
                state["ranked_vendors"] = []  # reset so RankingAgent fills it fresh

            # ---------------------------------
            # Session Query
            # ---------------------------------

            elif intent == "session_query":

                session_id = state.get("session_id")

                logger.debug(f"[ToolCallingAgent] session_query | session_id={session_id}")

                tool_name = "get_session_context"

                tool = registry.get_tool(tool_name)
                if not tool:
                    raise ValueError(f"Tool not found: {tool_name}")

                tool_output = await tool(
                    session_id=session_id,
                    token=token
                )

                logger.debug(f"[ToolCallingAgent] session_context raw output: {tool_output}")

                # Normalize the session context into a consistent shape
                # so ResponseAgent always receives { "context": <str or dict> }
                if isinstance(tool_output, dict):
                    # Already has "context" key — use as-is
                    if "context" in tool_output:
                        normalized_context = tool_output

                    # API returned nested under "data"
                    elif "data" in tool_output:
                        normalized_context = tool_output.get("data", {})

                    # API returned raw fields (messages, summary, etc.)
                    else:
                        normalized_context = {
                            "context": tool_output  # wrap the whole dict
                        }
                else:
                    normalized_context = {
                        "context": str(tool_output)
                    }

                logger.debug(f"[ToolCallingAgent] normalized session_context: {normalized_context}")

                state["session_context"] = normalized_context

                # Explicitly clear vendors so RankingAgent
                # and ResponseAgent don't get confused
                state["vendors"] = []
                state["ranked_vendors"] = []

            # ---------------------------------
            # Query Understanding   
            # ---------------------------------

            elif intent == "query_understanding":

                query = state.get(
                    "query",
                    ""
                )

                tool_name = (
                    "ai_understand_query"
                )

                tool = registry.get_tool(
                    tool_name
                )

                if not tool:
                    raise ValueError(
                        f"Tool not found: {tool_name}"
                    )

                tool_output = await tool(
                    query=query
                )

                state["query_analysis"] = (
                    tool_output
                )

                state["vendors"] = []
                state["ranked_vendors"] = []

            # ---------------------------------
            # Unhandled intent — log and skip
            # ---------------------------------

            else:
                logger.warning(f"[ToolCallingAgent] No tool mapped for intent: {intent}")

            state["tool_name"] = tool_name
            state["tool_input"] = tool_input
            state["tool_output"] = tool_output
            state["tool_status"] = "success"

            trace = state.get("workflow_trace", [])
            trace.append({
                "agent": "tool_calling_agent",
                "status": "success",
                "tool": tool_name,
                "intent": intent
            })
            state["workflow_trace"] = trace

            return state

        except Exception as e:

            logger.error(f"[ToolCallingAgent] Exception: {str(e)}", exc_info=True)

            state["tool_status"] = "failed"
            state["tool_error"] = str(e)

            errors = state.get("errors", [])
            errors.append(str(e))
            state["errors"] = errors

            trace = state.get("workflow_trace", [])
            trace.append({
                "agent": "tool_calling_agent",
                "status": "failed",
                "error": str(e)
            })
            state["workflow_trace"] = trace

            return state