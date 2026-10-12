---
name: master-skiller
description: "Master AI Agent Skill Orchestrator & Execution Router. Analyzes any user prompt, queries the 2,499+ indexed skill catalog in milliseconds, determines the exact tools required, and constructs chronological multi-skill execution DAG pipelines (Analysis -> Design -> Implementation -> Testing -> Security -> Growth/Audit)."
---

# Master Skiller — Universal Agent Skill Router & Pipeline Orchestrator

Master Skiller is the central brain of this workspace. Instead of polluting model context with thousands of flat skill instructions, Master Skiller provides a **hierarchical two-tier routing architecture**:
1. **High-Level Domain Taxonomy** (Instant in-context domain orientation, ~2,000 tokens).
2. **Sub-second Local Query Engine** (`master-skiller/scripts/router.py` searching `catalog.json`).
3. **Multi-Skill Execution DAG** (Deterministic chronological sequencing across stages).

---

## ⚡ Autonomous Agent Protocol (Execution Pipeline)

Whenever you receive a prompt that involves complex tasks, multiple technologies, or you are unsure which specialized workspace skill is best:

### Step 1: Run the Router CLI
Execute the router CLI with the user's prompt:
```bash
python master-skiller/scripts/router.py "<user prompt or task brief>" --top 4 --json
```

### Step 2: Parse the Generated Pipeline
The router returns a structured JSON payload containing:
- `top_skills`: Best matching specialized skills ranked by relevance and robustness score.
- `pipeline`: A sorted, chronological sequence grouped by lifecycle phase:
  1. **Phase 1: Analysis & Research** (e.g. `website-analyzer`, `video-analyzer`, `image-analyzer`)
  2. **Phase 2: UX & Design System** (e.g. `uiux-designer`, `apple-design`, `antigravity-design-expert`)
  3. **Phase 3: Architecture & Implementation** (e.g. `frontend-expert`, `3d-web-experience`, `aws-serverless-eda`)
  4. **Phase 4: Testing & QA** (e.g. `testing-patterns`, `e2e-testing`, `playwright-skill`)
  5. **Phase 5: Security & Compliance** (e.g. `sast-scanning`, `threat-modeling`, `security-audit`)
  6. **Phase 6: Growth, Marketing & Final Audit** (e.g. `copywriting`, `brag`, `humanizer`)

### Step 3: Load and Follow Selected Skills Sequentially
For each step in the pipeline:
1. Call `view_file` on `core/skills/<skill_id>/SKILL.md` to load the exact instructions for that step.
2. Execute the phase using the specialized skill's guidelines.
3. Advance to the next phase in the pipeline until delivery is complete.

---

## 🗺️ High-Level Domain Map

When reasoning about user requests, consult this domain index:

| Domain | Primary Focus | Flagship Workspace Skills |
|---|---|---|
| **UI/UX & Motion** | Palettes, typography, micro-interactions, gestures | `uiux-designer`, `apple-design`, `emil-design-eng`, `antigravity-design-expert` |
| **Frontend Frameworks** | React 19, Next.js, TypeScript, Suspense, state | `frontend-expert`, `frontend-design`, `react-best-practices` |
| **3D & WebGL** | Three.js, React Three Fiber, shaders, canvas | `3d-web-experience` |
| **Backend & APIs** | FastAPI, Node, GraphQL, REST, microservices | `python-fastapi-development`, `graphql-architect`, `nodejs-best-practices` |
| **Databases & Storage** | PostgreSQL, Neon, Redis, migrations, queries | `database-architect`, `neon-postgres`, `supabase-postgres-best-practices`, `redis-cli` |
| **Cloud & DevOps** | Docker, K8s, AWS, Cloudflare, Terraform, CI/CD | `docker-expert`, `kubernetes-architect`, `cloudflare-workers`, `terraform-specialist` |
| **Testing & QA** | Unit tests, TDD, Playwright, E2E, mock factories | `testing-patterns`, `e2e-testing`, `playwright-skill`, `tdd-workflows-tdd-cycle` |
| **Security & Audits** | SAST, threat modeling, pentesting, PCI-DSS | `security-audit`, `sast-scanning`, `threat-modeling`, `pci-dss-compliance` |
| **Multimodal Inspection**| Videos, screenshots, EXIF, Core Web Vitals | `image-analyzer`, `video-analyzer`, `website-analyzer`, `fal-upscale` |
| **AI & Agentic Tools** | Banana Claude, Gemini, prompts, MCP servers | `banana-claude`, `prompt-engineering-patterns`, `gemini-live-api-dev` |
| **Marketing & Growth** | Conversion copy, launch videos, humanizing prose | `copywriting`, `brag`, `humanizer`, `seo-aeo-schema-generator` |
| **Search & Discovery** | Algolia indexing, InstantSearch, relevance | `algolia-search`, `vector-database-ops` |
| **Browser Extensions** | Chrome/Firefox MV3, service workers, popups | `browser-extension-builder`, `reverse-browser-automation` |
| **Git & Collaboration**| Production git workflows, rebase, branch rules | `git-workflow`, `github-actions`, `performance-testing-review-ai-review` |
| **Observability** | Root-cause analysis, triage, logs, telemetry | `debugging-code`, `incident-response`, `debugging-toolkit-smart-debug` |

---

## 🛠️ CLI Reference

### Find Skills for Any Prompt
```bash
python master-skiller/scripts/router.py "<your query or prompt>"
```

### Get Structured JSON for Agent Chaining
```bash
python master-skiller/scripts/router.py "<your query>" --top 3 --json
```

### Filter by Specific Domain
```bash
python master-skiller/scripts/router.py "<query>" --domain frontend-engineering
```

### List All Indexed Domains
```bash
python master-skiller/scripts/router.py --list-domains
```
