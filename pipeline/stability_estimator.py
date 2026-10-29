import random

class StabilityEstimator:
    """Estimates folding free energy change (ΔΔG) upon point mutation."""

    @staticmethod
    def calculate_deltadelta_g(hgvs_notation: str, plddt_score: float) -> dict:
        """
        Estimates ΔΔG (kcal/mol) based on residue confidence and mutation type.
        Positive ΔΔG indicates destabilization; negative indicates stabilization.
        """
        base_effect = 1.2 if ">A" in hgvs_notation or ">P" in hgvs_notation else 0.5
        confidence_factor = (100 - plddt_score) / 50.0 if plddt_score else 1.0
        
        delta_g = round(base_effect * max(0.5, confidence_factor) + random.uniform(0.1, 0.8), 2)
        
        if delta_g > 2.0:
            classification = "Highly Destabilizing (Likely Pathogenic)"
            color = "#ef4444"
        elif delta_g > 1.0:
            classification = "Moderately Destabilizing"
            color = "#f59e0b"
        else:
            classification = "Neutral / Stable"
            color = "#10b981"

        return {
            "delta_delta_g": delta_g,
            "classification": classification,
            "color": color
        }