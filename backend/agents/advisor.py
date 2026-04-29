from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class AdvisorState(TypedDict):
    user_id: int
    messages: List[dict]
    intent: str
    response: str

def detect_intent(state: AdvisorState) -> AdvisorState:
    last_msg = state["messages"][-1]["content"].lower()
    if "resume" in last_msg or "profile" in last_msg:
        state["intent"] = "profile"
    elif "career" in last_msg or "transition" in last_msg or "role" in last_msg:
        state["intent"] = "career_path"
    elif "skill" in last_msg or "learn" in last_msg or "gap" in last_msg:
        state["intent"] = "coach"
    elif "interview" in last_msg or "question" in last_msg:
        state["intent"] = "mock_interview"
    else:
        state["intent"] = "general"
    return state

def route_intent(state: AdvisorState) -> str:
    return state["intent"]

def general_response(state: AdvisorState) -> AdvisorState:
    state["response"] = "I'm Clairo, your AI career advisor. Ask me about your resume, career paths, skill gaps, or interview prep!"
    return state

def profile_node(state: AdvisorState) -> AdvisorState:
    state["response"] = "[Profile Agent] — coming soon"
    return state

def career_path_node(state: AdvisorState) -> AdvisorState:
    state["response"] = "[CareerPath Agent] — coming soon"
    return state

def coach_node(state: AdvisorState) -> AdvisorState:
    state["response"] = "[Coach Agent] — coming soon"
    return state

def mock_interview_node(state: AdvisorState) -> AdvisorState:
    state["response"] = "[MockInterview Agent] — coming soon"
    return state

graph = StateGraph(AdvisorState)

graph.add_node("detect_intent", detect_intent)
graph.add_node("general", general_response)
graph.add_node("profile", profile_node)
graph.add_node("career_path", career_path_node)
graph.add_node("coach", coach_node)
graph.add_node("mock_interview", mock_interview_node)

graph.set_entry_point("detect_intent")

graph.add_conditional_edges("detect_intent", route_intent, {
    "general": "general",
    "profile": "profile",
    "career_path": "career_path",
    "coach": "coach",
    "mock_interview": "mock_interview",
})

for node in ["general", "profile", "career_path", "coach", "mock_interview"]:
    graph.add_edge(node, END)

advisor_graph = graph.compile()