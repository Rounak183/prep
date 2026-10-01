# -*- coding: utf-8 -*-
import sys; sys.path.insert(0,'/home/claude/resumes')
from body_common import *

# ---------- v1: AI Products & Full-Stack ----------
v1_skills = "\n".join([
 r"\skl{AI \& LLM Products:}{LLM-backed features, agent orchestration, RAG, embeddings \& vector search, context design, agent observability, LLM compression (CompactifAI)}",
 r"\skl{Frontend:}{Next.js, React, TypeScript, Streamlit, HTML/CSS}",
 r"\skl{Backend:}{Python, Go, FastAPI, Django, Node.js, REST, GraphQL, SQL}",
 r"\skl{Infrastructure \& Delivery:}{AWS (EKS, Lambda, SQS), Kubernetes, Helm, ArgoCD, Docker, Terraform, GitLab CI/CD, Kafka, Prometheus, Grafana, enterprise SSO (Logto, Microsoft Entra ID, AWS Cognito / OIDC)}",
 r"\skl{Data:}{PostgreSQL, MongoDB, DynamoDB, ClickHouse, Cassandra, Druid}",
])
V1_ORG = (r"\item Owned the universal platform standardising FastAPI/Next.js/Streamlit delivery across the entire "
          r"engineering organisation: product, services, DevOps and MLOps, \textbf{200+} engineers across "
          r"\textbf{15+} teams at peak. Built its Next.js template frontend, the entry point and conventions every "
          r"company app inherits; migrated auth to enterprise SSO (Logto, OIDC) fleet-wide.")
v1 = doc(r"Senior Software Engineer \textperiodcentered{} AI Products \& Full-Stack",
  r"Full-stack engineer shipping AI-powered products end to end: LLM-backed services behind FastAPI, product "
  r"surfaces in Next.js and React, and the auth, CI/CD and deployment underneath. Built an agent system "
  r"generating production-ready full-stack apps used by \textbf{200+} engineers across \textbf{15+} teams, "
  r"cutting scaffolding \textbf{70\%+} across \textbf{100+} services.",
  v1_skills, "\n".join([TA, OBS, FOUNDRY, CENTRAL]), "\n".join([V1_ORG, EKS, BRANCH, ONCALL, CI])) + ACH_NO + "\n" + r"\end{document}"

# ---------- v2: Backend & Distributed Systems ----------
v2_skills = "\n".join([
 r"\skl{Languages:}{Python, Go, TypeScript, C++, SQL}",
 r"\skl{Backend:}{FastAPI, Django, Node.js, REST, GraphQL, Kafka, AWS SQS/Lambda, async \& event-driven processing}",
 r"\skl{Infrastructure \& Reliability:}{AWS (EKS, Lambda, SQS), Kubernetes, Helm, ArgoCD, Terraform, Docker, GitLab CI/CD, Prometheus, Grafana, OpenTelemetry, ELK, enterprise SSO (Logto, Microsoft Entra ID, AWS Cognito / OIDC)}",
 r"\skl{Data:}{PostgreSQL, DynamoDB, MongoDB, ClickHouse, Cassandra, Druid}",
 r"\skl{AI Systems:}{LLM-backed services, agent orchestration, RAG, vector search, LLM compression (CompactifAI)}",
])
v2 = doc(r"Senior Software Engineer \textperiodcentered{} Backend \& Distributed Systems",
  r"Backend engineer, \textbf{4+ years} on shared platform infrastructure: \textbf{100+} production services on "
  r"Kubernetes at \textbf{99.99\%} availability, event-driven pipelines on Kafka and SQS, and the CI/CD, identity "
  r"and observability tooling used by \textbf{200+} engineers across \textbf{15+} teams.",
  v2_skills, "\n".join([FOUNDRY, TA, OBS, CENTRAL]), "\n".join([ORG, EKS, BRANCH, ONCALL, CI])) + ACH_LC + "\n" + r"\end{document}"

# ---------- v3: AI Agent Platforms & Developer Tooling ----------
v3_skills = "\n".join([
 r"\skl{AI Agent Systems:}{agent harness \& orchestration, LLM-backed services, agent observability \& evaluation, RAG, vector search, LLM compression (CompactifAI)}",
 r"\skl{Languages:}{Python, Go, TypeScript, C++, SQL}",
 r"\skl{Backend:}{FastAPI, Django, Node.js, REST, GraphQL, Kafka, AWS SQS/Lambda}",
 r"\skl{Platform \& Identity:}{shared SDKs \& templates, enterprise SSO (Logto, Entra ID, Cognito / OIDC), GitLab CI/CD, Kubernetes, Helm, ArgoCD, Terraform, AWS (EKS, Lambda, SQS)}",
 r"\skl{Product Surfaces:}{Next.js, React, Streamlit}",
 r"\skl{Observability \& Data:}{Prometheus, Grafana, OpenTelemetry, ELK, PostgreSQL, DynamoDB, ClickHouse, Druid}",
])
v3 = doc(r"Senior Software Engineer \textperiodcentered{} AI Agent Platforms \& Developer Tooling",
  r"Senior engineer building AI coding agents and the developer platform around them: a deterministic agent "
  r"pipeline that cut service scaffolding \textbf{70\%+} across \textbf{100+} services, and the shared platform "
  r"\textbf{200+} engineers build on. $\mathbf{0{\to}1}$ work, delivered directly to a \textbf{\euro{}20M} client.",
  v3_skills, "\n".join([TA, OBS, FOUNDRY, CENTRAL]), "\n".join([ORG, EKS, BRANCH, ONCALL, CI])) + ACH_LC + "\n" + r"\end{document}"

for name, src in [("v1_ai_fullstack",v1), ("v2_backend_infra",v2), ("v3_agent_platforms",v3)]:
    open(name+".tex","w").write(src)
    assert "---" not in src, name + " still has em dash"
print("generated, no em dashes")
