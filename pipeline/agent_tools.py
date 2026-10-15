import os
import json
from langchain.tools import tool
from pipeline.alphafold_context import AlphaFoldFetcher
from pipeline.evo2_score import Evo2BatchScorer

fetcher = AlphaFoldFetcher()
scorer = Evo2BatchScorer()

@tool
def fetch_protein_structure_tool(uniprot_id: str) -> str:
    """Fetches PDB structural data for a given UniProt ID from AlphaFold DB."""
    pdb_file = fetcher.fetch_pdb(uniprot_id)
    if pdb_file:
        return f"Successfully retrieved PDB for {uniprot_id} and cached locally."
    return f"Failed to retrieve PDB for UniProt ID: {uniprot_id}"

@tool
def analyze_residue_confidence_tool(uniprot_id: str, residue_pos: int) -> str:
    """Extracts the pLDDT confidence score for a specific residue position in a protein."""
    pdb_path = os.path.join("data/alphafold_cache", f"{uniprot_id}.pdb")
    if not os.path.exists(pdb_path):
        fetcher.fetch_pdb(uniprot_id)
    
    with open(pdb_path, "r") as f:
        pdb_data = f.read()
        
    plddt = fetcher.extract_plddt(pdb_data, residue_pos)
    return json.dumps({"uniprot_id": uniprot_id, "residue": residue_pos, "pLDDT": plddt})

@tool
def score_genomic_variant_tool(chrom: str, pos: int, ref: str, alt: str) -> str:
    """Scores a VCF genomic variant using the Evo2 foundation model scoring engine."""
    variants = [{"chrom": chrom, "pos": pos, "ref": ref, "alt": alt}]
    out_path = scorer.score_vcf_batch(variants)
    
    with open(out_path, "r") as f:
        results = json.load(f)
    return json.dumps(results["results"][0])