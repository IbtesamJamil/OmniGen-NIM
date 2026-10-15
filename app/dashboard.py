import streamlit as st
import py3Dmol
import os
import sys
import json
from openai import OpenAI

# Ensure project root directory is in Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.alphafold_context import AlphaFoldFetcher
from llm.guardrail import NumericalGuardrail
from app.chat_renderer import render_custom_chat_message

st.set_page_config(page_title="OmniGen-NIM | Agentic Genomic Platform", page_icon="🧬", layout="wide")

st.title("🧬 OmniGen-NIM: Agentic Genomic Analysis Platform")
st.caption("Multi-modal agentic framework combining AlphaFold 3D structure analytics, VCF pathogenicity scoring, and local LLM guardrails.")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("⚙️ Local LLM Engine (Offline)")
base_url = st.sidebar.text_input("API Base URL", value="http://localhost:11434/v1", help="Ollama local server endpoint")
model_name = st.sidebar.text_input("Model Name", value="llama3.1", help="Downloaded local Ollama model tag")
api_key = st.sidebar.text_input("API Key (Optional)", value="ollama", type="password", help="Dummy key for local OpenAI client compliance")

st.sidebar.markdown("---")
st.sidebar.header("🧠 Agent Persona Mode")
agent_persona = st.sidebar.selectbox(
    "Select Expert Persona",
    ["Structural Biologist", "Clinical Geneticist", "Bioinformatician / Python Developer"],
    help="Changes the reasoning lens and tone of the offline agent."
)

st.sidebar.markdown("---")
st.sidebar.header("🔬 Target Variant Context")
gene_symbol = st.sidebar.text_input("Gene Symbol", value="TP53")
uniprot_id = st.sidebar.text_input("UniProt ID Primary", value="P04637")
uniprot_id_compare = st.sidebar.text_input("UniProt ID Compare (Optional)", value="")
hgvs_notation = st.sidebar.text_input("HGVS Variant", value="c.524G>A")
residue_pos = st.sidebar.number_input("Protein Residue Position", min_value=1, value=175)

fetcher = AlphaFoldFetcher()

@st.cache_data
def get_structure_data(u_id):
    if not u_id:
        return None, None
    pdb_data = fetcher.fetch_pdb(u_id)
    return pdb_data, fetcher

pdb_primary, _ = get_structure_data(uniprot_id)
plddt_primary = fetcher.extract_plddt(pdb_primary, residue_pos) if pdb_primary else None

# Helper for Dynamic pLDDT Confidence Badge Styling
def get_plddt_badge(score):
    if score is None:
        return "N/A", "#64748b"
    if score >= 90:
        return f"Very High Confidence ({score}) — Ultra Stable", "#10b981"
    elif score >= 70:
        return f"Confident ({score}) — Solid Prediction", "#3b82f6"
    elif score >= 50:
        return f"Low Confidence ({score}) — Flexible Region", "#f59e0b"
    else:
        return f"Very Low Confidence ({score}) — Unstructured", "#ef4444"

col_left, col_right = st.columns([1, 1])

# --- LEFT COLUMN: 3D STRUCTURAL INSPECTION ---
with col_left:
    st.subheader("🖼️ 3D Structural Inspection")
    
    if plddt_primary is not None:
        badge_text, badge_color = get_plddt_badge(plddt_primary)
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.6); border-left: 5px solid {badge_color}; padding: 10px 14px; border-radius: 6px; margin-bottom: 12px;">
            <span style="font-size: 13px; color: #94a3b8; text-transform: uppercase; font-weight: bold;">AlphaFold Metrics (Residue {residue_pos})</span><br>
            <span style="font-size: 15px; font-weight: 600; color: #f8fafc;">pLDDT Score: <span style="color: {badge_color};">{badge_text}</span></span>
        </div>
        """, unsafe_allow_html=True)

    if uniprot_id_compare:
        tab1, tab2 = st.tabs([f"Primary ({uniprot_id})", f"Compare ({uniprot_id_compare})"])
        
        with tab1:
            if pdb_primary:
                view = py3Dmol.view(width=450, height=380)
                view.addModel(pdb_primary, 'pdb')
                view.setStyle({'cartoon': {'color': 'spectrum'}})
                view.addStyle({'resi': str(residue_pos)}, {'stick': {'colorscheme': 'redCarbon'}})
                view.zoomTo({'resi': str(residue_pos)})
                st.components.v1.html(view._make_html(), height=400)
                
        with tab2:
            pdb_compare, _ = get_structure_data(uniprot_id_compare)
            if pdb_compare:
                plddt_compare = fetcher.extract_plddt(pdb_compare, residue_pos)
                st.info(f"Compare Residue {residue_pos} | pLDDT Confidence: **{plddt_compare}**")
                view2 = py3Dmol.view(width=450, height=380)
                view2.addModel(pdb_compare, 'pdb')
                view2.setStyle({'cartoon': {'color': 'cyan'}})
                view2.addStyle({'resi': str(residue_pos)}, {'stick': {'colorscheme': 'yellowCarbon'}})
                view2.zoomTo({'resi': str(residue_pos)})
                st.components.v1.html(view2._make_html(), height=400)
    else:
        if pdb_primary:
            view = py3Dmol.view(width=500, height=420)
            view.addModel(pdb_primary, 'pdb')
            view.setStyle({'cartoon': {'color': 'spectrum'}})
            view.addStyle({'resi': str(residue_pos)}, {'stick': {'colorscheme': 'redCarbon'}})
            view.zoomTo({'resi': str(residue_pos)})
            st.components.v1.html(view._make_html(), height=450)

# --- RIGHT COLUMN: CONVERSATIONAL AGENT & TRACE ---
with col_right:
    st.subheader(f"🤖 Offline Agent ({agent_persona})")
    
    ground_truth_payload = {
        "Gene": gene_symbol,
        "UniProt": uniprot_id,
        "HGVS": hgvs_notation,
        "Residue": residue_pos,
        "pLDDT": plddt_primary,
        "Persona": agent_persona
    }

    # Agent Execution Trace
    with st.expander("⚙️ Agent Execution Trace & Pipeline Status"):
        st.markdown(f"""
        * **Step 1: Data Acquisition** — UniProt ID `{uniprot_id}` resolved.
        * **Step 2: Structural Extraction** — AlphaFold PDB model loaded; Residue `{residue_pos}` extracted (pLDDT: **{plddt_primary}**).
        * **Step 3: Persona Lens** — Active Mode: **{agent_persona}**.
        * **Step 4: Guardrail Status** — `NumericalGuardrail` active and monitoring local inference.
        """)

    with st.expander("📊 Live Ground Truth Payload (Guardrail Reference)"):
        st.json(ground_truth_payload)

    # Dynamic Quick Prompt Chips based on Selected Persona
    st.markdown("**Quick Prompts:**")
    q_col1, q_col2, q_col3 = st.columns(3)
    preset_prompt = None

    if agent_persona == "Structural Biologist":
        p1_label, p1_text = "🧬 Folding Stability", f"Analyze the local 3D folding and hydrogen bonding network around residue {residue_pos}."
        p2_label, p2_text = "🔬 pLDDT Confidence", f"What does the pLDDT score of {plddt_primary} indicate about the structural rigidity of this region?"
        p3_label, p3_text = "⚛️ Side-Chain Interactions", f"How do electrostatic interactions at residue {residue_pos} affect protein conformation in {gene_symbol}?"
    elif agent_persona == "Clinical Geneticist":
        p1_label, p1_text = "🏥 Pathogenicity Impact", f"How does variant {hgvs_notation} disrupt tumor suppression and relate to clinical phenotypes in {gene_symbol}?"
        p2_label, p2_text = "⚠️ Functional Loss", f"What is the clinical significance of mutations occurring at residue {residue_pos}?"
        p3_label, p3_text = "🩺 Disease Association", f"Discuss the oncogenic consequences and loss-of-function risks associated with {hgvs_notation}."
    else:  # Bioinformatician / Python Developer
        p1_label, p1_text = "💻 API Data Pipeline", f"How can we programmatically fetch and parse AlphaFold coordinates for UniProt ID {uniprot_id} using Python?"
        p2_label, p2_text = "⚙️ Structural Parsing", f"Write a python snippet using Biopython or PDB parser to inspect residue {residue_pos}."
        p3_label, p3_text = "📊 Guardrail Metrics", f"Explain how programmatic validation checks coordinate payloads against local LLM inferences."

    with q_col1:
        if st.button(p1_label):
            preset_prompt = p1_text
    with q_col2:
        if st.button(p2_label):
            preset_prompt = p2_text
    with q_col3:
        if st.button(p3_label):
            preset_prompt = p3_text

    # Session state initialization with reset support & sanitization
    if "messages" not in st.session_state or st.sidebar.button("🧹 Clear Chat Session"):
        st.session_state.messages = [
            {"role": "assistant", "content": f"Hello! I am your OmniGen-NIM Offline AI Agent operating as a **{agent_persona}**. Active Context: **{hgvs_notation}** in **{gene_symbol}** ({uniprot_id}). Ask me anything about biology, programming, or structural metrics!"}
        ]

    # Clean any accidental stray </div> tags from history
    for msg in st.session_state.messages:
        if "</div>" in msg["content"] and not msg["content"].strip().startswith("<div"):
            msg["content"] = msg["content"].replace("</div>", "")

    # Render previous conversation history using custom renderer module
    for msg in st.session_state.messages:
        footer = f"<br><br><span style='font-size: 11px; color: #10b981;'>🛡️ Verified by NumericalGuardrail</span>" if msg["role"] == "assistant" and "Hello!" not in msg["content"] else ""
        render_custom_chat_message(msg["role"], msg["content"], footer)

    # Handle user interaction (typed input or clicked quick prompt)
    user_prompt = st.chat_input("Ask a question...")
    if preset_prompt:
        user_prompt = preset_prompt

    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        render_custom_chat_message("user", user_prompt)

        with st.chat_message("assistant"):
            try:
                client = OpenAI(
                    api_key=api_key if api_key else "ollama",
                    base_url=base_url
                )
                
                persona_instructions = {
                    "Structural Biologist": "Focus on 3D folding, hydrogen bonding, electrostatic interactions, and structural stability around target residues.",
                    "Clinical Geneticist": "Focus on pathogenicity, variant impact, clinical phenotype associations, and loss-of-function consequences in oncology/disease.",
                    "Bioinformatician / Python Developer": "Focus on computational pipelines, API extraction, AlphaFold DB structures, programmatic metrics, and script automation."
                }
                
                system_prompt = (
                    f"You are OmniGen-NIM, an expert conversational AI agent in computational biology and genomics.\n"
                    f"Active Persona Mode: {agent_persona}. {persona_instructions.get(agent_persona, '')}\n"
                    f"Active Context: Gene={gene_symbol}, UniProt={uniprot_id}, HGVS={hgvs_notation}, Residue={residue_pos}, pLDDT={plddt_primary}.\n"
                    f"Provide clear, concise explanations suited to your persona. "
                    f"When referencing target structural metrics, strictly state residue {residue_pos} and pLDDT score {plddt_primary}. "
                    f"Keep responses punchy and direct."
                )
                
                messages_for_api = [{"role": "system", "content": system_prompt}] + [
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ]
                
                # Optimized streaming API request with chunk batching for ultra-fast performance
                stream = client.chat.completions.create(
                    model=model_name,
                    messages=messages_for_api,
                    temperature=0.2,
                    max_tokens=250,
                    stream=True
                )
                
                full_response_text = ""
                response_container = st.empty()
                chunk_counter = 0
                
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response_text += chunk.choices[0].delta.content
                        chunk_counter += 1
                        if chunk_counter % 3 == 0:
                            response_container.markdown(full_response_text + "▌")
                        
                response_container.markdown(full_response_text)

            except Exception as e:
                full_response_text = f"Failed to reach the local Ollama instance: {str(e)}"
                st.error(full_response_text)

            # Verify response via NumericalGuardrail
            is_valid = NumericalGuardrail.verify_llm_output(full_response_text, ground_truth_payload)
            
            if is_valid:
                st.caption("🛡️ **Response status:** Verified by `NumericalGuardrail` against ground-truth payload.")
                st.session_state.messages.append({"role": "assistant", "content": full_response_text})
            else:
                st.warning("⚠️ **Guardrail Interception:** Unverified structural coordinates detected! Response flagged.")

    # Export Chat Session Button
    if len(st.session_state.messages) > 1:
        st.sidebar.markdown("---")
        chat_export = json.dumps({"payload": ground_truth_payload, "history": st.session_state.messages}, indent=2)
        st.sidebar.download_button(
            label="📥 Export Session Report",
            data=chat_export,
            file_name=f"OmniGen_NIM_{gene_symbol}_{hgvs_notation}_report.json",
            mime="application/json"
        )