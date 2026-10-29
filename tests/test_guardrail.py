import unittest
from llm.guardrail import NumericalGuardrail
from pipeline.uniprot_motifs import UniProtMotifIndex
from pipeline.audit_ledger import AuditLedger
from pipeline.pdf_generator import PDFReportGenerator
from pipeline.benchmark_runner import BenchmarkRunner
from pipeline.structural_neighborhood import StructuralNeighborhoodAnalyzer

class TestGuardrailEngine(unittest.TestCase):
    def setUp(self):
        self.evidence_card = {
            "Gene": "TP53",
            "Residue": 175,
            "HGVS": "c.524G>A"
        }

    def test_valid_llm_response(self):
        # Use a response that matches the evidence card's residue/HGVS
        valid_response = "TP53 variant c.524G>A at residue 175 shows stable folding."
        self.assertTrue(NumericalGuardrail.verify_llm_output(valid_response, self.evidence_card))

    def test_hallucinated_number_rejection(self):
        # A response with an unauthorized variant position should be rejected
        hallucinated_response = "BRCA1 variant c.188T>G has a 99.9% probability of disease."
        self.assertFalse(NumericalGuardrail.verify_llm_output(hallucinated_response, self.evidence_card))

    def test_uniprot_motif_lookup(self):
        match = UniProtMotifIndex.lookup_motif("TP53", 175)
        self.assertIsNotNone(match)
        self.assertEqual(match["matched_motif"], "DNA-binding domain")

    def test_audit_ledger_and_verification(self):
        AuditLedger.initialize_db()
        AuditLedger.log_action("test_user", "Admin", "TEST", "Testing ledger integrity")
        self.assertTrue(PDFReportGenerator.verify_ledger_integrity())

    def test_benchmark_runner(self):
        dummy_cases = [
            {"predicted_residue": 175, "actual_residue": 175, "guard_caught": True},
            {"predicted_residue": 999, "actual_residue": 175, "guard_caught": True}
        ]
        metrics = BenchmarkRunner.evaluate_pipeline(dummy_cases)
        self.assertEqual(metrics["total_test_cases"], 2)
        self.assertEqual(metrics["guardrail_catch_rate_pct"], 100.0)

    def test_structural_neighborhood_analyzer(self):
        analyzer = StructuralNeighborhoodAnalyzer(pdb_dir="data/alphafold_cache")
        result = analyzer.analyze_neighborhood(pdb_filename="P04637.pdb", residue_number=175, threshold_angstroms=8.0)
        self.assertNotIn("error", result)
        self.assertEqual(result["target_residue"], 175)
        self.assertEqual(result["exposure_classification"], "Buried Core (Proxy > 12 contacts)")
        self.assertGreater(result["neighborhood_count"], 0)
        self.assertIn("plddt_score", result)

if __name__ == "__main__":
    unittest.main()