# Daily Reflection Tree — DT Fellowship Assignment

**Submitted by:** Vishal Sharma  
**Role:** BA/DS Fellowship  

---

## What's in This Repo

```
/tree/
  reflection-tree.json     ← Part A: the full tree (28 nodes, 3 axes)
  tree-diagram.mermaid     ← Part A: visual diagram of all branching paths
write-up.md                ← Part A: design rationale (2 pages)
README.md                  ← You're here
```

---

## How to Read the Tree

Open `reflection-tree.json`. Each node has:

- `id` — unique identifier
- `parentId` — which node this follows from
- `type` — what kind of node it is (see below)
- `text` — what the employee sees
- `options` — fixed choices (question nodes) or routing rules (decision nodes)
- `target` — explicit jump target (used by bridges and reflections)
- `signal` — what gets tallied in state when this node is reached

### Node Types

| Type | Visible to employee? | Employee action |
|---|---|---|
| `start` | Yes | Auto-advances |
| `question` | Yes | Picks one option |
| `decision` | No | Auto-routes based on prior answer |
| `reflection` | Yes | Reads, clicks Continue |
| `bridge` | Yes | Auto-advances |
| `summary` | Yes | Reads their reflection summary |
| `end` | Yes | Session closes |

---

## How to Trace a Path

Example — employee who had a rough day and felt out of control:

```
START → A1_OPEN (picks "Like a wall")
→ A1_D1 (routes to LOW branch)
→ A1_Q_AGENCY_LOW → A1_Q2_LOW → A1_REFL_EXT
→ BRIDGE_1_2 → A2_OPEN (picks "Waiting for someone to notice")
→ A2_D1 (routes to ENTITLE branch)
→ A2_Q_ENTITLE_HIGH → A2_Q2_ENTITLE → A2_REFL_ENTITLE
→ BRIDGE_2_3 → A3_OPEN (picks "Just me")
→ A3_D1 (routes to SELF branch)
→ A3_Q_SELF_HIGH → A3_Q2_SELF → A3_REFL_SELF
→ SUMMARY → END
```

Every path through the tree hits exactly: 1 start + 3 opening questions + 3 decisions + 3 follow-up questions + 3 reflections + 2 bridges + 1 summary + 1 end = **15 nodes per session**.

---

## State Tracking

As the employee moves through the tree, the engine tallies signals:

```json
{
  "axis1": { "internal": 0, "external": 2 },
  "axis2": { "contribution": 0, "entitlement": 2 },
  "axis3": { "altrocentric": 0, "selfcentric": 2 },
  "answers": {
    "A1_OPEN": "Like a wall — kept blocking me no matter what I tried",
    "A1_Q_AGENCY_LOW": "To what other people should have done differently",
    ...
  }
}
```

The `dominant` field in the summary is derived from whichever signal is higher per axis. Ties default to the more growth-oriented pole.

---

## The Three Axes at a Glance

| Axis | Spectrum | Psychological Basis |
|---|---|---|
| Locus | Victim ↔ Victor | Rotter (1954), Dweck (2006) |
| Orientation | Entitlement ↔ Contribution | Campbell et al. (2004), Organ (1988) |
| Radius | Self-Centric ↔ Altrocentric | Maslow (1969), Batson (2011) |

---

## No LLM at Runtime

The tree is fully deterministic. No API calls, no AI inference, no randomness. Same answers → same path → same reflections. Every time.

LLMs were used during the *design process* — to stress-test questions against different employee personas, critique option phrasing, and research the psychological frameworks. The final product is a static JSON file walked by simple routing logic.
