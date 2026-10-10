import asyncio
import aiohttp
from Bio import Entrez
import os
from dotenv import load_dotenv

load_dotenv()
# NCBI requires an email for Entrez queries
Entrez.email = os.getenv("NCBI_EMAIL", "your_email@example.com")

class AsyncGenomicFetcher:
    def __init__(self):
        self.ensembl_base = "https://rest.ensembl.org"

    async def fetch_ensembl_sequence(self, session, gene_symbol: str) -> dict:
        """Fetches genomic sequence and coordinates from Ensembl REST API."""
        url = f"{self.ensembl_base}/lookup/symbol/homo_sapiens/{gene_symbol}?expand=1"
        headers = {"Content-Type": "application/json"}
        
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "ensembl_id": data.get("id"),
                        "chromosome": data.get("seq_region_name"),
                        "start": data.get("start"),
                        "end": data.get("end"),
                        "strand": data.get("strand"),
                        "biotype": data.get("biotype")
                    }
                return {"error": f"Ensembl lookup failed with status {response.status}"}
        except Exception as e:
            return {"error": str(e)}

    async def fetch_clinvar_variants(self, session, gene_symbol: str) -> list:
        """Queries NCBI Entrez for ClinVar clinical variants associated with the gene."""
        search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term={gene_symbol}[gene_name]&retmode=json&retmax=5"
        
        try:
            async with session.get(search_url) as response:
                if response.status == 200:
                    data = await response.json()
                    id_list = data.get("esearchresult", {}).get("idlist", [])
                    return id_list
                return []
        except Exception as e:
            return []

    async def get_multi_omics_payload(self, gene_symbol: str) -> dict:
        """Concurrent master call pulling data across multiple databases simultaneously."""
        async with aiohttp.ClientSession() as session:
            # Execute queries concurrently
            ensembl_task = self.fetch_ensembl_sequence(session, gene_symbol)
            clinvar_task = self.fetch_clinvar_variants(session, gene_symbol)
            
            ensembl_res, clinvar_res = await asyncio.gather(ensembl_task, clinvar_task)
            
            return {
                "gene_symbol": gene_symbol.upper(),
                "genomics": ensembl_res,
                "clinvar_variant_ids": clinvar_res
            }

# --- Quick Test Execution ---
if __name__ == "__main__":
    fetcher = AsyncGenomicFetcher()
    results = asyncio.run(fetcher.get_multi_omics_payload("BRCA1"))
    print("\n[+] Asynchronous Fetch Successful:")
    print(results)