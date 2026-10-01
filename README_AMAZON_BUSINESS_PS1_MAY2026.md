# Amazon Business PS1 Revision Plan (May 5 - May 8, 2026)

**Interview:** Friday, May 8, 2026  
**Time:** 11:30 AM - 12:30 PM CEST  
**Role:** Software Development Engineer, Amazon Business  
**Language:** Python  
**Interviewer:** Sr. Software Dev Engineer

This is a **3-day revision plan**, not a from-scratch study plan. The goal is to sharpen what you already know, reduce rust, and walk into the call calm and structured.

---

## What To Optimize For

- **Coding first:** this is the highest-probability signal in a phone screen.
- **LP stories second:** Amazon will almost certainly probe behavior.
- **System design light revision:** enough to speak clearly about trade-offs, APIs, caching, scaling, and data modeling if asked.

---

## Daily Structure

Use this format on each prep day:

1. **Warm-up (20-30 min)**  
   One easy problem or revisit one solved pattern.
2. **Coding block 1 (60-90 min)**  
   One medium or hard, done interview-style.
3. **LP block (30-45 min)**  
   Speak STAR stories out loud.
4. **Coding block 2 (60-90 min)**  
   One medium or one medium + one easy.
5. **System design revision (30-45 min)**  
   Review notes, not deep-dives.
6. **Wrap-up (15 min)**  
   Write mistakes, edge cases, and 2-3 phrases you want to reuse.

---

## Day 1: Tue, May 5

**Goal:** Re-enter interview mode and lock coding rhythm.

### Coding

- Done `Add Two Numbers (2)`
- Done `Kth Largest Element in an Array (215)`
- Done `Find Eventual Safe States (802)`

### LP

Prepare and speak these stories:
- **Ownership**
- **Dive Deep**
- **Deliver Results**

For each story, be ready with:
- Situation
- Task
- Action
- Result
- What you learned

### System Design Revision

Review:
- Caching + Redis
- Load balancer basics
- Rate limiting basics

Use:
- [README_AMAZON_SDE2_NOTES.md](/Users/rounak/Desktop/prep/README_AMAZON_SDE2_NOTES.md)

### Day 1 Success Criteria

- You solve at least 2/3 coding questions cleanly.
- You can explain `cache-aside`, `token bucket`, and `L7 vs L4` without notes.
- You can tell 3 LP stories in under 3 minutes each.

---

## Day 2: Wed, May 6

**Goal:** Hit high-signal interview patterns and tighten explanations.

### Coding

- Done `Task Scheduler (621)`
- Done `Reorganize String (767)`
- Done `Largest Rectangle in Histogram (84)`
- Done `Split Array Largest Sum (410)`

### LP

Prepare and speak these stories:
- **Customer Obsession**
- **Bias for Action**
- **Earn Trust**

Also prep one conflict/failure story:
- disagreement
- missed expectation
- recovery

### System Design Revision

Review:
- SQL vs NoSQL
- normalization vs denormalization
- sharding vs partitioning
- consistent hashing

### Mock Behavior Drill

Answer these aloud:
- “Tell me about yourself.”
- “Why Amazon?”
- “Tell me about a time you disagreed with someone.”
- “Tell me about a time you went deep into a problem.”

### Day 2 Success Criteria

- You can solve one heap/greedy question without major hints.
- You can explain `consistent hashing` and `normalization vs denormalization` crisply.
- You have 6 LP stories that feel natural, not memorized.

---

## Day 3: Thu, May 7

**Goal:** Simulate the interview, then taper down.

### Mock Interview Round

Do this in one sitting:
- 5 min: clarify problem
- 30-35 min: solve one coding problem live
- 10 min: behavioral answer
- 5 min: ask 2 thoughtful questions

Recommended mock coding pick:
- `Alien Dictionary (269)` if you want a harder graph/topo rep
- `Critical Connections (1192)` if you want hard graph depth
- `Add Two Numbers (2)` if you want confidence and fluency

### Light Coding After Mock

- `Counting Bits (338)`
- `Reverse Bits (190)`

These are confidence-builders and good for clean communication practice.

### LP Final Review

Pick your best 5 stories and map them to multiple LPs:
- Ownership
- Customer Obsession
- Dive Deep
- Bias for Action
- Deliver Results

### System Design Final Review

Only revise:
- API design basics
- DB choice trade-offs
- cache + invalidation
- rate limiting
- scaling reads/writes

Do **not** start new topics here.

### Day 3 Success Criteria

- You finish one mock interview end-to-end.
- You have 5 polished LP stories.
- You stop prep with confidence, not exhaustion.

---

## Interview Morning: Fri, May 8

### 60-90 Minutes Before

- Wake up early enough to avoid rushing.
- Eat something light.
- Check audio, camera, laptop, charger, network.
- Open Zoom test and the Amazon livecode link.

### 30 Minutes Before

- Review only:
  - complexity cheat sheet
  - 5 LP stories
  - one-page system design bullets

Do **not** solve a hard new problem.

### 10 Minutes Before

- Breathe.
- Join on time, not too early.
- Keep:
  - water
  - notebook
  - charger
  - quiet room

---

## Coding Rules For The Interview

- Clarify inputs, outputs, and constraints first.
- Start with brute force briefly if needed, then improve.
- Narrate while coding.
- Use clear Python names, not contest names.
- Say complexity out loud.
- Test with 2-3 examples before you stop.

If stuck:
- say what you considered
- say why it fails
- move to the next best approach

That still scores better than going silent.

---

## LP Rules For The Interview

- Use **I**, not **we**, when describing your contribution.
- Quantify results whenever possible.
- Keep stories tight: 2-3 minutes max.
- End with the impact and what changed because of your action.

If you do not have a perfect story for a principle, use a real one that shows judgment and ownership.

---

## Questions To Ask The Interviewer

Pick 2:

- “What does success look like for an SDE in this team in the first 6 months?”
- “What are the biggest technical challenges the team is solving right now?”
- “How does the team balance speed of delivery with long-term engineering quality?”
- “What kinds of systems or products does this role contribute to most directly?”

---

## Recommended 3-Day Coding Set

If you want the shortest high-value set, do these:

1. Done `Add Two Numbers (2)`
2. Done `Kth Largest Element in an Array (215)`
3. Done `Find Eventual Safe States (802)`
4. Done `Task Scheduler (621)`
5. Done `Reorganize String (767)`
6. Done `Largest Rectangle in Histogram (84)`
7. `Alien Dictionary (269)` or `Critical Connections (1192)`
8. `Counting Bits (338)`
9. `Reverse Bits (190)`

---

## Final Reminder

You do **not** need to become a different candidate in 3 days.  
You need to show:

- clear thinking
- calm communication
- strong core coding
- structured LP answers

That is enough to do very well in a PS1.
