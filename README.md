# OmniGen-NIM: LLM-Guarded Genomic Analysis & Visualization

An end-to-end genomic inference pipeline and interactive Streamlit dashboard integrating AlphaFold 3D protein structure visualization, batch VCF variant scoring, and LLM output guardrails to prevent numerical hallucinations.

## Key Features

- **3D Protein Structure Viewer**: Dynamic retrieval of AlphaFold PDB models via `AlphaFoldFetcher` with automatic API/version fallback handling, rendering residue-level pLDDT confidence scores via `py3Dmol`.
- **LLM Numerical Guardrail**: Integration with `NumericalGuardrail` to parse and verify LLM-generated numerical values, HGVS notations, and rsIDs against ground-truth variant payloads.
- **Batch VCF Scoring Engine**: High-throughput variant pathogenicity scoring engine (`Evo2BatchScorer`) with runtime execution and throughput tracking (`vps`).
- **Interactive Streamlit Dashboard**: Clean two-column interface for variant query configuration, 3D structure rendering, and real-time guardrail verification.

## Repository Structure

```text
OmniGen-NIM/
├── app/
│   └── dashboard.py          # Streamlit interactive Web UI
├── pipeline/
│   ├── alphafold_context.py  # AlphaFold PDB fetcher & pLDDT parser
│   └── evo2_score.py         # Batch VCF scoring engine
├── llm/
│   └── guardrail.py          # Numerical guardrail verification engine
├── data/
│   ├── alphafold_cache/      # Cached PDB files
│   └── scores/               # Output JSON results from batch scoring
├── .gitignore
└── README.md
