# 🏢 AI Workspace Generator

> **Autonomous Multi-Agent Enterprise Workspace Synthesizer built with CrewAI, Google Gemini, Streamlit, and SQLite.**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent%20Framework-FF4B4B?style=flat)](https://github.com/crewAIInc/crewAI)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-LLM%20Engine-4285F4?style=flat&logo=google)](https://ai.google.dev/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI%20Dashboard-FF4B4B?style=flat&logo=streamlit)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Tenant%20Storage-003B57?style=flat&logo=sqlite)](https://www.sqlite.org/)

---

## 📖 Overview

The **AI Workspace Generator** transforms the complex process of enterprise software onboarding into an automated, intelligent, and instantaneous multi-agent pipeline. 

Instead of spending weeks configuring tools, designing department dashboards, setting up role permissions, and establishing workflows, businesses complete an intuitive **8-stage onboarding interview**. A collaborative crew of specialized AI agents then digests these operational requirements, synthesizes an organization blueprint, and dynamically deploys a **live, multi-tenant, role-filtered workspace**.

---

## 🏛️ The Three Core Pillars

Our application architecture is built upon three foundational pillars:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   1. AI WORKSPACE GENERATOR                            │
│  8-Stage Onboarding  ➔  CrewAI Multi-Agent Synthesis  ➔  JSON Blueprint │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
┌──────────────────────────────────┐        ┌──────────────────────────────────┐
│       2. COMMON WORKSPACE        │        │ 3. DEPARTMENT-SPECIFIC WORKSPACE │
│ • Unified Email (Gmail/Outlook)  │        │ • Executive / CEO Overview       │
│ • Calendar & Schedule Sync       │        │ • Software Engineering & CI/CD   │
│ • Cross-Team Task Manager        │        │ • Vehicle / Fleet Operations     │
│ • Central AI Document Assistant  │        │ • Finance & Invoicing Hub        │
│ • Company Announcements          │        │ • HR & Recruitment Portal        │
└──────────────────────────────────┘        └──────────────────────────────────┘
```

1. **AI Workspace Generator (The Starting Point)**:
   The foundational intake agent that interviews the organization across 8 strategic dimensions, feeds inputs to a CrewAI agent team, builds an organization blueprint, and stores it under a dedicated tenant ID.
2. **Common Workspace (Universal Productivity)**:
   A shared digital headquarters accessible to every team member regardless of department, featuring unified communications, schedules, company notices, and an AI chat assistant.
3. **Department-Specific & Role-Filtered Workspaces**:
   Dynamic dashboards that automatically adapt depending on who logs in (e.g., CEO, HR Manager, Finance Manager, CTO, Operations Manager), enforcing least-privilege views and domain-specific widgets.

---

## 🤖 Multi-Agent Architecture (CrewAI)

The generation pipeline orchestrates five specialized autonomous agents powered by **Google Gemini**:

```
                       ┌─────────────────────────┐
                       │   Company Onboarding    │
                       │     Questionnaire       │
                       └────────────┬────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │                   CREWAI AGENT SQUAD                    │
       ├─────────────────────────┬───────────────────────────────┤
       │ 🏛️ Organization         │ Designs departments, teams,   │
       │    Architect            │ roles, and reporting lines    │
       ├─────────────────────────┼───────────────────────────────┤
       │ ⚡ Workflow             │ Builds departmental tasks,    │
       │    Specialist           │ workflows, and approvals      │
       ├─────────────────────────┼───────────────────────────────┤
       │ 🛡️ Security             │ Establishes RBAC boundaries   │
       │    Architect            │ and least-privilege access    │
       ├─────────────────────────┼───────────────────────────────┤
       │ 🔌 Integration          │ Maps required APIs (OAuth,    │
       │    Specialist           │ Slack, GitHub, Jira, etc.)    │
       ├─────────────────────────┼───────────────────────────────┤
       │ 📐 Workspace Config     │ Compiles findings into valid, │
       │    Architect            │ deterministic JSON schema     │
       └─────────────────────────┴───────────────────────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │ SQLite Tenant Database  │
                       │     (workspaces.db)     │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │   Interactive Web UI    │
                       │   (Streamlit Portal)    │
                       └─────────────────────────┘
```

- **Organization Architect**: Analyzes company headcount, offices, and operational scope to generate accurate departmental hierarchies.
- **Workflow Specialist**: Translates standard business procedures into concrete, actionable steps, approval chains, and notifications.
- **Security Architect**: Audits permissions to guarantee data segregation (e.g., restricting payroll to HR and financial statements to Finance).
- **Integration Specialist**: Identifies third-party dependencies and clearly documents authorization requirements without falsely declaring tools "connected" before credentials exist.
- **Workspace Configuration Architect**: Aggregates all structural findings into a strict JSON payload rendered by the frontend engine.

---

## 📋 The 8-Stage Onboarding Flow

The onboarding questionnaire systematically gathers all necessary business context:

| Stage | Focus Area | Key Data Captured |
|:-----:|:-----------|:------------------|
| **1** | **Company Profile & Mission** | Company name, industry, size, locations, and strategic AI goals. |
| **2** | **Structure & Hierarchy** | Departments, team leads, employee headcounts, and reporting lines. |
| **3** | **Roles & Responsibilities** | Job descriptions, operational responsibilities, and access boundaries. |
| **4** | **Existing Workflows** | Daily task triggers, approvals, cross-functional dependencies. |
| **5** | **AI & Automation Scope** | Tasks designated for full automation vs. human-in-the-loop assistance. |
| **6** | **Tools & Integrations** | Communication suites, code repositories, CRM, ERP, and cloud storage. |
| **7** | **Data Privacy & Security** | Compliance requirements, sensitive data partitions, and access control. |
| **8** | **Dashboard Preferences** | Theme preferences, layout style, priority metrics, and quick actions. |

---

## ⚡ Flagship Test Case: VoltFleet Technologies

To demonstrate the full depth of the system, a pre-configured enterprise test case is included: **VoltFleet Technologies** (an electric commercial fleet management startup).

- **Departments**: Software Development, Vehicle Operations, Customer Support, Sales & Marketing, HR, Finance, IT Administration.
- **Roles Evaluated**: CEO, CTO, Operations Manager, Support Manager, HR Manager, Finance Manager, IT Head.
- **Testing**: Use the **"Load VoltFleet example"** button on the onboarding screen to instantly populate all 8 stages with a rich, realistic dataset.

---

## 📁 Repository Structure

```
Ai-agent-ai-workspace-generator/
│
├── .env.example                # Template configuration for environment variables
├── .gitignore                  # Git ignore rules for virtual environments, secrets, databases
├── requirements.txt            # Python dependencies (Streamlit, CrewAI, google-genai, etc.)
├── README.md                   # Complete project documentation and guide
├── README.txt                  # Original developer reference sheet
│
├── app.py                      # Interactive CLI entrypoint for terminal generation
├── frontend.py                 # Primary Streamlit application (Onboarding, Generator, Dashboard)
│
├── config.py                   # LLM & Gemini model initialization
├── agents.py                   # CrewAI agent definitions
├── tasks.py                    # CrewAI task specifications and prompts
├── crew.py                     # Crew assembly, execution, and JSON parser
├── storage.py                  # SQLite multi-tenant database manager
├── workspace_builder.py        # Role-based view aggregator & dashboard data generator
├── assistant_chat.py           # Contextual AI assistant chatbot handler
│
├── docs/                       # Project documentation & reference briefs
│   └── features and test 1.docx # System architecture, question rubrics, and test specs
│
├── examples/                   # Sample outputs and payloads
│   └── workspace_blueprint.txt # Example generated JSON blueprint for VoltFleet
│
├── tests/                      # Diagnostic and verification test suite
│   ├── __init__.py
│   └── test_gemini.py          # Gemini API connectivity and response validation
│
└── tools/                      # Custom CrewAI tools directory
    └── __init__.py
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Python 3.12** (Recommended: Python 3.12 64-bit for pre-built wheel compatibility on Windows/macOS/Linux).
- A **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).

### 2. Clone the Repository
```bash
git clone -b ai-workspace-generator https://github.com/samskruthi18/Ai-agent.git
cd Ai-agent
```

### 3. Create a Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and add your Gemini API key:
```bash
cp .env.example .env
```
Open `.env` and configure:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini/gemini-3.5-flash-lite
```

### 5. Verify Gemini Connection
Run the diagnostic script to ensure your API key and network can communicate with Google Gemini:
```bash
python tests/test_gemini.py
```
*Expected output:*
```
API key loaded.
Connecting to Gemini...

SUCCESS!
Gemini is working!
```

---

## 💻 Running the Application

### Option A: Streamlit Interactive Web Application (Recommended)
Launch the full graphic user interface:
```bash
streamlit run frontend.py
```
Open your browser at **`http://localhost:8501`**.

#### User Workflow:
1. Complete the 8 onboarding steps or click **"Load VoltFleet example"**.
2. Click **"Generate My Workspace"** to trigger the CrewAI agents.
3. Upon completion, log in to the generated company workspace.
   - **Demo Password**: `1234`
4. Select any generated role (e.g., CEO, HR Manager, Finance Manager, CTO) to inspect the tailored view.
5. Interact with the contextual **AI Workspace Assistant** directly in the sidebar.

---

### Option B: Terminal CLI Generator
For running headless blueprint generation directly in your console:
```bash
python app.py
```
Enter your company description and requirements. The generated blueprint will be displayed in the terminal and saved to `workspace_blueprint.txt`.

---

## 🔒 Security & Prototype Notes

- **Demo Credentials**: The shared password `1234` is strictly for demonstration purposes in this local prototype.
- **Tenant Isolation**: Each company is persisted as an isolated SQLite record identified by a UUID `tenant_id`.
- **Integrations**: Third-party services (Slack, Jira, GitHub, Gmail) are modeled in state as `NOT CONNECTED` until live OAuth workflows and API secrets are configured.
- **Role Switching**: Role selection in the prototype demonstrates dynamic UI adaptation and RBAC layout filtering; a production system requires distinct user accounts, hashed passwords, session cookies, and backend authorization guards.

---

## 👥 Contributors & Credits

Developed as part of the **Agentic AI** initiative exploring multi-agent enterprise automation with CrewAI and Google Gemini.

