import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any

class LocalRAGEngine:
    # Curated knowledge base enriched with structural metadata & domain ranges
    KNOWLEDGE_BASE = [
        {
            "id": "kb_tp53_1",
            "text": "TP53 missense mutations occurring in the DNA-binding domain (residues 100-300), such as R175H, frequently disrupt structural zinc coordination and destabilize folding architecture, leading to complete loss of tumor suppressor function and dominant-negative effects in oncology.",
            "gene": "TP53",
            "domain": "DNA-binding domain",
            "residue_start": 100,
            "residue_end": 300
        },
        {
            "id": "kb_tp53_2",
            "text": "AlphaFold pLDDT confidence scores above 90 in core beta-sheets indicate high structural rigidity, whereas scores below 70 in loop regions reflect inherent conformational flexibility and susceptibility to thermal unfolding or proteolytic degradation.",
            "gene": "GENERIC",
            "domain": "loop_regions",
            "residue_start": None,
            "residue_end": None
        },
        {
            "id": "kb_clinvar_1",
            "text": "Pathogenic variants in ClinVar demonstrate significant positive correlation with predicted folding free energy changes (delta delta g greater than 2.0 kcal/mol), indicating that thermodynamic destabilization is a primary driver of pathogenicity.",
            "gene": "GENERIC",
            "domain": "thermodynamics",
            "residue_start": None,
            "residue_end": None
        },
        {
            "id": "kb_pipeline_1",
            "text": "OmniGen-NIM combines asynchronous Celery workers, SQLite audit trails, and strict NumericalGuardrails to verify that all local LLM generations accurately reflect underlying structural metrics.",
            "gene": "INFRA",
            "domain": "pipeline",
            "residue_start": None,
            "residue_end": None
        }
    ]

    @classmethod
    def query_knowledge_base(cls, query_text: str, target_gene: str = None, target_residue: int = None, top_k: int = 2) -> List[Dict[str, Any]]:
        corpus = [item["text"] for item in cls.KNOWLEDGE_BASE]
        vectorizer = TfidfVectorizer().fit(corpus + [query_text])
        
        corpus_vectors = vectorizer.transform(corpus)
        query_vector = vectorizer.transform([query_text])
        
        # Base TF-IDF semantic similarities
        similarities = cosine_similarity(query_vector, corpus_vectors).flatten()
        
        scored_results = []
        for idx, item in enumerate(cls.KNOWLEDGE_BASE):
            base_score = float(similarities[idx])
            
            # Apply structural metadata boosting & gene matching
            boost = 0.0
            if target_gene and item["gene"].lower() == target_gene.lower():
                boost += 0.25
            
            # Check if target residue falls within the documented structural domain range
            if target_residue and item["residue_start"] and item["residue_end"]:
                if item["residue_start"] <= target_residue <= item["residue_end"]:
                    boost += 0.40  # Significant boost for domain coordinate alignment
            
            final_score = base_score + boost
            
            if final_score > 0.05:  # Relevance threshold
                scored_results.append({
                    "source_id": item["id"],
                    "text": item["text"],
                    "gene": item["gene"],
                    "domain": item.get("domain", "general"),
                    "score": round(float(final_score), 4)
                })
                
        # Dynamic Re-ranking & sorting by final hybrid score
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:top_k]