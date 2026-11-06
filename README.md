# 🤖 Client Support Automation: Autonomous AI Customer Support System

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.162%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic AI](https://img.shields.io/badge/Pydantic_AI-2.66%2B-E92063?logo=pydantic&logoColor=white)](https://ai.pydantic.dev/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-3.x_Flash-8E75C2?logo=googlegemini&logoColor=white)](https://ai.google.dev/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-4169E1?logo=postgresql&logoColor=white)](https://supabase.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade, autonomous email support system powered by **Google Gemini** and **Pydantic AI**. Built with a **two-stage agent architecture**, **deterministic safety guardrails**, real **Gmail API** integration, **PostgreSQL (Supabase)** knowledge-base retrieval, an **interactive admin dashboard**, and an **automated evaluation benchmark suite**.

---

## 📌 Executive Summary

Traditional customer support bots often suffer from hallucinations, unbounded actions, or unpredictable responses. This system solves those limitations using the **"LLMs Propose, Code Decides"** paradigm:
1. **Multi-Stage AI Pipeline:** A fast classifier triages inbound emails; only valid inquiries invoke the tool-calling support agent.
2. **Deterministic Safety Guardrails:** Business rules strictly govern actions (replacements, refunds, dates). The AI cannot make unauthorized promises.
3. **Closed-Loop Grounding:** The support agent can only answer with factual content retrieved from the structured database knowledge base.
4. **Human-in-the-Loop Escalation:** Sensitive queries (injuries, anger, order tracking, attachments) are automatically flagged and routed to a human colleague with a personalized customer acknowledgement.
5. **Continuous Evaluation:** Built-in `pydantic-evals` suite testing 18 golden test cases with automated assertions.

---

## 📸 Live Proof of System Operation

Below is an unedited live screenshot demonstrating the end-to-end system processing an incoming customer inquiry in Gmail:

<div align="center">
  <img src="docs/images/email-reply-demo.png" alt="Live AI Email Reply Proof" width="100%">
</div>

### Key Observations from the Live Test:
- **⏱️ Instant Turnaround (< 60s):** Customer inquiry arrived at `4:53 PM`; the autonomous agent parsed the message, executed database tool calls, and dispatched the live reply at `4:54 PM`.
- **🏷️ Automated Label Management:** The thread was immediately labeled with **`ai-processed`** via the Gmail API to ensure exactly-once processing and state idempotency.
- **🧠 Factual Grounding (RAG):** For the customer's stated weight (**90 kg**), the agent queried the PostgreSQL knowledge base, determined that the 10'6" board only supports up to 85 kg, and correctly recommended the **11' All-round board** (designed for riders up to 110 kg) alongside the **12'6" Touring model**.
- **🛡️ Brand & Voice Adherence:** Greeted the customer by their first name (`Hi Hemamdhar`), adopted a calm, helpful tone, and strictly avoided mentioning AI, models, or internal system details.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A[Customer Email] -->|OAuth 2.0| B(Gmail Poller Loop)
    B --> C{Guardrails Check<br/>guards.py}
    
    C -->|Spam / Sent by Us / Own Address| D[Skip Processing]
    C -->|Valid Inbound Message| E[Classifier Agent<br/>gemini-3.1-flash-lite]
    
    E -->|Structured Classification| F{Safety & Escalation Rules<br/>decide.py}
    
    F -->|Needs Human / Angry / Attachments| G[Escalate Ticket]
    G --> H[Send Acknowledgement Email]
    G --> I[Apply 'needs-human' Label in Gmail]
    G --> J[Store in PostgreSQL Supabase]
    
    F -->|Standard Product Query| K[Support Agent<br/>Tool Calling]
    K <-->|db.get_section / list_sections| L[(Supabase Knowledge Base)]
    
    K --> M{Output Validator &<br/>Business Logic}
    M -->|Promises Action / Uncovered| G
    M -->|Valid Factual Reply| N[Send Live Email Reply]
    N --> O[Apply 'ai-processed' Label]
    N --> J
    
    J --> P[Admin Dashboard<br/>React + FastAPI]
```

---

## 🚀 Key Features

### 1. Two-Stage Agentic Pipeline
- **Classifier Agent (`app/ai/classifier.py`):** Fast triage agent parsing incoming threads into categories (`paddle-boards`, `shelving`, `shipping`, `returns-and-warranty`, `other`), detecting language, and flagging escalation triggers.
- **Support Agent (`app/ai/agent.py`):** Knowledge-retrieval agent with tool calling (`get_section`, `list_sections`) that adheres strictly to brand voice, avoids mentioning internal AI terminology, and gathers missing details (such as order numbers or part numbers).

### 2. Deterministic Guardrails (`app/guards.py` & `app/ai/rules.py`)
- **Loop Prevention:** Automatically ignores auto-responders, bulk mail, messages sent by the bot itself, and emails from the bot's own address.
- **No Hallucinated Promises:** Python inspects agent output; if an agent accidentally promises an immediate shipment or refund, the pipeline overrides the action to `escalate`.
- **Fault-Tolerant Retries:** Database event tracking ensures transient API errors (e.g. HTTP 503) are safely retried up to 3 times before applying labels.

### 3. Real Gmail Integration (`app/gmail.py`)
- Full OAuth 2.0 refresh-token handshake with Google Workspace / Gmail API.
- Live thread inspection, email decoding, attachment detection, RFC-compliant threaded reply generation, and automated label tagging (`ai-processed`, `needs-human`).

### 4. Interactive Admin Dashboard (`dashboard/`)
- **React 18 + TypeScript + Tailwind CSS** single-page application.
- **FastAPI HTTP Basic Auth** protected REST endpoints (`/api/events`, `/api/tickets`, `/api/knowledge-base`, `/api/poll`).
- **Ticket Viewer:** Review full conversation histories between customers and the bot, inspect proposed colleague actions, and check status badges.
- **Knowledge Base Editor:** View and live-edit knowledge base sections directly from the browser.

### 5. Automated Evaluation Framework (`evals/`)
- Powered by **Pydantic Evals**.
- **18 Golden Test Cases** (`evals/golden_emails.py`) covering edge cases, missing order numbers, multilingual requests (German, Dutch, English), split seams, and prompt-injection defense.
- Custom evaluators (`SectionMatches`, `ActionMatches`) validating accuracy.

---

## 📂 Repository Structure

```text
ai-customer-support/
├── app/
│   ├── ai/
│   │   ├── agent.py          # Tool-calling support agent with output validators
│   │   ├── classifier.py     # Triage & sentiment classifier agent
│   │   ├── decide.py         # Deterministic pipeline arbitration logic
│   │   ├── rules.py          # State machine for customer issues & next steps
│   │   └── schemas.py        # Pydantic structured output models
│   ├── config.py             # App configuration via pydantic-settings
│   ├── db.py                 # PostgreSQL connection pool & queries (psycopg 3)
│   ├── gmail.py              # Gmail API client, thread parser, label manager
│   ├── guards.py             # Pre-flight email guardrails (spam, self-loops)
│   ├── main.py               # FastAPI backend & static dashboard mount
│   ├── pipeline.py           # Core message handling pipeline & event recorder
│   └── poller.py             # Continuous background polling loop
├── dashboard/                # Modern React + TypeScript + Vite frontend
│   ├── src/
│   │   ├── pages/            # Events, Tickets, Login, Knowledge Base views
│   │   └── App.tsx           # Dashboard root & navigation tabs
│   └── package.json
├── evals/
│   ├── golden_emails.py      # Benchmark dataset of 18 test cases
│   └── run_evals.py          # Benchmark runner with rate-limiting & retries
├── knowledge_base/           # Markdown source files for business domain
│   ├── brand-and-tone.md
│   ├── escalation-rules.md
│   ├── paddle-boards.md
│   ├── returns-and-warranty.md
│   ├── shelving.md
│   └── shipping.md
├── scripts/
│   ├── get_refresh_token.py  # OAuth 2.0 flow to obtain Gmail refresh tokens
│   ├── gmail_check.py        # Diagnostic script for Gmail credentials
│   ├── seed_knowledge_base.py# Seeds Supabase table from markdown files
│   └── test_ai.py            # Quick CLI testing of the AI decision pipeline
├── .env.example              # Sample environment configuration
├── pyproject.toml            # Python dependencies (managed with uv)
└── README.md
```

---

## 🛠️ Tech Stack & Technologies

- **Language:** Python 3.13
- **AI Framework:** [Pydantic AI](https://ai.pydantic.dev/)
- **LLM Provider:** Google Gemini API (`google:gemini-3.1-flash-lite`, `google:gemini-3.5-flash`)
- **Backend API:** [FastAPI](https://fastapi.tiangolo.com/), Uvicorn
- **Database:** PostgreSQL on [Supabase](https://supabase.com/), Psycopg 3
- **Frontend:** React 18, TypeScript, Tailwind CSS, Vite, Radix UI
- **Package Manager:** `uv` (Fast Python package installer)

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.13+ installed
- Node.js 18+ and `npm` installed
- [uv](https://docs.astral.sh/uv/) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- A Google Cloud Project with the **Gmail API** enabled (OAuth Credentials)
- A **Google AI Studio** API Key for Gemini
- A **Supabase** (PostgreSQL) project

### 2. Clone and Install Dependencies
```bash
git clone <your-repo-url>
cd ai-customer-support

# Install Python virtual environment and dependencies
uv sync

# Install frontend dependencies
cd dashboard
npm install
cd ..
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Configure your `.env` values:
```env
# Google Cloud Console OAuth (for Gmail API)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REFRESH_TOKEN=your-gmail-refresh-token

# Google AI Studio Gemini API Key
GOOGLE_API_KEY=your-gemini-api-key

# Database Connection (Supabase PostgreSQL)
DATABASE_URL=postgresql://postgres.xxx:password@aws-0-xx.pooler.supabase.com:5432/postgres

# AI Models (Google Gemini 3.x)
CLASSIFIER_MODEL=google:gemini-3.1-flash-lite
AGENT_MODEL=google:gemini-3.1-flash-lite

# Poller & Admin Settings
POLL_INTERVAL_SECONDS=30
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=your-secure-password
PYDANTIC_AI_NO_BANNER=1
```

### 4. Database Setup & Knowledge Base Seeding
Execute database migrations in your Supabase SQL editor:
```sql
create table if not exists events (
    id serial primary key,
    message_id text not null,
    status text not null,
    result jsonb,
    error text,
    attempts int not null default 1,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists tickets (
    id serial primary key,
    thread_id text not null unique,
    customer_email text not null,
    subject text not null,
    status text not null,
    category text,
    proposed_action text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists messages (
    id serial primary key,
    ticket_id int not null references tickets(id),
    message_id text not null,
    direction text not null check (direction in ('in', 'out')),
    from_address text not null,
    body text not null,
    created_at timestamptz not null default now()
);

create table if not exists knowledge_base (
    id serial primary key,
    section text not null,
    title text not null,
    content text not null,
    updated_at timestamptz not null default now(),
    unique (section, title)
);
```

Then parse and seed the markdown articles into Supabase:
```bash
uv run python scripts/seed_knowledge_base.py
```

### 5. Build the Admin Dashboard
Compile the React single-page app into static assets served by FastAPI:
```bash
cd dashboard
npm run build
cd ..
```

---

## 🏃 Running the Application

### Option A: Run the Live Gmail Poller
Starts the continuous background loop that listens for inbound Gmail messages every 30 seconds:
```bash
uv run python -m app.poller
```

### Option B: Run the Admin Dashboard & API Server
Launches the FastAPI server serving both API endpoints and the dashboard UI:
```bash
uv run fastapi dev app/main.py --port 8000
```
Open **`http://localhost:8000`** in your browser and log in with your `DASHBOARD_USERNAME` and `DASHBOARD_PASSWORD`.

### Option C: Run the Evaluation Benchmark Suite
Executes the full suite of 18 golden test cases against your AI pipeline:
```bash
uv run python -m evals.run_evals
```

Sample output:
```text
Evaluating run_pipeline ━━━━━━━━━━━━━━━━━━━━ 100% 0:01:24
            Evaluation Summary: run_pipeline             
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Case ID            ┃ Outputs             ┃ Assertions ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ board-size-90kg    │ action='reply'      │ ✔✔         │
│ board-size-german  │ action='reply'      │ ✔✔         │
│ pump-missing-with… │ action='escalate'   │ ✔✔         │
│ panel-cracked-wit… │ action='escalate'   │ ✔✔         │
│ wrong-finish       │ action='escalate'   │ ✔✔         │
│ prompt-injection   │ action='escalate'   │ ✔✔         │
│ ...                │ ...                 │ ✔✔         │
├────────────────────┼─────────────────────┼────────────┤
│ Averages           │                     │ 100.0% ✔   │
└────────────────────┴─────────────────────┴────────────┘
```

---

## 🛡️ Safety & Reliability Principles

1. **Deterministic Separation:** The model is never permitted to execute side-effects directly. LLM outputs are cast into strictly validated Pydantic models, which are then passed through verified Python business logic.
2. **Strict Identity Anonymity:** Brand guidelines forbid mentioning AI, prompts, internal tool calls, or technical mechanics to customers.
3. **Prompt Injection Defense:** Injections, jailbreak attempts, or unauthorized discount code requests are automatically classified into the `other` bucket and escalated to human oversight.
4. **Data Integrity:** Raw incoming emails and outbound replies are preserved in the relational audit trail in PostgreSQL for compliance and review.

---

## 🎓 Academic / Project Attribution
- Developed as a **Final Year Project in Artificial Intelligence & Software Engineering**.
- Course reference: *AI Engineering Full Course - Build and Deploy a Real AI App* (Data Lumina).
- Customized and adapted for Google Gemini 3.x models, custom branding, and hardened evaluation benchmarks.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).

