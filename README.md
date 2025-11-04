# HaslettCLI

**HaslettCLI** is a command-line tool designed to help you build, manage, and tailor your CVs and cover letters with the precision of an engineer and the creativity of a storyteller.

Inspired by **Dame Caroline Haslett**, a pioneering British electrical engineer and advocate for women in technology, HaslettCLI celebrates her mission to empower women through innovation.  
This CLI brings that same spirit to your career — automating the way you create, customize, and version-control your professional documents.

---

## Features

- 🧠 **Profile Management** — Store multiple CV variants (e.g., backend, data, leadership).  
- 🧩 **Smart Templates** — Generate CVs and cover letters using flexible Jinja2 templates.  
- 📄 **Multi-format Output** — Export to HTML, Markdown, or PDF.  
- ⚙️ **Command-line Simplicity** — Manage and generate with clear, developer-style commands.  
- 🔍 **ATS Optimization (coming soon)** — Automatically highlight keywords for each role.  

---

## Installation

>Clone the repository:

```bash
git clone https://github.com/yourusername/HaslettCLI.git
cd HaslettCLI
```

>Install dependencies:

```bash
pip install -r requirements.txt
```

or

```bash
python3 -m pip install click jinja2 pyyaml weasyprint
```

Example Commands

- Initialize a new HaslettCLI project:

```bash
    ./run.sh init
```

- Add or update profile:

```bash
    ./run.sh add-profile profile/backend.yml
```

- List available profiles:

```bash
    ./run.sh list_profiles
```

- Generate CV:

```bash
    # PDF output
    ./run.sh generate --profile backend.yml --format pdf --out backend_cv.pdf
    # PDF output
    ./run.sh generate --profile backend.yml --format html --out backend_cv.html
```

- Generate Cover Letter:

```bash
    ./run.sh cover --profile backend.yml --job "Awesome Company" --format pdf --out cover_letter.pdf
```

---

## 👁️‍🗨️ Vision

To empower professionals — especially women in tech — with open-source tools that combine automation, creativity, and confidence in career storytelling.

## Workflow

For a detailed explanation of the CLI's workflow, see the [WORKFLOW.md](WORKFLOW.md) file.

🗂️ Project Structure:

``` script
HaslettCLI/
├─ haslettcli.py                 # Main CLI script
├─ templates/
│  ├─ cv_template.html.j2        # CV template
│  └─ cover_template.txt.j2      # Cover letter template
├─ profiles/
│  └─ backend.yml                # Sample YAML profile
├─ tests/
│  └─ test_haslettcli.py         # Optional tests
└─ README.md
```

**Built by Tania Rosa | linkedin.com/in/tania-rosa-99503b36 | <trsdeveloper@proton.me>**

![AI Generated - Human Verified](https://img.shields.io/badge/🤖%20AI%20Generated%20%2D%20🧠%20Human%20Verified-success)
