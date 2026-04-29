from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from typing import Optional

app = FastAPI(title="Daily Reflection Tree Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load tree ──────────────────────────────────────────────
TREE_PATH = os.path.join(os.path.dirname(__file__), "..", "tree", "reflection-tree.json")

with open(TREE_PATH, "r") as f:
    TREE_DATA = json.load(f)

NODE_MAP = {node["id"]: node for node in TREE_DATA["nodes"]}


# ── Models ─────────────────────────────────────────────────
class SessionState(BaseModel):
    current_node_id: str
    answers: dict = {}
    signals: dict = {
        "axis1": {"internal": 0, "external": 0},
        "axis2": {"contribution": 0, "entitlement": 0},
        "axis3": {"altrocentric": 0, "selfcentric": 0},
    }
    history: list = []


class AnswerRequest(BaseModel):
    session: SessionState
    selected_option: Optional[str] = None


# ── Helpers ────────────────────────────────────────────────
def get_dominant(axis_signals: dict) -> str:
    """Return the dominant pole for an axis, or 'balanced' if tied."""
    poles = list(axis_signals.items())
    if poles[0][1] > poles[1][1]:
        return poles[0][0]
    elif poles[1][1] > poles[0][1]:
        return poles[1][0]
    else:
        return "balanced"


def interpolate(text: str, answers: dict, signals: dict) -> str:
    """Replace {node_id.answer} and {axis.dominant} placeholders."""
    for node_id, answer in answers.items():
        text = text.replace(f"{{{node_id}.answer}}", answer)

    for axis_key, axis_vals in signals.items():
        dominant = get_dominant(axis_vals)
        text = text.replace(f"{{{axis_key}.dominant}}", dominant)

    return text


def resolve_next_node(node: dict, selected_option: str, session: SessionState) -> str:
    """Determine the next node ID based on node type and selected option."""
    node_type = node["type"]

    # Explicit target always wins (bridges, reflections)
    if node.get("target"):
        return node["target"]

    if node_type == "decision":
        # Parse routing rules from options list
        for rule in node["options"]:
            # Format: "answer=opt1|opt2:TARGET_NODE"
            condition, target = rule.split(":")
            _, values = condition.split("=")
            valid_answers = [v.strip() for v in values.split("|")]
            if selected_option in valid_answers:
                return target
        # Fallback: first child in node map
        for n in TREE_DATA["nodes"]:
            if n["parentId"] == node["id"]:
                return n["id"]

    # For question/start/bridge: find first child node
    for n in TREE_DATA["nodes"]:
        if n["parentId"] == node["id"]:
            return n["id"]

    return None


def record_signal(session: SessionState, signal: Optional[str]):
    """Tally axis signals from node."""
    if not signal:
        return
    axis, pole = signal.split(":")
    if axis in session.signals and pole in session.signals[axis]:
        session.signals[axis][pole] += 1


# ── Routes ─────────────────────────────────────────────────
@app.get("/start")
def start_session():
    """Initialize a fresh session at the START node."""
    start_node = NODE_MAP["START"]
    state = SessionState(current_node_id="START")
    return {
        "session": state.dict(),
        "node": start_node,
    }


@app.post("/advance")
def advance(req: AnswerRequest):
    """
    Advance the session forward.
    - Records the selected option (if any)
    - Tallies signals
    - Resolves the next node
    - Auto-advances through non-interactive nodes (decision, bridge, start)
    """
    session = req.session
    selected = req.selected_option

    current_node = NODE_MAP.get(session.current_node_id)
    if not current_node:
        raise HTTPException(status_code=404, detail=f"Node {session.current_node_id} not found")

    # Record answer if this was a question node
    if current_node["type"] == "question" and selected:
        session.answers[session.current_node_id] = selected
        record_signal(session, current_node.get("signal"))
        session.history.append({
            "node_id": session.current_node_id,
            "question": current_node["text"],
            "answer": selected,
        })

    # Resolve next node
    next_id = resolve_next_node(current_node, selected, session)
    if not next_id:
        raise HTTPException(status_code=400, detail="No next node found — conversation may be complete.")

    next_node = NODE_MAP[next_id]
    session.current_node_id = next_id

    # Record signal for non-question nodes (reflections etc.)
    if next_node["type"] != "question":
        record_signal(session, next_node.get("signal"))

    # Auto-advance through invisible nodes (decision, bridge, start)
    auto_advance_types = {"decision", "bridge", "start"}
    while next_node["type"] in auto_advance_types:
        next_id = resolve_next_node(next_node, selected, session)
        if not next_id:
            break
        next_node = NODE_MAP[next_id]
        session.current_node_id = next_id
        record_signal(session, next_node.get("signal"))

    # Interpolate text with answers and signals
    next_node = dict(next_node)  # copy so we don't mutate the global map
    next_node["text"] = interpolate(next_node["text"], session.answers, session.signals)

    # Build summary dominants if we're at the summary node
    if next_node["type"] == "summary":
        next_node["dominants"] = {
            axis: get_dominant(vals)
            for axis, vals in session.signals.items()
        }
        # Fix display labels in interpolated text
        next_node["text"] = next_node["text"].replace("selfcentric", "self-centric")

    return {
        "session": session.dict(),
        "node": next_node,
    }


@app.get("/node/{node_id}")
def get_node(node_id: str):
    node = NODE_MAP.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@app.get("/health")
def health():
    return {"status": "ok", "nodes_loaded": len(NODE_MAP)}
