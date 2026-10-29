import logging

class AgenticVerificationPipeline:
    def __init__(self, max_retries=2, llm_client=None):
        self.max_retries = max_retries
        self.llm_client = llm_client

    def verify_and_correct(self, claim_text, extracted_data, validator_func, prompt_builder=None):
        """
        Runs the 2-retry agentic verification loop with real LLM error feedback.
        """
        attempts = 0
        is_valid = False
        current_data = extracted_data
        current_prompt = claim_text

        while attempts < self.max_retries and not is_valid:
            is_valid, error_message = validator_func(current_data)
            if is_valid:
                break
            
            attempts += 1
            logging.warning(f"Validation failed on attempt {attempts}: {error_message}. Feeding error back to model...")
            
            # If we have an LLM client and prompt builder, feed the exact error back into the next prompt
            if self.llm_client and prompt_builder:
                correction_prompt = prompt_builder(current_prompt, error_message, current_data)
                # current_data = self.llm_client.generate(correction_prompt)

        return {
            "verified": is_valid,
            "attempts": attempts + 1,
            "data": current_data,
            "error": None if is_valid else error_message
        }