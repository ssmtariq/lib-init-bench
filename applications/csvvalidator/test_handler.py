import pytest
from handler import parse_csv, validate_xml_schema, lambda_handler

def test_parse_csv():
    data = "name,age\nJohn,30\nJane,25"
    headers, rows = parse_csv(data)
    assert headers == ["name", "age"]
    assert rows == [["John", "30"], ["Jane", "25"]]

def test_parse_csv_empty():
    headers, rows = parse_csv("")
    assert headers == []
    assert rows == []

def test_validate_xml_schema():
    headers = ["name", "age"]
    rows = [["John", "30"], ["Jane", "25"]]
    assert validate_xml_schema(headers, rows) == True

def test_lambda_handler_basic():
    event = {
        "data": "name,age\nJohn,30\nJane,25",
        "validate_schema": False
    }
    result = lambda_handler(event, None)
    assert result["valid"] == True
    assert result["rows"] == 2
    assert result["columns"] == 2
    assert "import_time" in result

def test_lambda_handler_with_schema():
    event = {
        "data": "name,age\nJohn,30\nJane,25",
        "validate_schema": True
    }
    result = lambda_handler(event, None)
    assert result["valid"] == True
    assert result["schema_valid"] == True
    assert "import_time" in result

def test_lambda_handler_empty():
    event = {}
    result = lambda_handler(event, None)
    assert "error" in result
    assert "import_time" in result