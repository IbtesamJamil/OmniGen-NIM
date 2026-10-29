import requests

class LiveVariantAPI:
    @staticmethod
    def fetch_clinvar_data(hgvs_notation: str, gene_symbol: str):
        """
        Queries NCBI E-utilities / ClinVar API for live clinical significance.
        """
        try:
            term = f"{gene_symbol}%20AND%20{hgvs_notation}"
            url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term={term}&retmode=json"
            response = requests.get(url, timeout=3)
            data = response.json()
            id_list = data.get("esearchresult", {}).get("idlist", [])
            
            if not id_list:
                return {"source": "ClinVar", "status": "No direct match found in live ClinVar index", "clinical_significance": "Unknown / VUS"}
            
            # Fetch summary for the first matched ID
            clinvar_id = id_list[0]
            summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id={clinvar_id}&retmode=json"
            sum_resp = requests.get(summary_url, timeout=3)
            sum_data = sum_resp.json()
            
            item = sum_data.get("result", {}).get(clinvar_id, {})
            trait = item.get("trait_set", [{}])
            condition = trait[0].get("trait_name", "Unspecified condition") if trait else "Unspecified condition"
            sig = item.get("clinical_significance", {}).get("description", "Pathogenic / Uncertain")
            
            return {
                "source": "NCBI ClinVar Live API",
                "clinvar_id": clinvar_id,
                "condition": condition,
                "clinical_significance": sig,
                "status": "Live Data Retrieved Successfully"
            }
        except Exception as e:
            return {"source": "ClinVar API", "status": f"API offline or unreachable: {str(e)}", "clinical_significance": "Simulation Fallback Active"}