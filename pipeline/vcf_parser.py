import io

class VCFParser:
    @staticmethod
    def parse_vcf_upload(uploaded_file):
        """
        Parses an uploaded VCF file stream into a structured list of variant dictionaries.
        """
        variants = []
        try:
            stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
            for line in stringio:
                if line.startswith("#"):
                    continue  # Skip header/metadata lines
                
                parts = line.strip().split("\t")
                if len(parts) >= 8:
                    chrom, pos, rs_id, ref, alt, qual, filter_val, info = parts[:8]
                    variants.append({
                        "chrom": chrom,
                        "pos": pos,
                        "id": rs_id if rs_id != "." else "rs_unknown",
                        "ref": ref,
                        "alt": alt,
                        "qual": qual if qual != "." else "100.0",
                        "info": info
                    })
        except Exception as e:
            print(f"Error parsing VCF stream: {e}")
            
        return variants