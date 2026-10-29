class UniProtMotifIndex:
    # Real structural motif index across core functional proteins
    UNIPROT_MOTIF_INDEX = {
        "P04637": {
            "gene": "TP53",
            "protein": "Cellular tumor antigen p53",
            "motifs": [
                {"name": "Transactivation domain 1", "start": 1, "end": 42},
                {"name": "DNA-binding domain", "start": 102, "end": 292},
                {"name": "Tetramerization domain", "start": 326, "end": 356}
            ]
        },
        "P15056": {
            "gene": "BRAF",
            "protein": "Serine/threonine-protein kinase B-raf",
            "motifs": [
                {"name": "RBD (Ras-binding domain)", "start": 150, "end": 227},
                {"name": "Protein kinase domain", "start": 457, "end": 717}
            ]
        },
        "P00533": {
            "gene": "EGFR",
            "protein": "Epidermal growth factor receptor",
            "motifs": [
                {"name": "Extracellular ligand-binding", "start": 25, "end": 645},
                {"name": "Protein kinase domain", "start": 712, "end": 979}
            ]
        },
        "P01116": {
            "gene": "KRAS",
            "protein": "GTPase KRas",
            "motifs": [
                {"name": "G-domain", "start": 1, "end": 166},
                {"name": "Switch I", "start": 32, "end": 40},
                {"name": "Switch II", "start": 60, "end": 76}
            ]
        }
    }

    @classmethod
    def lookup_motif(cls, gene_or_accession: str, residue: int):
        """
        Looks up functional UniProt motifs for a given gene/accession and residue coordinate.
        """
        for acc, data in cls.UNIPROT_MOTIF_INDEX.items():
            if data["gene"].upper() == gene_or_accession.upper() or acc.upper() == gene_or_accession.upper():
                for motif in data["motifs"]:
                    if motif["start"] <= residue <= motif["end"]:
                        return {
                            "accession": acc,
                            "protein": data["protein"],
                            "matched_motif": motif["name"],
                            "range": f"{motif['start']}-{motif['end']}"
                        }
        return None