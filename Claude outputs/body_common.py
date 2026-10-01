# -*- coding: utf-8 -*-
# Shared, de-narrativised bullets. No em dashes anywhere; en dash only in date ranges.
ORG = (r"\item Owned the universal platform standardising FastAPI/Next.js/Streamlit delivery across the entire "
       r"engineering organisation: product, services, DevOps and MLOps, \textbf{200+} engineers across "
       r"\textbf{15+} teams at peak. Migrated auth from an in-house mechanism to enterprise SSO (Logto, OIDC) fleet-wide.")
EKS = (r"\item Operated \textbf{100+} production services on EKS via Helm and ArgoCD at \textbf{99.99\%} "
       r"availability: load balancing, pod replicas, DB failover.")
BRANCH = (r"\item Chose staged \textbf{Dev-Test-Prod} over trunk-based development for the platform: release "
          r"discipline across the organisation did not support safe continuous integration to main. Built the "
          r"first staged pipeline; now the standard branching strategy on ongoing projects.")
ONCALL = (r"\item On-call across time zones for a \textbf{70+} engineer, \textbf{15-app} build day: hot-patched "
          r"deployment and auth edge cases in flight; shipped the missing logging layer and deployment docs.")
CI = r"\item Cut GitLab CI runtime \textbf{65\%} across all jobs via caching, modularisation and parallelisation."
INOV = (r"\item Architected a secure HR system for \textbf{10,000+} employees and the APIs behind a core-banking "
        r"platform. Built its financial data pipelines (PySpark/Airflow, NiFi, PostgreSQL, Druid on K8s) serving "
        r"\textbf{100,000+} bank clients; cut compute \textbf{60\%}.")
CN1 = (r"\item Shipped a GPT-3 QA and automated L1 support system (React, TypeScript, GraphQL, AWS CDK); cut "
       r"ticket resolution \textbf{15h} to \textbf{7min}.")
CN2 = (r"\item Designed the Lambda + SQS async pipeline behind it, processing \textbf{80,000+} support "
              r"tickets in under \textbf{2h}.")

URL = "https://www.linkedin.com/pulse/how-i-built-template-agents-deterministic-ai-pipelines-rounak-saraf-kybpe/"
TA = (r"\item Built \href{" + URL + r"}{\textbf{Template Agents}} $\mathbf{0{\to}1}$, a deterministic codegen "
      r"pipeline: rule-based transforms, LLM calls scoped to unstructured steps, append-only event log, "
      r"serialization gate resolving a concurrent-run race. Cut service scaffolding \textbf{70\%+} across "
      r"\textbf{100+} services.")
OBS = (r"\item Built the per-run agent observability layer: step, tool call, token spend, reasoning trace. "
       r"\textbf{6} releases, \textbf{500+} automated tests.")
FOUNDRY = (r"\item Tech lead, \textbf{Foundry}: versioned SDK for a \textbf{\euro{}20M} client exposing "
           r"Multiverse's compression, pruning and healing algorithms as a RAG platform. Owned version propagation "
           r"and rolling template upgrades downstream without breaking compatibility. Ramped \textbf{10+} engineers "
           r"to independent ownership; established the team's design-review process.")
CENTRAL = (r"\item Extending Template Agents into a central delivery platform: completed client work, Foundry "
           r"included, generalised into reusable components so new projects are generated from the platform "
           r"rather than built alongside it.")

EDU = (r"\edu{\textbf{Writing:} \href{" + URL + r"}{How I Built Template Agents: Deterministic AI Pipelines} (LinkedIn, 2026)}" + "\n"
       r"\edu{\textbf{B.Tech, Electrical and Computer Engineering.} Indraprastha Institute of Information "
       r"Technology (IIIT), Delhi \textperiodcentered{} 2022}" + "\n"
       r"\edu{\textbf{Startup Technical Advisor}, Creative Destruction Lab (CDL) San Sebasti\'an: advise "
       r"early-stage teams on engineering strategy, from architecture to production pipelines.}" + "\n")
ACH_LC = (r"\edu{\textbf{700+} problems solved on \href{https://leetcode.com/u/Rounak_08/}{LeetCode} \textperiodcentered{} Karate Senior Brown Belt, WSKF \textperiodcentered{} Classical Guitar, Trinity College London Grade 4.}")
ACH_NO = ACH_LC
def doc(subtitle, summary, skills, sde3, sde2):
    return "\n".join([
      r"\input{preamble}", r"\begin{document}",
      r"\headerblock{" + subtitle + "}", "",
      r"\summ{" + summary + "}", "",
      r"\section{SKILLS}", skills, "",
      r"\section{EXPERIENCE}",
      r"\role{Senior Software Engineer (SDE 3), Multiverse Computing}{Nov 2025 -- Present}{San Sebasti\'an, Spain}",
      r"\begin{bullets}", sde3, r"\end{bullets}", "",
      r"\role{Software Engineer (SDE 2), Multiverse Computing}{Dec 2023 -- Nov 2025}{San Sebasti\'an, Spain}",
      r"\begin{bullets}", sde2, r"\end{bullets}", "",
      r"\role{Software Engineer, Inovatyv Pvt. Ltd.}{Jun 2023 -- May 2024}{Remote, India}",
      r"\begin{bullets}", INOV, r"\end{bullets}", "",
      r"\role{Software Engineer, CodeNation, Trilogy Innovation}{Jul 2022 -- Mar 2023}{Dubai, UAE / Remote}",
      r"\begin{bullets}", CN1, CN2, r"\end{bullets}", "",
      r"\section{EDUCATION \& ACHIEVEMENTS}", EDU, "",
    ])
