import os

class SmartVCFGenerator:
    # Expanded catalog of clinical genes, rsIDs, and genomic coordinates
    VARIANT_DATABASE = {
        "TP53_R175H": {"chrom": "17", "pos": 7577120, "id": "rs28934578", "ref": "G", "alt": "A", "gene": "TP53", "eff": "missense"},
        "BRCA1_185delAG": {"chrom": "17", "pos": 43094464, "id": "rs383970", "ref": "AG", "alt": "A", "gene": "BRCA1", "eff": "frameshift"},
        "BRCA2_N372H": {"chrom": "13", "pos": 32341788, "id": "rs144848", "ref": "A", "alt": "C", "gene": "BRCA2", "eff": "missense"},
        "CFTR_F508del": {"chrom": "7", "pos": 11718866, "id": "rs113993960", "ref": "CTT", "alt": "C", "gene": "CFTR", "eff": "in-frame_deletion"},
        "EGFR_L858R": {"chrom": "7", "pos": 55259515, "id": "rs121913491", "ref": "T", "alt": "G", "gene": "EGFR", "eff": "missense"},
        "PIK3CA_E545K": {"chrom": "3", "pos": 179218303, "id": "rs104894603", "ref": "G", "alt": "A", "gene": "PIK3CA", "eff": "missense"},
        "BRAF_V600E": {"chrom": "7", "pos": 140753336, "id": "rs113488022", "ref": "A", "alt": "T", "gene": "BRAF", "eff": "missense"},
        "KRAS_G12D": {"chrom": "12", "pos": 25245350, "id": "rs121913529", "ref": "C", "alt": "A", "gene": "KRAS", "eff": "missense"}
    }

    @classmethod
    def generate_vcf_from_selection(cls, variant_keys=None, output_filename="sample_patient.vcf"):
        """Automatically determines rsIDs and coordinates for selected variants and writes a VCF file."""
        if variant_keys is None:
            variant_keys = ["TP53_R175H", "BRCA1_185delAG", "CFTR_F508del", "BRAF_V600E", "KRAS_G12D"]

        vcf_content = [
            "##fileformat=VCFv4.2",
            "##source=OmniGen-NIM_SmartVCFGenerator",
            '##INFO=<ID=GENE,Number=1,Type=String,Description="Gene Symbol">',
            '##INFO=<ID=EFF,Number=1,Type=String,Description="Variant Effect">',
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tPATIENT_01"
        ]

        count = 0
        for key in variant_keys:
            if key in cls.VARIANT_DATABASE:
                v = cls.VARIANT_DATABASE[key]
                info_field = f"GENE={v['gene']};EFF={v['eff']}"
                line = f"{v['chrom']}\t{v['pos']}\t{v['id']}\t{v['ref']}\t{v['alt']}\t100\tPASS\t{info_field}\tGT:DP\t0/1:40"
                vcf_content.append(line)
                count += 1
                print(f"[+] Resolved {key} -> rsID: {v['id']} at Chr{v['chrom']}:{v['pos']}")

        os.makedirs(os.path.dirname(output_filename) if os.path.dirname(output_filename) else ".", exist_ok=True)
        with open(output_filename, "w") as f:
            f.write("\n".join(vcf_content) + "\n")
            
        print(f"[SUCCESS] Generated VCF file '{output_filename}' containing {count} variants.")

if __name__ == "__main__":
    # Run the generator to output the file for Phase 3 ingestion
    SmartVCFGenerator.generate_vcf_from_selection(
        variant_keys=["TP53_R175H", "BRCA1_185delAG", "CFTR_F508del", "BRAF_V600E", "KRAS_G12D", "PIK3CA_E545K"],
        output_filename="sample_patient.vcf"
    )