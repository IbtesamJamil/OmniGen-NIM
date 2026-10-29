import os
import pytest
from pipeline.audit_ledger import AuditLedger
from pipeline.vcf_parser import VCFParser

def test_audit_ledger_chain_verification():
    """Test that the SQLite audit ledger initializes and verifies its hash chain correctly."""
    AuditLedger.initialize_db()
    AuditLedger.log_action("ibtesam", "Clinical Geneticist", "UNIT_TEST_ACTION", "Testing ledger integrity.")
    
    is_valid = AuditLedger.verify_full_ledger()
    assert is_valid is True, "Audit ledger cryptographic verification failed unexpectedly."

    head_hash = AuditLedger.get_head_hash()
    assert head_hash is not None
    assert isinstance(head_hash, str)
    assert len(head_hash) == 64  # SHA-256 hex length

def test_vcf_parser_structure():
    """Test VCF parser handles mock file uploads correctly."""
    class MockUploadedFile:
        def __init__(self, content):
            self.content = content
        def read(self):
            return self.content.encode('utf-8')
        def getvalue(self):
            return self.content.encode('utf-8')

    mock_vcf_data = (
        "##fileformat=VCFv4.2\n"
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n"
        "17\t7577538\trs123\tC\tT\t100\tPASS\tGENE=TP53\tGT\t0/1\n"
    )
    
    uploaded_file = MockUploadedFile(mock_vcf_data)
    variants = VCFParser.parse_vcf_upload(uploaded_file)
    
    assert len(variants) == 1
    assert variants[0]["chrom"] == "17"
    assert variants[0]["pos"] == "7577538"
    assert variants[0]["ref"] == "C"
    assert variants[0]["alt"] == "T"