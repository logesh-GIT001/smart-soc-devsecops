# Smart-SOC DevSecOps Pipeline

> DevSecOps pipeline for Smart-SOC — Bandit SAST → pytest → Docker multi-stage build → Trivy CVE scan → Docker Compose deploy. Security gates at every stage. Built with GitHub Actions.

**Security doesn't start at deployment — it starts at commit.**

A production-grade DevSecOps pipeline for the Smart-SOC ML-based threat triage API. Every push to `main` runs a full 6-stage security-first CI/CD workflow before a single container reaches production.

Built a 6-stage DevSecOps CI/CD pipeline integrating static application security testing (Bandit), container vulnerability scanning (Trivy), unit testing with coverage gates, and automated deployment via Docker Compose — all orchestrated through GitHub Actions. Every commit to main triggers the full security pipeline before any code reaches production. Designed to demonstrate security-first engineering practices for SOC and DevSecOps roles.

---

## Pipeline Architecture

```
  Push to GitHub
       │
       ▼
┌─────────────────┐
│  Stage 1: LINT  │  flake8 + black — code quality gate
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Stage 2: SAST  │  Bandit — static security analysis on source code
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Stage 3: TEST  │  pytest + coverage — unit tests must pass ≥70%
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Stage 4: BUILD │  Docker multi-stage build (non-root, minimal image)
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  Stage 5: TRIVY SCAN │  CVE scan — fails pipeline on CRITICAL unfixed vulns
└────────┬─────────────┘
         │
         ▼
┌──────────────────┐
│  Stage 6: DEPLOY │  Docker Compose deploy + smoke tests (main branch only)
└──────────────────┘
```

---

## Security Controls

| Control | Tool | What It Catches |
|---|---|---|
| SAST | Bandit | Hardcoded secrets, insecure functions, injection risks |
| Container CVE scan | Trivy | Known CVEs in OS packages and Python deps |
| Non-root container | Dockerfile | Privilege escalation inside container |
| Multi-stage build | Dockerfile | Reduces attack surface — no build tools in runtime image |
| Smoke tests | curl | Verifies API is live and responding correctly post-deploy |

---

## Running Locally

```bash
# Clone the repo
git clone https://github.com/logesh-GIT001/smart-soc-devsecops.git
cd smart-soc-devsecops

# Build and run
docker compose up --build

# Test the API
curl http://localhost:8000/health

curl -X POST http://localhost:8000/triage \
  -H "Content-Type: application/json" \
  -d '{
    "src_ip": "192.168.1.100",
    "dst_ip": "10.0.0.1",
    "protocol": "TCP",
    "bytes_sent": 100000,
    "packets": 5000,
    "duration": 0.5
  }'
```

---

## Run Pipeline Stages Manually

```bash
# Install dev dependencies
pip install flake8 black bandit pytest pytest-cov httpx
pip install -r app/requirements.txt

# Lint
flake8 app/ --max-line-length=100
black --check app/

# SAST
bandit -r app/ --severity-level medium

# Tests
cd app && pytest test_main.py -v --cov=. --cov-report=term-missing

# Build image
docker build -t smart-soc-api:local .

# Container scan (requires Trivy installed)
trivy image --severity HIGH,CRITICAL smart-soc-api:local
```

---

## Project Structure

```
smart-soc-devsecops/
├── .github/
│   └── workflows/
│       └── devsecops.yml     # Full 6-stage pipeline
├── app/
│   ├── main.py               # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   └── test_main.py          # Unit tests
├── Dockerfile                # Multi-stage, non-root build
├── docker-compose.yml        # Local deployment
└── README.md
```

---

## About Smart-SOC

Smart-SOC is an ML-powered threat triage system built for SOC environments. It uses XGBoost to classify network traffic into attack categories and SHAP to explain why each alert was flagged — giving L1 analysts readable reasoning without requiring a data science background.

**Stack:** Python · FastAPI · XGBoost · SHAP · Docker · GitHub Actions · Trivy · Bandit

---

*Built by [Logeshwaran S](https://logesh-git001.github.io/loki/) — Cybersecurity Analyst · DevSecOps*
