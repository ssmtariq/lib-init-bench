import pytest
from handler import basic_analysis, advanced_analysis, lambda_handler

def test_basic_analysis():
    text = "This is a test sentence. And another one."
    result = basic_analysis(text)
    assert result["word_count"] == 8
    assert result["sentence_count"] == 2
    assert "avg_word_length" in result

def test_advanced_analysis():
    text = "John Smith works at Google in New York."
    result = advanced_analysis(text)
    assert result["word_count"] == 8
    assert result["sentence_count"] == 1
    assert "pos_tags" in result
    assert "named_entities" in result
    assert "embedding_dim" in result

def test_lambda_handler_basic():
    event = {
        "text": "This is a test.",
        "analysis_type": "basic"
    }
    result = lambda_handler(event, None)
    assert result["word_count"] == 4
    assert result["sentence_count"] == 1
    assert "import_time" in result
    assert "nltk_data_path" in result
    assert "transformer_model" in result

def test_lambda_handler_advanced():
    event = {
        "text": "This is a test.",
        "analysis_type": "advanced"
    }
    result = lambda_handler(event, None)
    assert "pos_tags" in result
    assert "named_entities" in result
    assert "import_time" in result

def test_lambda_handler_no_text():
    event = {}
    result = lambda_handler(event, None)
    assert "error" in result
    assert "import_time" in result

def test_lambda_handler_empty_text():
    event = {"text": ""}
    result = lambda_handler(event, None)
    assert "error" in result
    assert "import_time" in result