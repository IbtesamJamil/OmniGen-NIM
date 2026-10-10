import unittest
from llm.guardrail import NumericalGuardrail

class TestGuardrailEngine(unittest.TestCase):
    def setUp(self):
        self.evidence_card = {
            "gene_symbol": "BRCA1",
            "hgvsc": "c.188T>G",
            "evo2_delta": -24.85,
            "gnomad_af": 0.000032
        }

    def test_valid_llm_response(self):
        valid_response = "BRCA1 variant c.188T>G shows an Evo 2 score of -24.85 and AF of 0.000032."
        self.assertTrue(NumericalGuardrail.verify_llm_output(valid_response, self.evidence_card))

    def test_hallucinated_number_rejection(self):
        hallucinated_response = "BRCA1 variant c.188T>G has a 99.9% probability of disease with Evo 2 score -24.85."
        self.assertFalse(NumericalGuardrail.verify_llm_output(hallucinated_response, self.evidence_card))

if __name__ == "__main__":
    unittest.main()