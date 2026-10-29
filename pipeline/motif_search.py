import numpy as np

class MotifSearchEngine:
    """Simulates semantic structure and motif pattern matching for proteins."""

    # Mock database of known structural motifs / functional domains
    MOTIF_DATABASE = [
        {"name": "p53 DNA-Binding Domain (Core)", "uniprot": "P04637", "residues": "94-292", "signature": "R175H, G245S, R248W", "description": "Sequence-specific DNA binding domain critical for transcriptional activation."},
        {"up_id": "P01308", "name": "Insulin Chain B Helix", "uniprot": "P01308", "residues": "9-30", "signature": "SHLVEALYLVCG", "description": "Alpha-helical segment responsible for receptor binding affinity."},
        {"name": "SH2 Domain (Generic Kinase)", "uniprot": "P00533", "residues": "120-200", "signature": "FLVRES", "description": "Recognizes phosphotyrosine-containing peptides in signal transduction."}
    ]

    @classmethod
    def search_motifs(cls, query_text: str) -> list:
        """Performs basic semantic/keyword match against structural motifs."""
        results = []
        query_lower = query_text.lower()
        for item in cls.MOTIF_DATABASE:
            if query_lower in item["name"].lower() or query_lower in item["description"].lower() or query_lower in item["signature"].lower():
                results.append(item)
        
        # Fallback if no direct match: return all or top matches for demonstration
        if not results:
            return cls.MOTIF_DATABASE[:2]
        return results