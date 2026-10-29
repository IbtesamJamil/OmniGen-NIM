import re

class NumericalGuardrail:
    @staticmethod
    def verify_llm_output(response_text: str, ground_truth: dict) -> bool:
        """
        Validates LLM output by checking residue coordinates and variant positions 
        against ground-truth data to prevent hallucinations.
        """
        target_residue = int(ground_truth.get("Residue", 175))
        
        # Extract expected variant position from ground truth HGVS if available
        hgvs = ground_truth.get("HGVS", "")
        hgvs_match = re.search(r'c\.(\d+)', hgvs)
        expected_variant_pos = int(hgvs_match.group(1)) if hgvs_match else target_residue

        # 1. Check for explicitly mentioned residues that differ from target
        suspicious_residue_mentions = re.findall(r'residue\s+(\d+)', response_text, re.IGNORECASE)
        for res in suspicious_residue_mentions:
            if int(res) != target_residue and int(res) > 5 and int(res) != expected_variant_pos:
                return False
                
        # 2. Check for conflicting variant positions in the text
        variant_matches = re.findall(r'c\.(\d+)', response_text)
        for v_pos in variant_matches:
            if int(v_pos) != expected_variant_pos and int(v_pos) != target_residue:
                return False

        return True