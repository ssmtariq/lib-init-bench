import pytest
from handler import validate_person, lambda_handler

def test_validate_person_valid():
    data = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    }
    is_valid, normalized_data, error = validate_person(data)
    assert is_valid is True
    assert normalized_data["name"] == "John Doe"
    assert normalized_data["age"] == 30
    assert normalized_data["email"] == "john@example.com"
    assert error is None

def test_validate_person_invalid_email():
    data = {
        "name": "John Doe",
        "age": 30,
        "email": "not-an-email"
    }
    is_valid, normalized_data, error = validate_person(data)
    assert is_valid is False
    assert "email" in str(error).lower()

def test_validate_person_invalid_age():
    data = {
        "name": "John Doe",
        "age": -1,
        "email": "john@example.com"
    }
    is_valid, normalized_data, error = validate_person(data)
    assert is_valid is False
    assert "age" in str(error).lower()

def test_lambda_handler_valid():
    event = {
        "data": {
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com"
        }
    }
    result = lambda_handler(event, None)
    assert result["valid"] is True
    assert "normalized_data" in result
    assert "import_time" in result
    assert "pydantic_version" in result

def test_lambda_handler_invalid():
    event = {
        "data": {
            "name": "John Doe",
            "age": -1,
            "email": "not-an-email"
        }
    }
    result = lambda_handler(event, None)
    assert result["valid"] is False
    assert "validation_error" in result
    assert "import_time" in result

def test_lambda_handler_no_data():
    event = {}
    result = lambda_handler(event, None)
    assert "error" in result
    assert "import_time" in result