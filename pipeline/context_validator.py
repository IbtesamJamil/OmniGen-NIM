class ContextValidator:
    @staticmethod
    def harmonize_prompt_context(user_prompt: str, active_gene: str, active_hgvs: str) -> str:
        """
        Inspects if the user's prompt references a different gene/variant than the active sidebar context,
        and injects an intelligent correction note so the model uses context awareness rather than panicking.
        """
        prompt_upper = user_prompt.upper()
        active_upper = active_gene.upper()
        
        # Check if user mentioned a gene other than the active one
        common_genes = ["PTEN", "BRAF", "TP53", "EGFR", "KRAS", "HER2"]
        mentioned_genes = [g for g in common_genes if g in prompt_upper]
        
        correction_note = ""
        if mentioned_genes and active_upper not in mentioned_genes:
            target_mentioned = mentioned_genes[0]
            correction_note = (
                f"\n[INTELLIGENCE OVERRIDE NOTE: The user's query mentions '{target_mentioned}', "
                f"but the enterprise dashboard sidebar is actively locked onto '{active_upper}' ({active_hgvs}). "
                f"Acknowledge the user's mention of {target_mentioned}, but intelligently anchor your structural "
                f"and thermodynamic analysis on the active dashboard context ({active_upper}), explaining how "
                f"the active metrics apply.]\n"
            )
        
        return user_prompt + correction_note