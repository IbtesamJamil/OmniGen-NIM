import asyncio
import aiohttp

class VariantDatabaseFetcher:
    def __init__(self):
        # gnomAD GraphQL API endpoint v2/v3
        self.gnomad_graphql_url = "https://gnomad.broadinstitute.org/api"

    async def fetch_gnomad_gene_data(self, session, ensembl_id: str) -> dict:
        """
        Queries gnomAD via GraphQL to fetch allele frequency and constraint metrics.
        Determines if a gene is intolerant to loss-of-function mutations.
        """
        query = """
        query GnomadGene($gene_id: String!) {
          gene(gene_id: $gene_id, reference_genome: GRCh38) {
            symbol
            flags
            gnomad_constraint {
              oe_lof
              oe_lof_lower
              oe_lof_upper
              pLI
            }
          }
        }
        """
        payload = {
            "query": query,
            "variables": {"gene_id": ensembl_id}
        }
        headers = {"Content-Type": "application/json"}

        try:
            async with session.post(self.gnomad_graphql_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    gene_info = data.get("data", {}).get("gene", {})
                    constraint = gene_info.get("gnomad_constraint", {})
                    return {
                        "pLI_score": constraint.get("pLI", "N/A"), # Probability of Loss-of-function Intolerance
                        "oe_lof": constraint.get("oe_lof", "N/A"),  # Observed/Expected loss of function ratio
                        "flags": gene_info.get("flags", [])
                    }
                return {"error": f"gnomAD query failed with status {response.status}"}
        except Exception as e:
            return {"error": str(e)}

    async def fetch_clinvar_summary(self, session, variant_id: str) -> dict:
        """
        Fetches detailed clinical pathogenicity classification for a specific ClinVar ID.
        """
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id={variant_id}&retmode=json"
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    result = data.get("result", {}).get(variant_id, {})
                    germline = result.get("germline_classification", {})
                    return {
                        "variant_id": variant_id,
                        "title": result.get("title", "Unknown"),
                        "clinical_significance": germline.get("description", "Uncertain significance"),
                        "review_status": germline.get("review_status", "N/A")
                    }
                return {"error": "Failed to fetch ClinVar summary"}
        except Exception as e:
            return {"error": str(e)}

    async def get_variant_analysis(self, ensembl_id: str, sample_variant_id: str) -> dict:
        """Runs concurrent fetches across gnomAD and ClinVar."""
        async with aiohttp.ClientSession() as session:
            gnomad_task = self.fetch_gnomad_gene_data(session, ensembl_id)
            clinvar_task = self.fetch_clinvar_summary(session, sample_variant_id)
            
            gnomad_res, clinvar_res = await asyncio.gather(gnomad_task, clinvar_task)
            
            return {
                "gnomad_constraint": gnomad_res,
                "clinvar_detail": clinvar_res
            }

# --- Quick Test Execution ---
if __name__ == "__main__":
    fetcher = VariantDatabaseFetcher()
    # Testing using Ensembl ID from BRCA1 (ENSG00000012048) and ClinVar ID (4975019)
    results = asyncio.run(fetcher.get_variant_analysis("ENSG00000012048", "4975019"))
    print("\n[+] Variant & Population Database Fetch Successful:")
    print(results)