Markdown# 🧬 OmniGen-NIM: Guarded Agentic Genomic Analysis Platform

![CI / Pytest Status](https://github.com/IbtesamJamil/OmniGen-NIM/actions/workflows/pytest.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **RESEARCH PROTOTYPE — FOR RESEARCH USE ONLY.** Not for clinical diagnostics.

OmniGen-NIM is an enterprise-grade agentic genomic variant interpretation prototype that bridges **AlphaFold 3D structural data**, **VCF batch annotation**, **RAG literature grounding**, and **NVIDIA Nemotron LLM intelligence** via the **Token Factory** API. It features strict cryptographic audit logging and deterministic numerical guardrails to prevent structural hallucinations and coordinate invention.

---

## ⚡ Quick Evaluation for Judges (Demo Mode)
Evaluating this prototype for Devpost or review? You can launch the app and click the **"Try Demo Mode (Instant Judge Access)"** button on the login screen to instantly bypass authentication, load a pre-cached TP53 case, and explore the interactive workspace and verification panels in under 30 seconds.

---

## 🚀 Key Features

*   **3D Structural Inspection:** Real-time AlphaFold PDB structure rendering and PAE error matrix analysis.
*   **Guarded Agentic Inference:** Powered by NVIDIA Nemotron (Super, Ultra, Nano tiers) via Token Factory, protected by `NumericalGuardrail` to intercept unverified or hallucinated coordinate outputs.
*   **Tamper-Evident Audit Ledger:** Cryptographic SHA-256 hash-chain SQLite ledger logging every user action, query, and PDF report generation.
*   **Variant Report Dossier Export:** Professional ReportLab PDF generation stamped with variant metrics, burial contact-count proxy analysis, low-pLDDT residue warnings, and the audit ledger's cryptographic head hash.
*   **VCF Batch Processing:** Ingestion and automated annotation of Variant Call Format files with asynchronous Celery execution support.
*   **Multi-Agent Co-Pilot:** Automated cross-examination debates between specialized expert personas (*Structural Biologist*, *Clinical Geneticist*, *Bioinformatician*).

---

## ⚙️ Tech Stack

*   **Frontend & Dashboard:** Streamlit (Python)
*   **LLM Integration:** NVIDIA Nemotron via Token Factory API
*   **Structural & Bioinformatics Tools:** AlphaFold DB API, Py3Dmol, Biopython heuristic proxies
*   **Compliance & Storage:** SQLite tamper-evident audit ledger, ReportLab (PDF generation)
*   **Testing & CI/CD:** Pytest unit test suite with automated GitHub Actions workflows

---

## 🛠️ Installation & Setup

### Local Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/IbtesamJamil/OmniGen-NIM.git](https://github.com/IbtesamJamil/OmniGen-NIM.git)
   cd OmniGen-NIM
Create and activate a virtual environment:Bashpython -m venv venv
source venv/Scripts/activate  # On Windows use: venv\Scripts\activate
Install dependencies:Bashpip install --upgrade pip
pip install -r requirements.txt
pip install pytest
Configure environment variables:
Create a .env file in the root directory and add your API credentials:Code snippet
TOKEN_FACTORY_API_KEY=v1.CmQKHHN0YXRpY2tleS1lMDBteHcwbmdmbTlucDBrc2gSIXNlcnZpY2VhY2NvdW50LWUwMGh2bTlhcHQ1MWE0YzI1NjIMCOG38tYGEJWc3KcBOgwI27qKogcQwIX0sAFAAloDZTAw.AAAAAAAAAAHpuZTXxIkK9vUeXkjfmi2FAoLslRi9Xb2tdYHSx9mAatN6lWBb_vcu2HEQNBfjT98i4Ll2BJOCJDunwNQ7rLUL
Run the Streamlit application:Bashstreamlit run app/dashboard.py
📊 Adversarial Guardrail Evaluation & BenchmarksTo rigorously test stability and compliance, OmniGen-NIM includes an automated adversarial evaluation harness (tests/run_benchmark_test.py) comprising 30 clinical and structural test cases:MetricValid Clinical Set (25 Cases)Injected Structural Anomalies (5 Cases)Guardrail Interception / Validation25 / 25 Passed5 / 5 Intercepted & BlockedFalse Positive Rate0.0%—Testing Methodology: Run the physical evaluation harness locally using:Bashpython tests/run_benchmark_test.py
🛡️ LicenseDistributed under the MIT License. See LICENSE for more information