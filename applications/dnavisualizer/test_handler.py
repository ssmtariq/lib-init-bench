import pytest
from handler import validate_dna, calculate_gc_content, lambda_handler

def test_validate_dna():
    assert validate_dna("ATCG") == True
    assert validate_dna("INVALID") == False
    assert validate_dna("") == True

def test_calculate_gc_content():
    assert calculate_gc_content("ATCG") == 0.5
    assert calculate_gc_content("AAAA") == 0.0
    assert calculate_gc_content("CCGG") == 1.0

def test_lambda_handler():
    event = {"sequence": "ATCGATCG"}
    result = lambda_handler(event, None)
    assert result["sequence_length"] == 8
    assert result["gc_content"] == 0.5
    assert "import_time" in result

def test_lambda_handler_invalid_input():
    event = {"sequence": "INVALID"}
    result = lambda_handler(event, None)
    assert "error" in result
    assert "import_time" in result

def test_lambda_handler_empty_input():
    event = {}
    result = lambda_handler(event, None)
    assert "error" in result
    assert "import_time" in result