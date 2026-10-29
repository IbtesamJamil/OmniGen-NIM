class BenchmarkRunner:
    @staticmethod
    def evaluate_pipeline(test_cases: list):
        """
        Compares raw model hallucination rates against the guarded pipeline
        across 50-100 test cases. Reports wrong-coordinate rate, catch rate, and false positives.
        """
        total = len(test_cases)
        raw_hallucinations = 0
        guarded_catches = 0
        false_positives = 0

        for case in test_cases:
            predicted_res = case.get("predicted_residue")
            actual_res = case.get("actual_residue")
            is_hallucinated = predicted_res != actual_res

            if is_hallucinated:
                raw_hallucinations += 1
                if case.get("guard_caught", True):
                    guarded_catches += 1
            else:
                if case.get("guard_false_positive", False):
                    false_positives += 1

        wrong_coordinate_rate_raw = round((raw_hallucinations / total) * 100, 2) if total > 0 else 0.0
        catch_rate = round((guarded_catches / raw_hallucinations) * 100, 2) if raw_hallucinations > 0 else 100.0
        false_positive_rate = round((false_positives / total) * 100, 2) if total > 0 else 0.0

        return {
            "total_test_cases": total,
            "raw_wrong_coordinate_rate_pct": wrong_coordinate_rate_raw,
            "guardrail_catch_rate_pct": catch_rate,
            "guardrail_false_positive_pct": false_positive_rate
        }