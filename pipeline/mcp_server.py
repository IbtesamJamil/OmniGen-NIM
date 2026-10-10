import asyncio
from ncbi_ensembl import AsyncGenomicFetcher
from variant_db import VariantDatabaseFetcher

class OmniGenMCPTools:
    def __init__(self):
        self.genomic_fetcher = AsyncGenomicFetcher()
        self.variant_fetcher = VariantDatabaseFetcher()

    async def run_full_genomic_audit(self, gene_symbol: str, sample_variant_id: str = "4975019") -> dict:
        """
        Master MCP Tool: Aggregates NCBI, Ensembl, gnomAD, and ClinVar data 
        into a single unified payload for NVIDIA NIM inference.
        """
        # Step 1: Fetch genomic coordinates & variant list
        genomic_data = await self.genomic_fetcher.get_multi_omics_payload(gene_symbol)
        
        ensembl_id = genomic_data.get("genomics", {}).get("ensembl_id")
        if not ensembl_id or "error" in genomic_data.get("genomics", {}):
            return {"error": "Could not retrieve valid Ensembl ID for gene"}

        # Step 2: Fetch population & clinical metrics
        variant_data = await self.variant_fetcher.get_variant_analysis(ensembl_id, sample_variant_id)

        # Step 3: Combine into Master Data Contract
        return {
            "gene_symbol": gene_symbol.upper(),
            "ensembl_id": ensembl_id,
            "chromosome": genomic_data["genomics"].get("chromosome"),
            "genomic_location": {
                "start": genomic_data["genomics"].get("start"),
                "end": genomic_data["genomics"].get("end"),
                "strand": genomic_data["genomics"].get("strand")
            },
            "population_constraint": variant_data.get("gnomad_constraint"),
            "clinical_classification": variant_data.get("clinvar_detail")
        }

# --- MCP Tool Runner ---
if __name__ == "__main__":
    mcp_tools = OmniGenMCPTools()
    print("\n[*] Executing Unified MCP Master Tool Audit for BRCA1...")
    master_payload = asyncio.run(mcp_tools.run_full_genomic_audit("BRCA1", "4975019"))
    print("\n[+] Master MCP Payload Ready for NVIDIA NIM:")
    print(master_payload)