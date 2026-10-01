# Resume Review — three versions, honest read
**28 Aug 2026. Reviewed against what the 139 live reqs in your tracker actually screen for.**

The writing is good. Specific numbers, verbs that mean something, no filler. Most engineers' resumes are worse than these. So this review is mostly about a handful of concrete defects and one strategic gap — not a rewrite.

---

## Fix these before you send anything (30 minutes total)

### 1. Your job title doesn't survive machine reading — this is the serious one

Your tagline is set in fake small-caps (a capital letter followed by smaller letters), and text extraction reads it as:

```
S enior S oftware E ngineer · AI P roducts & F ull -S tack
```

That's not a rendering quirk on my end — it's what the PDF's text layer actually contains, and it's what an ATS parser gets. So the single most important keyword phrase on the page, in the most prominent position, does not match a search for "Senior Software Engineer". Same breakage on "Full-Stack".

**Fix:** set that line in normal type (bold or letter-spaced if you want the look), or use a font's real small-caps feature rather than manually shrinking letters. Then re-export and check: open the PDF, select the tagline, copy it, paste it into a plain text editor. If it comes out clean, you're done.

Worth checking the rest of the same way while you're there — copy the whole PDF into a text editor and read it. It's the closest free approximation of what an ATS sees.

### 2. Overlapping employment dates

```
Multiverse Computing   Dec 2023 – Present
Inovatyv Pvt. Ltd.     Jun 2023 – May 2024   ← overlaps by six months
```

Two apparently full-time roles running simultaneously. A recruiter who notices reads it as either carelessness or an inflated timeline, and it's the kind of thing background checks surface later at the worst moment. There's also an unexplained Mar–Jun 2023 gap after CodeNation.

**Fix:** if the Inovatyv work was contract, part-time or freelance alongside the move, label it — "Software Engineer (Contract)" or "(Part-time)" solves it in one word. If the dates are simply wrong, correct them. Don't leave it ambiguous.

### 3. Tense drift inside a past role

Your SDE2 block (Dec 2023 – Nov 2025) opens with "**Own** the universal platform" and "**Operate** 100+ production services" — present tense in a role that ended. The SDE3 block above it correctly uses past tense.

**Fix:** "Owned", "Operated". Small, but it's the kind of thing a careful reader notices on a document whose whole job is signalling care.

### 4. Phone formatting

`(+34) 647-386-943` → `+34 647 386 943`. Some parsers choke on the parenthesised country code. Trivial fix, zero downside.

### 5. Confirm your links are real hyperlinks

`github.com/rounaksaraf` and `linkedin.com/in/rounak-saraf` appear as plain text. If they aren't clickable in the exported PDF, half your readers won't type them out. Check in a PDF viewer and add the hyperlinks if they're missing.

---

## The one strategic change worth making

### Add your Spanish work rights to the header. This is your most underused asset.

Right now your header says "San Sebastián, Spain · Open to relocation to London". A recruiter reading that sees an Indian name, a Spanish address, and a UK target — and has no idea what your work authorisation is. Silence gets read pessimistically.

Meanwhile, the research turned up a whole tier of roles you can take *today with no immigration process at all*: Grafana Labs posts a Spain-remote twin of every single UK req, Datadog's REDAPL role lists Madrid as a location option, Celonis has a Madrid senior req, Elastic has a Spain-based one, Hugging Face has EMEA-remote roles, ElevenLabs is remote-global. That's a dozen strong roles where your Spanish status turns you from "visa problem" into "starts in four weeks".

**Fix (assuming it's accurate for you):**

> San Sebastián, Spain · EU work authorisation (Spain) · Open to London relocation

And if you're pursuing UK Global Talent — the route that needs no employer sponsor — that belongs in the header too. It removes the hiring manager's single biggest objection before they've finished reading your name.

---

## Which resume goes where

Your three versions are genuinely differentiated, which is more than most people manage. Mapping them to the 139 live roles:

| Resume | Use it for | Roughly how many of your live roles |
|---|---|---|
| **Backend/Infra** | The workhorse. All quant and bank roles, all Kubernetes/SRE/platform roles, OpenAI infra, Anthropic K8s, Palantir, Monzo, G-Research, Bloomberg, Grafana, Vercel, Amazon | ~60% |
| **AI Agent Platforms & Dev Tooling** | The differentiator. Anthropic CI, G-Research Engineering Tools, DRW Developer Experience, Tower Development Tools, Bloomberg DevX, Grafana Platform Productivity, Cursor FDE, xAI Sandbox Service, Scale Frontier Agents, Databricks FDE | ~25% |
| **AI/Fullstack** | Wayve Model Development Platform, ElevenLabs, Figma AI Product, Scale Enterprise, Google Zurich Full Stack | ~15% |

**Consider a fourth variant: Data Platform.** Several strong roles — G-Research Analytics Services Platform (R3409) and Data Software Engineer (R3714), HRT Data Production Engineer, Optiver Reference Data — want exactly PySpark/Airflow/NiFi/Druid/ClickHouse. Right now that work is buried in a single line under Inovatyv, three roles down the page. For those four reqs it should be the headline, with ClickHouse/Druid/Cassandra promoted out of the Data skills line into the summary. It's a 45-minute edit that materially changes four applications.

---

## Content notes, in rough priority order

**The seniority gap is real and you can't paper over it.** You were promoted to SDE3 in Nov 2025, so at Aug 2026 you have ~9 months at senior and ~4 years total. Meanwhile every Anthropic London req is Staff or Staff+, DeepMind's agentic-tooling role asks 8+, Adyen's observability role asks 10+. Apply to two or three of those anyway — Staff bars are softer than they read, and your scope genuinely exceeds your tenure. But build the plan on the roles where the level is right: Palantir Apollo ("open to all levels of experience"), Palantir Substrate (4+ yrs), Figma AI Product (3+ yrs), Monzo L50, Citadel and Jane Street generalist SWE with no seniority label. There are enough of those.

**Write the Template Agents design note. This is the highest-leverage thing you're not doing.** Anthropic's careers page explicitly invites independent research, blog posts and open-source contributions, and notes that roughly half their technical staff had no prior ML experience. Every AI lab reads the same way. You have a genuinely interesting design to write about — refusing to let the LLM drive, rule-based transforms with LLM calls scoped to the unstructured steps, an append-only event log, a serialization gate resolving a concurrent-run race. That last detail is the kind of thing engineers remember. 1,200 words on your own domain or a Substack, linked from all three resumes and every T5 message. Nothing else you can produce in a weekend moves the needle this much. *(One caveat: Anthropic asks applicants not to use AI in their application materials — write that one in your own hand.)*

**"700+ LeetCode problems solved" is context-dependent.** Keep it for quant (Jane Street, Citadel, HRT, Optiver — the screen is the whole filter there and this is your strongest signal) and big tech. Cut it from the AI/Fullstack version, where it reads like a new grad's resume.

**"CGPA 8.2/10" means nothing to a UK or US reader** and costs you a line. Drop it; keep the degree and institution.

**The Karate brown belt earns its place.** It's one clause, it's a real thing about you, and interviewers remember it. Keep it.

**"€20M client" is your best single credibility marker outside the platform numbers.** It's currently the fourth bullet under SDE3 in the Backend/Infra version. For enterprise-heavy targets — Palantir FDE, Databricks, Scale Enterprise, the banks — move it to first.

**Your dashboard work is undersold.** "Built the agent dashboard front to back: run control, pipeline graph, and live telemetry over every step, tool call, and token spend" is, almost word for word, what LangSmith and every agent-observability product does. For Grafana's Staff AI Engineer role, LangChain's observability role, and Datadog, that bullet should be near the top with the word *observability* in it — they search for that word.

---

## What I'd actually do with this

The 30 minutes on the five defects above, today, before the first application goes out. The Spain work-authorisation line in the header, today. The Data Platform variant this weekend if you want the four G-Research/HRT/Optiver data reqs. The Template Agents writeup next weekend — and then link it from everything.

Everything else here is optional polish on a document that's already doing its job.
