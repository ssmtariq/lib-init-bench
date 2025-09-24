import pytest
from handler import hash_text, lambda_handler

def test_hash_text():
    text = "Hello, World!"
    result = hash_text(text, "sha256")
    assert result == "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"

def test_hash_text_different_algorithms():
    text = "test"
    sha256_hash = hash_text(text, "sha256")
    sha512_hash = hash_text(text, "sha512")
    assert sha256_hash != sha512_hash
    assert len(sha512_hash) > len(sha256_hash)

def test_hash_text_invalid_algorithm():
    with pytest.raises(ValueError):
        hash_text("test", "invalid_algorithm")

def test_lambda_handler():
    event = {
        "text": "Hello, World!",
        "algorithm": "sha256"
    }
    result = lambda_handler(event, None)
    assert "text_hash" in result
    assert result["algorithm"] == "sha256"
    assert "import_time" in result
    assert "text_length" in result

def test_lambda_handler_no_text():
    event = {}
    result = lambda_handler(event, None)
    assert "error" in result
    assert "import_time" in result

def test_lambda_handler_invalid_algorithm():
    event = {
        "text": "test",
        "algorithm": "invalid"
    }
    result = lambda_handler(event, None)
    assert "error" in result
    assert "import_time" in result