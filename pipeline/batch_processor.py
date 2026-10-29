import os
import shutil
import zipfile
from pipeline.alphafold_context import AlphaFoldFetcher
from pipeline.stability_estimator import StabilityEstimator
from pipeline.pdf_exporter import ClinicalPDFExporter

class BatchInterpretationPipeline:
    @staticmethod
    def process_batch(variants_list, gene_symbol):
        """
        Processes a list of variant dictionaries and generates a zip file entirely on Drive D.
        """
        fetcher = AlphaFoldFetcher()
        
        # Create a local temporary directory strictly on Drive D:
        temp_dir = os.path.abspath(r"D:\OmniGen-NIM\batch_temp")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        os.makedirs(temp_dir, exist_ok=True)
        
        pdf_files = []

        for idx, var in enumerate(variants_list):
            hgvs = var.get("hgvs", "c.1A>G")
            residue = int(var.get("residue", 1))
            uniprot = var.get("uniprot", "P04637")

            pdb_content = fetcher.fetch_pdb(uniprot)
            plddt = fetcher.extract_plddt(pdb_content, residue) if pdb_content else 75.0
            stability = StabilityEstimator.calculate_deltadelta_g(hgvs, plddt)

            payload = {
                "Gene": gene_symbol,
                "UniProt": uniprot,
                "HGVS": hgvs,
                "Residue": residue,
                "pLDDT": plddt,
                "DeltaDeltaG_kcal_mol": stability["delta_delta_g"],
                "Stability_Status": stability["classification"],
                "Persona": "Automated Enterprise Batch Processor",
                "CeleryAsyncLayer": "Active (SQLite)"
            }

            filename = f"OmniGen_{gene_symbol}_{hgvs.replace('>', '_')}_Report.pdf"
            dest_path = os.path.join(temp_dir, filename)

            # Generate PDF directly inside the local Drive D folder
            ClinicalPDFExporter.generate_report(payload=payload, vcf_results=None, custom_output_path=dest_path)
            if os.path.exists(dest_path):
                pdf_files.append(dest_path)

        zip_path = os.path.join(temp_dir, f"OmniGen_{gene_symbol}_Batch_Reports.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in pdf_files:
                zipf.write(file, os.path.basename(file))

        return zip_path