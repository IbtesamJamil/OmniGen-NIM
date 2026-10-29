Markdown# OmniGen-NIM: Guarded Agentic Bioinformatics Platform

Official Repository: [https://github.com/IbtesamJamil/OmniGen-NIM](https://github.com/IbtesamJamil/OmniGen-NIM)

**OmniGen-NIM** is a research prototype designed to bridge LLM reasoning (via **Nebius Token Factory** and **Nemotron** models) with rigid structural and genomic ground-truth validation. Standard LLMs frequently hallucinate mutation coordinates, residue numbers, and clinical effect probabilities. OmniGen-NIM intercepts raw model outputs, runs them against Ensembl VEP ground-truth payloads, evaluates 3D spatial neighborhood burial proxies via AlphaFold PDB files, and logs all transactions to a tamper-evident SQLite SHA-256 hash-chaining audit ledger.

> **RESEARCH PROTOTYPE — FOR RESEARCH USE ONLY.** Not validated for clinical diagnostic use.

---

## Streamlit UI & Multi-Phase Dashboard Architecture

```ascii
┌────────────────────────────────────────────────────────────────────────┐
│                        Streamlit Multi-Panel Interface                 │
├──────────────────┬─────────────────┬─────────────────┬─────────────────┤
│  LLM Engine      │  Agent Persona  │  3D Structural  │  Phase 3-5      │
│  (Token Factory  │  (Structural    │  Inspection     │  (VCF Ingestion │
│   + Nemotron)    │   Biologist)    │  (AlphaFold pLDDT│ & Batch Dossier│
│                  │                 │   & PAE Matrix) │  Archiving)     │
└──────────────────┴─────────────────┴─────────────────┴─────────────────┘
LLM Engine & Model Tiering (llm/token_factory_client.py): Integrates Nebius Token Factory with dynamic Nemotron model tier selection (e.g., nano, super, ultra) and tracking of inference latency.Agent Persona Modes (pipeline/agent_guard.py): Configurable expert persona modes (such as Structural Biologist) driving multi-agent pathogenicity debates and reasoning traces.3D Structural Inspection (pipeline/structural_neighborhood.py): Renders interactive 3D protein structures via Biopython, calculating 8.0 Å Cα Euclidean distance thresholds as a structural burial proxy (Buried Core vs. Exposed Surface/Loop) and flagging AlphaFold pLDDT confidence scores (e.g., $>96$ Ultra Stable) and PAE matrices.Phase 3-5 Workflow Pipelines (pipeline/vcf_parser.py, batch_processor.py, tasks.py):Phase 3: Patient VCF batch file ingestion (up to 200MB per file).Phase 4: Clinical PDF dossier generation stamped with verified tamper-evident audit hashes.Phase 5: Asynchronous background Celery worker archiving and execution control.Complete Module & Directory BreakdownPlaintextOmniGen-NIM/
├── app/
│   ├── chat_renderer.py        # Streamlit chat message & agent trace rendering
│   └── dashboard.py            # Streamlit UI multi-panel main dashboard
├── data/
│   └── alphafold_cache/        # Pre-cached AlphaFold PDB structures (e.g., P04637.pdb)
├── llm/
│   ├── guardrail.py            # Numerical and coordinate verification logic
│   └── token_factory_client.py # Nebius Token Factory & Nemotron model routing
├── pipeline/
│   ├── agent_guard.py          # Agentic safety and error-correction loops
│   ├── agent_tools.py          # Core agent operational toolset
│   ├── alphafold_context.py    # AlphaFold confidence & spatial metrics parser
│   ├── annotate.py             # Genomic annotation pipeline connector
│   ├── api_client.py           # Unified external API communication client
│   ├── audit_ledger.py         # SHA-256 hash-chaining SQLite audit ledger
│   ├── batch_processor.py      # Bulk VCF and variant batch handling
│   ├── benchmark_runner.py     # Guardrail evaluation & metrics runner
│   ├── celery_app.py           # Celery background broker configuration
│   ├── evidence.py             # Evidence card structuring & validation
│   ├── evo2_score.py           # Evolutionary scoring integration
│   ├── mcp_server.py           # Model Context Protocol server integration
│   ├── motif_search.py         # Functional protein domain & motif search
│   ├── pathogenicity.py        # Pathogenicity scoring & analysis module
│   ├── pdf_exporter.py         # Exporter utilities for clinical PDFs
│   ├── pdf_generator.py        # ReportLab PDF generator with hash stamps
│   ├── rag_engine.py           # TF-IDF knowledge base document retrieval
│   ├── stability_estimator.py  # In silico mutagenesis & ΔΔG estimation
│   ├── structural_neighborhood.py # 8.0Å Cα contact & burial proxy analyzer
│   ├── tasks.py                # Celery background worker tasks
│   ├── tavily_connector.py     # Scoped biomedical literature retrieval
│   ├── uniprot_motifs.py       # UniProt structural motif mapping
│   ├── vcf_parser.py           # Variant Call Format file parser
│   ├── vep_client.py           # Ensembl VEP client interface
│   └── vep_connector.py        # Ensembl VEP ground truth connector
├── tests/
│   ├── test_guardrail.py       # Core verification unit tests
│   └── test_motif_search.py    # Motif index & lookup unit tests
├── Dockerfile                  # Containerization setup
├── run.bat                     # Single-click master Windows startup script
├── requirements.txt            # Python dependencies
└── README.md
Benchmark Metrics (30-Case Evaluation Suite)To measure the effectiveness of the numerical and structural guardrails against raw Nemotron generations, a benchmark suite of 30 clinical variant test cases was executed.MetricRaw Nemotron (Unconstrained)OmniGen-NIM (Guarded Pipeline)Coordinate Hallucination Rate16.7% (5 / 30 cases)0.0% (0 / 30 cases)Guardrail Catch RateN/A100.0%False-Positive Rejection RateN/A0.0% (No valid variants blocked)Mean Inference Latency (Token Factory)~1.2s~1.4s (includes guardrail validation)Installation & Local Setup1. Clone & Configure EnvironmentBashgit clone [https://github.com/IbtesamJamil/OmniGen-NIM.git](https://github.com/IbtesamJamil/OmniGen-NIM.git)
cd OmniGen-NIM
python -m venv venv_clean
venv_clean\Scripts\activate
pip install -r requirements.txt
2. Configure Environment Variables (.env)Set up your root .env file with your Nebius Token Factory credentials:Code snippetTOKEN_FACTORY_API_KEY=your_token_factory_key_here
TOKEN_FACTORY_BASE_URL=[https://api.tokenfactory.nebius.com/v1/](https://api.tokenfactory.nebius.com/v1/)
3. Run the Test SuiteVerify core module integrity (guardrails, audit ledger, motif search, spatial analyzer):Bashpython -m unittest discover tests
4. Single-Click Launch (run.bat)Use the automated run.bat master launcher script to switch to the workspace drive, activate your clean virtual environment, spin up the Celery background worker (using the solo execution pool on SQLite broker), and boot the Streamlit Dashboard simultaneously:DOSrun.bat
Alternatively, run them manually in separate terminals:DOS# Terminal 1: Celery Worker
celery -A pipeline.celery_app worker --loglevel=info -P solo

# Terminal 2: Streamlit UI
streamlit run app/dashboard.py