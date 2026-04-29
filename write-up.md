# Design Rationale — Daily Reflection Tree
**Vishal Sharma | DT Fellowship Assignment**

---

## Why These Questions

The hardest thing about designing this tree wasn't the branching logic. It was figuring out how to ask honest questions without making someone feel interrogated.

Most reflection tools fail because they're surveys pretending to be conversations. The employee can smell the "right" answer from the first option and clicks through in ninety seconds without actually thinking about anything. I wanted to avoid that.

So the first decision I made was to write questions where no option is obviously "good." On Axis 1, "I pushed through even when it felt pointless" is just as valid as "I looked for what I could actually change." On Axis 2, "I did what was expected and not much more" is an honest answer that a lot of people would give on most days. The tree shouldn't make them feel bad for picking it — it should use that answer to ask something sharper.

The opening question — "If today were a person, how would it have treated you?" — came from thinking about how people actually talk about hard days. Nobody says "I had an external locus of control experience today." They say the day was relentless, or cooperative, or just weird. The metaphor creates a little psychological distance that makes it easier to be honest. From there, the routing is simple: days that felt collaborative or challenging (partner/test) go down the agency-high path; days that felt like obstacles or chaos (wall/stranger) go down the agency-low path.

---

## How I Designed the Branching

The branching does two things simultaneously: it routes the employee toward appropriate follow-up questions, and it accumulates signals that feed the summary.

Each question node tags a signal — `axis1:internal` or `axis1:external`, for example. Decision nodes read the employee's last answer and route accordingly. By the time the employee reaches the summary, the tree has tallied which pole they leaned toward on each axis. The summary reflects that back without scoring or judging.

The trade-off I made was to keep the branching relatively flat — two main paths per axis rather than deeply nested trees. I did this deliberately. Deeply nested trees feel like mazes. They also make it harder for the employee to maintain a sense that this is a conversation rather than a questionnaire. With two branches per axis, the session stays under fifteen nodes per path and can be completed in under five minutes — which matters if this is supposed to be a daily habit at the end of a tiring workday.

The bridge nodes between axes do something specific: they don't just transition, they reframe. "We've looked at how you navigated today — now let's look at what you brought to it" is doing the same work a good therapist does when moving between topics: naming where you've been before moving forward. This makes the conversation feel cohesive rather than like three separate quizzes.

---

## Psychological Sources

**Axis 1 — Locus of Control (Rotter, 1954) + Growth Mindset (Dweck, 2006)**
Rotter's original insight was that internal vs external locus isn't about optimism — it's about where someone locates the source of outcomes. A person with an internal locus who has a bad day doesn't necessarily think they caused it; they think about what they could have done differently within it. I tried to capture that nuance in A1_Q_AGENCY_HIGH: the options aren't "I succeeded" — they're "I looked for what I could change," which is an internal orientation even in the middle of failure.

**Axis 2 — Psychological Entitlement (Campbell et al., 2004) + Organizational Citizenship Behavior (Organ, 1988)**
Entitlement is invisible to the person holding it, which is what makes it so hard to surface without shaming. The question "What's underneath it, honestly?" on the entitlement path tries to get at this — it invites the employee to look beneath the frustration rather than justify it. Organ's OCB research shows that discretionary effort (helping beyond your job description, volunteering for unglamorous work) is the single strongest predictor of team effectiveness. The contribution path questions try to surface concrete examples of this, not abstract commitments.

**Axis 3 — Self-Transcendence (Maslow, 1969) + Perspective-Taking (Batson, 2011)**
Maslow's 1969 paper argued that self-actualization wasn't the peak of human development — self-transcendence was. The shift from "what do I need" to "what does the world need from me." I kept this axis concrete rather than philosophical: it's not about grand purpose, it's about whether the employee's awareness extended to the people around them during an ordinary workday. Batson's perspective-taking research shows that the simple act of imagining another's experience — not fixing it, just understanding it — measurably changes behavior. The Axis 3 reflection on the self-centric path asks the employee to try exactly that tomorrow.

---

## What I'd Improve With More Time

Three things.

First, I'd add a fourth axis around **time orientation** — whether the employee's attention during the day was mostly on the past (what went wrong), present (what's happening now), or future (what's coming next). This is less established psychologically but practically important: employees who are stuck ruminating on yesterday's mistake and employees who are anxiously planning next week are both unavailable to the people around them today.

Second, I'd add **longitudinal pattern detection**. The tree as designed gives you a snapshot of one day. With three months of data, you could show the employee their own patterns: "You're consistently on the external-locus path on Mondays — does that match your experience?" That's a fundamentally different and more valuable kind of insight.

Third, the summary node is the weakest part of the current design. It names the dominant signals but doesn't do enough to synthesize them. A good summary should do what a good coach does: reflect back what the employee's path actually revealed, not just report the tally. With more time, I'd write unique summary text for each of the eight possible combinations of dominant signals (internal/external × contribution/entitlement × altrocentric/selfcentric).

---

*Total nodes: 28 | Question nodes: 11 | Decision nodes: 3 | Reflection nodes: 6 | Bridge nodes: 2 | Summary: 1 | Start/End: 2*
