# Outreach Message Pack — Rounak Saraf
**Built 28 Aug 2026. Use with the Apply Queue tab of the tracker. Log every send in Outreach Log.**

---

## The three rules that make these work

**1. Never ask for the referral in message one to a stranger.** The 2026 referral benchmark data puts warm referrals at ~28% apply-to-hire versus 2–5% for cold applications — but that number belongs to referrals where a human can describe your work. A stranger who clicks "refer" in an ATS with a blank comment box produces a candidate recruiters discount. With alumni and ex-colleagues you *can* ask directly; with true strangers, earn one exchange first.

**2. State your visa position in the first three lines, unprompted.** You are an Indian national in Spain applying to the UK. The referrer's silent first question is "can we even hire this person?" If you don't answer it, they assume the worst and don't reply. If you are pursuing UK Global Talent (no employer sponsor needed), say so — it converts you from a hassle into someone who can start.

**3. One specific requisition, with its ID.** "Any openings?" is a request for the other person to do your work. "Req 6635837, Senior Backend Engineer" is a request they can act on in ninety seconds.

---

## Your reusable building blocks

Keep these three lines in a note on your phone. Every message below is assembled from them.

**The one-line identity**
> Senior engineer at Multiverse Computing in San Sebastián — I build the internal platform and agent tooling that ~200 engineers across 15 teams ship on.

**The signature proof point** (pick the variant that matches the role)
> *Dev tooling / agents:* I built Template Agents 0→1 — a deterministic codegen pipeline that generates production-ready FastAPI + Next.js services. Rule-based transforms with LLM calls scoped only to the unstructured steps, an append-only event log, and a serialization gate that fixed a nasty concurrent-run race. Cut scaffolding time 70%+ across 100+ services.
>
> *Infra / SRE:* I run 100+ production services on EKS via Helm and ArgoCD, architected to 99.99% with load balancing, pod replicas and DB failover — and stood up the org's first Dev–Test–Prod pipeline.
>
> *Identity / platform:* I migrated our whole fleet off an in-house auth mechanism onto enterprise SSO — Logto, Entra ID, Cognito over OIDC — without breaking downstream apps.
>
> *Enterprise delivery:* I'm tech lead on Foundry, a versioned SDK for a €20M client that exposes our compression and RAG algorithms; I own version propagation and rolling template upgrades downstream without breaking compatibility.

**The visa line** (pick one — use the truthful one)
> I'm an Indian national with the right to work in Spain, so EU-based and EU-remote roles need nothing from you. For the UK I'd need sponsorship — [*or*: I'm pursuing the UK Global Talent visa, which needs no employer sponsor].

---

## T1 — Cold recruiter DM (LinkedIn)

Keep under 120 words. Recruiters read on mobile between meetings.

> Hi [Name] — I saw you're hiring for [exact role title] in London (req [ID]).
>
> I'm a senior engineer at Multiverse Computing in Spain. I built our agent-based codegen pipeline that ~200 engineers across 15 teams now build on, and I run 100+ production services on EKS at 99.99%. The [specific thing from the JD — "developer experience" / "Kubernetes fleet" / "OIDC identity work"] part of that req is most of what I do day to day.
>
> On visas: [visa line].
>
> CV attached. Happy to send a short writeup of the codegen pipeline's design if useful.
>
> Rounak

**When to send:** within 48h of applying, not before. "I applied to req X" gives them something to pull up.

---

## T2 — Referral ask, IIIT-Delhi alum (your highest-conversion message)

Target engineers **3–8 years in**, not directors. They remember being where you are and they have referral-bonus money on the table.

> Hi [Name] — fellow IIIT-Delhi grad, I was ECE '22. I'm a senior engineer at Multiverse Computing in San Sebastián now.
>
> I'm applying to [exact role], req [ID], on your team's side of [Company]. Genuinely the closest thing to my actual work I've seen this year — I built a deterministic codegen pipeline that generates production FastAPI/Next.js services for ~200 engineers, plus the agent telemetry and operator dashboard over it.
>
> Two things and then I'll get out of your inbox:
> 1. Would you be willing to refer me? CV attached, req linked.
> 2. If you'd rather not — completely fine — I'd still love to hear how you're finding [team/company].
>
> On the boring bit: [visa line].
>
> Either way, good to see another IIIT-D person over there.
> Rounak

**Why this converts:** shared institution (a real reason to reply), one specific req, an explicit out, and the visa question answered before they can worry about it.

---

## T3 — Referral ask, ex-colleague or someone who has seen your work

Shorter. You've earned directness.

> Hi [Name] — hope Multiverse/[old company] is treating you well.
>
> I'm making a move — targeting London and EU-remote, mostly platform and AI-agent infrastructure work. [Company] has [exact role] open (req [ID]) and it's a good match: same shape as the Template Agents work you saw me build.
>
> Would you be up for referring me? Happy to send a paragraph you can paste into the referral form so it costs you two minutes rather than twenty.
>
> [visa line]
>
> Thanks either way —
> Rounak

**Always offer the paste-in paragraph.** Referral forms have a "why are you recommending them" box, and a blank one is what kills the referral's value. Write it *for* them:

> *Paste-in paragraph to include:* "Rounak built our internal codegen platform from scratch — it now generates production FastAPI/Next.js services for around 200 engineers across 15 teams and cut scaffolding time by 70%. He also runs 100+ services on EKS at 99.99% and led our fleet-wide migration to enterprise SSO. He's the person we send at a problem when nobody's sure what the architecture should be yet."

---

## T4 — Cold ask to a stranger at a target company (two-step)

**Message 1 — no ask at all:**

> Hi [Name] — I read your [post / talk / PR / blog] on [specific thing]. The bit about [genuinely specific detail] landed for me: I hit the same wall building a deterministic agent pipeline at Multiverse — we ended up putting a serialization gate in front of the shared state to kill a concurrent-run race, which felt like a hack until it didn't.
>
> No ask, just wanted to say it was a good read.
> Rounak

**Message 2 — only after they reply, 3–5 days later:**

> Thanks for the reply — that makes sense.
>
> Slightly cheeky follow-up: [Company] has [role] open (req [ID]) and I'm applying. If you have a view on whether that team is the real thing, I'd value it. And if you ever felt comfortable referring, that'd obviously help — but genuinely no pressure, the view is the more useful part.
>
> [visa line]

**Do not compress these into one message.** The whole value is that the first one asks for nothing.

---

## T5 — Hiring-manager note (for AI labs and startups especially)

Anthropic's careers page explicitly invites independent research, blog posts and open-source contributions, and says roughly half their technical staff had no prior ML experience. That is an invitation to lead with an artifact rather than a CV. Also note: **Anthropic asks applicants not to use AI in their application — write that one yourself.**

> Hi [Name] — I'm applying to [role] (req [ID]) and wanted to send you the thing rather than the CV.
>
> I built Template Agents at Multiverse: a deterministic pipeline that generates production-ready full-stack services. The interesting design constraint was refusing to let the LLM drive the whole thing — rule-based transforms handle everything structured, LLM calls are scoped only to the genuinely unstructured steps, every step lands in an append-only event log, and a serialization gate resolves concurrent runs. 200+ engineers across 15 teams build on it now; scaffolding time dropped 70%+.
>
> [1 sentence on why THIS team specifically — not the company, the team.]
>
> Writeup: [link]. CV attached. [visa line].
>
> Rounak

**Prerequisite:** write the Template Agents design note first. See the resume review — this is the single highest-leverage thing you can produce, and it doesn't exist yet.

---

## T6 — Follow-up chaser

Send once, 7–10 days after silence. Then stop.

> Hi [Name] — bumping this once in case it got buried. Still very interested in [role] (req [ID]).
>
> One thing I didn't mention: [a genuinely new, relevant fact — a shipped release, the design writeup going up, a relevant OSS contribution]. Happy to leave it there if the timing isn't right.
>
> Rounak

**Never send a third.** A second chaser reads as desperate and costs you the contact for later.

---

## T7 — Ask HN: Who wants to be hired (post 1 September)

The August 2026 thread ran 589 comments with real European entries — including an AI engineer in Gipuzkoa doing Python/FastAPI/RAG work. This is the highest reach-per-minute channel in the whole plan, and it inverts the direction of the ask.

```
Location: San Sebastián, Spain
Remote: Yes
Willing to relocate: Yes — London, Zurich, Amsterdam, Dublin
Technologies: Python, Go, TypeScript · FastAPI, Next.js/React · Kubernetes (EKS),
Helm, ArgoCD, Terraform, AWS · Kafka, PostgreSQL, ClickHouse, Druid ·
LLM agent pipelines, RAG, agent telemetry · OIDC/enterprise SSO
Résumé/CV: [link]
Email: rounaksaraf.official@gmail.com

Senior engineer, 4 years, currently at Multiverse Computing. I built Template
Agents 0→1: a deterministic codegen pipeline that generates production
FastAPI/Next.js services — rule-based transforms with LLM calls scoped only to
the unstructured steps, append-only event log, serialization gate for concurrent
runs. 200+ engineers across 15 teams build on it; scaffolding time down 70%+.
I also run 100+ services on EKS at 99.99% and led a fleet-wide migration to
enterprise SSO (OIDC).

Looking for: platform, developer-tooling, or AI-agent infrastructure work.
Indian national with Spanish work rights — EU and EU-remote need nothing from
you; UK would need sponsorship.
```

Repost in the 1st-of-month thread every month you're still searching.

---

## T8 — Blind / community referral post

Only if your Multiverse work email verifies on Blind (test it — it's a coin flip for a Spanish domain, and without it you get read-only access and can't post at all).

> **[Company] — Senior Backend/Platform, London, req [ID]**
>
> 4 YOE. Currently senior at a European deep-tech company: built an LLM codegen pipeline used by 200+ engineers, run 100+ services on EKS at 99.99%, led a fleet-wide OIDC migration. Applying to req [ID].
>
> Need UK sponsorship (Indian national, currently EU-based with Spanish work rights). Happy to send CV. If you'd refer, I'll send a paragraph you can paste into the form so it's not a blank recommendation.

Keep it short, always name the req, and always state the visa position — most London referral requests die on that unanswered question.

---

## T9 — Recruiter reply, when *they* approach you

Two-thirds of inbound recruiter messages die because the candidate answers "yes interested". Answer with a filter instead — it makes you look like someone with options, which you are.

> Hi [Name] — thanks for reaching out, this could be interesting.
>
> Three things that would help me judge fit quickly:
> 1. What's the band for this level, and is it London-based or is there EU-remote flexibility?
> 2. Does the role sponsor, and has this team sponsored before?
> 3. What does the team actually own — is this greenfield platform work or maintaining something existing?
>
> For context: I'm senior at Multiverse Computing, ~4 years in, and my current comp is around €115k equivalent, so I'm being selective. CV attached.
>
> Rounak

**On the comp question:** naming €115k anchors you low for London — London senior engineering comp at your targets runs well above that. Consider saying "I'd need a meaningful step up on €115k to move countries" rather than naming the number, or naming a target range instead of your current salary. In the UK you are never obliged to disclose current pay.

---

## The weekly cadence that actually gets this done

| Day | Action | Time |
|---|---|---|
| Mon | Run the LinkedIn Alumni query (`linkedin.com/alumni` → IIIT-Delhi → London → each target company). Build a list of 10 names for the week. | 45 min |
| Mon | Apply to 3 Wave-1 roles. | 60 min |
| Tue–Thu | Send 10 outreach messages (T2 for alumni, T4 for strangers). Log each in Outreach Log. | 30 min/day |
| Wed | Apply to 3 more Wave-1/2 roles. | 60 min |
| Fri | Send T6 chasers for anything 7+ days silent. Update every Status in the tracker. | 20 min |
| 1st of month | Post T7 in the Ask HN "Who wants to be hired" thread. | 15 min |

Ten thoughtful messages beat a hundred templated ones. If you only do one thing on this page, do the Monday alumni query.

---

## Things not to do

- **Don't pay for a referral.** Not $39/month to a marketplace, not $250 to a stranger. You're buying an ATS checkbox without the judgement that makes referrals valuable — and many employers' policies prohibit paid referrals, so anyone openly selling one is either lying about where they work or willing to breach policy. Neither should be vouching for you.
- **Don't send your full CV into ungated groups.** It names your employer, your team, your stack and your phone number — exactly the raw material for targeted phishing against you and Multiverse. Keep a public version with a job-search email alias and no personal address or phone.
- **Don't lead with "700+ LeetCode solved"** outside quant and big-tech. At AI labs and startups it reads junior. Lead with what you built.
- **Don't apply to Wise's current London req** (£68–87.5k posted) or anything else below your baseline. Your own search principle says a step-function or nothing — hold that line even when the search feels slow.
- **Anyone offering to "arrange sponsorship" or "expedite your Global Talent endorsement" for a fee is running a scam.** UK sponsorship is arranged by the employer with the Home Office; you pay only official statutory fees, directly to the government.
