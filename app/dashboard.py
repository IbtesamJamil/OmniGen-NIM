import streamlit as st
import py3Dmol
import os
import sys

# Add project root to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.alphafold_context import AlphaFoldFetcher
from llm.guardrail import NumericalGuardrail

st.set_page_config(
    page_title="OmniGen-NIM | Genomic Inference Suite",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 OmniGen-NIM: LLM-Guarded Genomic Analysis")
st.markdown("---")

# Sidebar - Variant Query
st.sidebar.header("Variant Query Config")
gene_symbol = st.sidebar.text_input("Gene Symbol", value="TP53")
uniprot_id = st.sidebar.text_input("UniProt ID", value="P04637")
hgvs_notation = st.sidebar.text_input("HGVS Variant", value="c.524G>A")
residue_pos = st.sidebar.number_input("Protein Residue Position", min_value=1, value=175)

# Initialize engines
@st.cache_data
def load_pdb(uniprot_id_val):
    fetcher = AlphaFoldFetcher()
    return fetcher.fetch_pdb(uniprot_id_val), fetcher

pdb_data, fetcher = load_pdb(uniprot_id)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("3D Protein Structure (AlphaFold)")
    if pdb_data:
        plddt = fetcher.extract_plddt(pdb_data, residue_pos)
        st.info(f"**Target Residue:** {residue_pos} | **pLDDT Score:** {plddt if plddt else 'N/A'}")
        
        # Render 3D mol view
        view = py3Dmol.view(width=500, height=400)
        view.addModel(pdb_data, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.addStyle({'resi': str(residue_pos)}, {'stick': {'colorscheme': 'redCarbon'}})
        view.zoomTo({'resi': str(residue_pos)})
        
        html_content = view._make_html()
        st.components.v1.html(html_content, height=450, scrolling=False)
    else:
        st.error(f"Could not load 3D structure for UniProt ID: {uniprot_id}")

with col2:
    st.subheader("LLM Inference & Numerical Guardrail")
    
    # Ground truth context dictionary passed to the guardrail
    payload = {
        "Gene": gene_symbol,
        "UniProt": uniprot_id,
        "HGVS": hgvs_notation,
        "Residue": residue_pos,
        "pLDDT_Confidence": plddt if pdb_data else None,
        "rsID": "rs121912651",
        "Pathogenicity_Score": 0.892
    }
    
    llm_output = st.text_area(
        "LLM Generated Summary",
        value=f"The missense variant {hgvs_notation} in {gene_symbol} ({uniprot_id}) impacts residue position {residue_pos}. "
              f"Reported pathogenicity score is 0.892 under rs121912651.",
        height=150
    )
    
    if st.button("Run Numerical Guardrail Verification"):
        is_safe = NumericalGuardrail.verify_llm_output(llm_output, payload)
        if is_safe:
            st.success("✅ Guardrail Passed: All numerical tokens, HGVS notation, and rsIDs are verified in payload.")
        else:
            st.error("❌ Guardrail Alert: Unverified or hallucinated numerical tokens detected in LLM response.")

    st.markdown("---")
    st.subheader("Variant Metrics (Ground Truth)")
    st.json(payload)