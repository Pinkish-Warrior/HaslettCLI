# Project Proposal

## Implementation Options

### 1️⃣ Architecture Options

Option A — Pure Python CLI (fastest)
 • Python CLI using Click + Jinja2 templates
 • PDF generation via WeasyPrint or wkhtmltopdf
 • YAML/JSON profiles for CV and cover letters
 • Optional: integration with Selenium/API for auto-apply

Pros: Quick prototype, easy testing, single environment
Cons: CLI-only; no graphical interface

⸻

Option B — Python backend + React frontend
 • Backend: Python FastAPI serving endpoints for CV/cover letter generation
 • Frontend: React app lets users upload YAML profile, select templates, generate/download PDFs
 • PDF generation in backend
 • Optional CLI wrapper calls backend endpoints

Pros: Modern UI, easier for non-terminal users, API allows future automation
Cons: Slower to prototype, more moving parts

⸻

Recommendation:

Start pure Python CLI (Option A) — get a fully functional tool first. Later, optionally add a React GUI that calls your Python API.

⸻

### 2️⃣ Features to include in Python prototype

 • Project init: haslettcli init
 • Add/update profiles: haslettcli add-profile PATH
 • List profiles: haslettcli list
 • Generate CV: haslettcli generate --profile backend --format pdf/html
 • Generate Cover Letter: haslettcli cover --profile backend --job "Company" --format pdf
 • Template selection: optional --template NAME
 • Tests: profile parsing, template rendering, PDF generation

⸻

### 3️⃣ Python Prototype — Full Features

Install deoendencies:

```bash
pip install click jinja2 weasyprint pyyaml
```

Project structure:

```script
HaslettCLI/
├─ haslettcli.py
├─ templates/
│   ├─ cv_template.html.j2
│   └─ cover_template.txt.j2
├─ profiles/
├─ tests/
│   └─ test_haslettcli.py
└─ README.md
└─ PROPOSAL.md
```


