import re

class NumericalGuardrail:
    @staticmethod
    def verify_llm_output(response_text: str, ground_truth: dict) -> bool:
        """
        Validates LLM output with proper type casting so string/integer comparisons 
        don't cause false positives on correct residue coordinates.
        """
        target_residue = int(ground_truth.get("Residue", 175))
        
        # Extract residue numbers mentioned in the text
        suspicious_residue_mentions = re.findall(r'residue\s+(\d+)', response_text, re.IGNORECASE)
        for res in suspicious_residue_mentions:
            # If a residue is mentioned that differs from our target, flag it (ignoring small index numbers <= 5)
            if int(res) != target_residue and int(res) > 5:
                return False
                
        return True