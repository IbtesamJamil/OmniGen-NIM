import os
import numpy as np
from Bio.PDB import PDBParser

class StructuralNeighborhoodAnalyzer:
    """
    Analyzes 3D structural neighborhoods using C-alpha Euclidean distance cutoffs (8 Å)
    as a structural burial proxy, and extracts AlphaFold pLDDT confidence scores.
    """
    def __init__(self, pdb_dir: str = "data/alphafold_cache"):
        self.pdb_dir = pdb_dir
        self.parser = PDBParser(QUIET=True)

    def analyze_neighborhood(self, pdb_filename: str, residue_number: int, threshold_angstroms: float = 8.0):
        pdb_path = os.path.join(self.pdb_dir, pdb_filename)
        if not os.path.exists(pdb_path):
            return {"error": f"PDB structure file not found at {pdb_path}"}

        structure = self.parser.get_structure("protein", pdb_path)
        target_coords = None
        target_resname = "UNKNOWN"
        plddt_score = 0.0

        # Locate target residue C-alpha coordinates and B-factor (pLDDT is stored in B-factor column in AlphaFold PDBs)
        for model in structure:
            for chain in model:
                for residue in chain:
                    if residue.get_id()[1] == residue_number and "CA" in residue:
                        target_coords = residue["CA"].get_coord()
                        target_resname = residue.get_resname()
                        plddt_score = float(residue["CA"].get_bfactor())
                        break
                if target_coords is not None:
                    break
            if target_coords is not None:
                break

        if target_coords is None:
            return {"error": f"Residue {residue_number} C-alpha atom not found in PDB structure."}

        neighbors = []
        for model in structure:
            for chain in model:
                for residue in chain:
                    if residue.get_id()[0] != " ":
                        continue
                    res_id = residue.get_id()[1]
                    if res_id == residue_number:
                        continue
                    if "CA" in residue:
                        other_coords = residue["CA"].get_coord()
                        distance = np.linalg.norm(target_coords - other_coords)
                        if distance <= threshold_angstroms:
                            neighbors.append({
                                "residue": residue.get_resname(),
                                "position": res_id,
                                "chain": chain.id,
                                "distance_angstroms": round(float(distance), 2)
                            })

        # Burial proxy classification based on 8Å coordination number
        neighborhood_count = len(neighbors)
        exposure_status = "Buried Core (Proxy > 12 contacts)" if neighborhood_count > 12 else "Exposed Surface/Loop (Proxy <= 12 contacts)"

        # pLDDT confidence reliability warning
        confidence_warning = None
        if plddt_score < 70.0:
            confidence_warning = "Low pLDDT confidence (<70); structural neighborhood metrics carry higher uncertainty."

        return {
            "target_residue": residue_number,
            "target_residue_name": target_resname,
            "threshold_angstroms": threshold_angstroms,
            "neighborhood_count": neighborhood_count,
            "exposure_classification": exposure_status,
            "plddt_score": round(plddt_score, 2),
            "confidence_warning": confidence_warning,
            "neighbors": sorted(neighbors, key=lambda x: x["distance_angstroms"])
        }