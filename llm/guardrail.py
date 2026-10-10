import re

class NumericalGuardrail:
    @staticmethod
    def extract_numbers_and_ids(text: str) -> set:
        """
        Extracts numbers (normalizing scientific notation and floats) 
        and HGVS/rsID identifiers.
        """
        tokens = set()
        
        # Regex matching floats, integers, and scientific notation (e.g. 3.2e-05, -24.85)
        number_pattern = r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?"
        raw_numbers = re.findall(number_pattern, text)
        
        for num in raw_numbers:
            if not num or num in ["-", "+"]:
                continue
            try:
                # Round normalized floats to avoid precision mismatch
                val = float(num)
                tokens.add(round(val, 6))
            except ValueError:
                tokens.add(num)

        # Match HGVS notation & rsIDs
        ids = set(re.findall(r"rs\d+|c\.[A-Za-z0-9>]+|p\.[A-Za-z0-9]+", text))
        tokens.update(ids)
        
        return tokens

    @classmethod
    def verify_llm_output(cls, llm_response: str, input_json_payload: dict) -> bool:
        """
        Verifies that every number/ID in the response exists in the computed JSON payload.
        """
        allowed_tokens = cls.extract_numbers_and_ids(str(input_json_payload))
        response_tokens = cls.extract_numbers_and_ids(llm_response)
        
        hallucinated_tokens = response_tokens - allowed_tokens
        if hallucinated_tokens:
            print(f"[!] Guardrail Triggered! Hallucinated tokens detected: {hallucinated_tokens}")
            return False
        return True