import pytest
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.motif_search import MotifSearchEngine

def test_motif_search_exact_match():
    """Test searching for an exact term present in the motif database."""
    results = MotifSearchEngine.search_motifs("DNA binding")
    assert len(results) > 0
    assert any("p53" in motif["name"] for motif in results)

def test_motif_search_signature_match():
    """Test searching by chemical/amino acid signature."""
    results = MotifSearchEngine.search_motifs("SHLVEALYLVCG")
    assert len(results) > 0
    assert results[0]["uniprot"] == "P01308"

def test_motif_search_fallback():
    """Test fallback behavior when a completely unknown query is provided."""
    results = MotifSearchEngine.search_motifs("xyz_nonexistent_motif_999")
    # Based on our logic, it should return the default fallback items (first 2 items)
    assert len(results) == 2