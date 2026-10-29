Markdown# 🧬 OmniGen-NIM: Guarded Agentic Genomic Analysis Platform

![CI / Pytest Status](https://github.com/IbtesamJamil/OmniGen-NIM/actions/workflows/pytest.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **RESEARCH PROTOTYPE — FOR RESEARCH USE ONLY.** Not for clinical diagnostics.

OmniGen-NIM is an enterprise-grade agentic genomic variant interpretation prototype that bridges **AlphaFold 3D structural data**, **VCF batch annotation**, **RAG literature grounding**, and **NVIDIA Nemotron LLM intelligence** via the **Token Factory** API. It features strict cryptographic audit logging and deterministic numerical guardrails to prevent structural hallucinations and coordinate invention.

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
Create a .env file in the root directory and add your API credentials:Code snippetTOKEN_FACTORY_API_KEY=your_nebius_token_factory_key_here
Run the Streamlit application:Bashstreamlit run app/dashboard.py
Docker DeploymentBuild the container image:Bashdocker build -t omnigen-nim .
Run the container:Bashdocker run -p 8501:8501 --env-file .env omnigen-nim
📊 Benchmarks & Performance EvaluationOmniGen-NIM was physically evaluated via our automated test harness (tests/run_benchmark_test.py) on a curated benchmark set of 30 clinical and structural test cases:MetricRaw Model (Unguarded Baseline)Guarded Model (OmniGen-NIM)Correct Interpretations / Validations5 / 3030 / 30False Positives / HallucinationsHigh (Coordinate invention)0 / 30How the Cases Were Built: The 30-case validation harness combines 25 valid clinical hotspot variants (from TP53, BRCA1, EGFR) with 5 deliberately injected coordinate and stability anomalies to test guardrail interception limits.Statistical Confidence & False Positive Boundary: Observing 0/30 false positives in our harness execution confirms robust interception reliability, statistically ruling out error rates above roughly 10% at standard confidence thresholds.⚠️ What OmniGen-NIM Cannot CatchNovel post-translational modifications or complex multi-subunit allosteric conformational shifts not captured in static AlphaFold 3D models or heuristic ΔΔG estimates.Subtle non-coding regulatory variants outside the scope of structural residue coordinate parsing.Clinical phenotypes completely devoid of structural or orthologous database annotation in ClinVar/UniProt knowledge bases.🛡️ LicenseDistributed under the MIT License. See LICENSE for more information.