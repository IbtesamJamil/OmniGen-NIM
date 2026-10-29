from pipeline.celery_app import celery_app
from pipeline.alphafold_context import AlphaFoldFetcher
from pipeline.stability_estimator import StabilityEstimator
from pipeline.pathogenicity import PathogenicityEngine

fetcher = AlphaFoldFetcher()

@celery_app.task(bind=True)
def async_fetch_structure_data(self, gene_symbol: str, uniprot_id: str):
    """
    Asynchronously fetches AlphaFold structural data and confidence scores.
    """
    try:
        pdb_content = fetcher.fetch_pdb(uniprot_id)
        return {"status": "SUCCESS", "data": {"pdb_content": pdb_content, "gene": gene_symbol}}
    except Exception as exc:
        return {"status": "FAILURE", "error": str(exc)}

@celery_app.task(bind=True)
def async_compute_stability(self, sequence: str, mutation_pos: int, target_aa: str):
    """
    Asynchronously computes In Silico Mutagenesis free-energy shift.
    """
    try:
        result = StabilityEstimator.calculate_deltadelta_g(f"c.{mutation_pos}{target_aa}", 85.0)
        return {"status": "SUCCESS", "delta_g": result.get("delta_delta_g", 0.0)}
    except Exception as exc:
        return {"status": "FAILURE", "error": str(exc)}

@celery_app.task(bind=True)
def async_annotate_vcf_batch(self, variant_list: list):
    """
    Asynchronously processes and annotates a batch of variants from an uploaded VCF file.
    """
    try:
        annotated_results = []
        total = len(variant_list)
        
        for idx, var in enumerate(variant_list):
            score_data = PathogenicityEngine.evaluate_variant(
                var["chrom"], var["pos"], var["ref"], var["alt"]
            )
            annotated_results.append({**var, **score_data})
            
            # Update state for asynchronous tracking
            self.update_state(state='PROGRESS', meta={'current': idx + 1, 'total': total})
            
        return {"status": "SUCCESS", "annotated_variants": annotated_results}
    except Exception as exc:
        return {"status": "FAILURE", "error": str(exc)}