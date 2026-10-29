import os
import requests
from typing import Optional

class AlphaFoldFetcher:
    """Fetches 3D structure data and pLDDT confidence scores from AlphaFold DB."""

    def __init__(self, cache_dir: str = "data/alphafold_cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def fetch_pdb(self, uniprot_id: str) -> Optional[str]:
        """Downloads PDB file for a given UniProt ID with dynamic version fallback."""
        uniprot_id = uniprot_id.upper()
        cache_path = os.path.join(self.cache_dir, f"{uniprot_id}.pdb")

        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                return f.read()

        # Try API lookup first to get exact model URL
        api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
        try:
            res = requests.get(api_url, timeout=10)
            if res.status_code == 200 and len(res.json()) > 0:
                pdb_url = res.json()[0].get("pdbUrl")
                if pdb_url:
                    pdb_res = requests.get(pdb_url, timeout=15)
                    if pdb_res.status_code == 200:
                        with open(cache_path, "w") as f:
                            f.write(pdb_res.text)
                        return pdb_res.text
        except Exception:
            pass

        # Fallback to direct download URLs (v4 & v5)
        for version in ["v4", "v5", "v3"]:
            url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_{version}.pdb"
            try:
                res = requests.get(url, timeout=10)
                if res.status_code == 200:
                    with open(cache_path, "w") as f:
                        f.write(res.text)
                    return res.text
            except Exception:
                continue

        return None

    def extract_plddt(self, pdb_content: str, residue_number: int) -> Optional[float]:
        """Extracts pLDDT score (B-factor column) for a target residue position."""
        for line in pdb_content.splitlines():
            if line.startswith("ATOM") or line.startswith("HETATM"):
                try:
                    res_num = int(line[22:26].strip())
                    if res_num == residue_number:
                        return float(line[60:66].strip())
                except ValueError:
                    continue
        return None

    def fetch_pae_json(self, uniprot_id: str):
        """Fetches the Predicted Aligned Error (PAE) JSON data from AlphaFold DB."""
        uniprot_id = uniprot_id.upper()
        try:
            summary_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
            res = requests.get(summary_url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if data and len(data) > 0:
                    pae_json_url = data[0].get("paeDocUrl")
                    if pae_json_url:
                        json_res = requests.get(pae_json_url, timeout=15)
                        if json_res.status_code == 200:
                            return json_res.json()
        except Exception as e:
            print(f"Error fetching PAE matrix: {e}")
        return None


if __name__ == "__main__":
    fetcher = AlphaFoldFetcher()
    print("Fetching AlphaFold model for P04637...")
    pdb_data = fetcher.fetch_pdb("P04637")
    if pdb_data:
        plddt = fetcher.extract_plddt(pdb_data, residue_number=175)
        print(f"[SUCCESS] Downloaded PDB. pLDDT at residue 175: {plddt}")
    else:
        print("[FAILED] Could not fetch PDB model.")