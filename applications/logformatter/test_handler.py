import pytest
from datetime import datetime
from handler import format_log_message, lambda_handler

def test_format_log_message():
    # Test basic formatting
    result = format_log_message("ERROR", "Test message")
    assert "ERROR" in result
    assert "Test message" in result
    assert str(datetime.now().year) in result

def test_format_log_message_with_service():
    result = format_log_message("INFO", "Test message", "test-service")
    assert "INFO" in result
    assert "Test message" in result
    assert "test-service" in result

def test_lambda_handler_basic():
    event = {
        "level": "ERROR",
        "message": "Test error",
        "service": "test-service"
    }
    result = lambda_handler(event, None)
    assert result["formatted_log"]
    assert "ERROR" in result["formatted_log"]
    assert "Test error" in result["formatted_log"]
    assert "test-service" in result["formatted_log"]
    assert "import_time" in result

def test_lambda_handler_minimal():
    event = {
        "message": "Test message"
    }
    result = lambda_handler(event, None)
    assert result["formatted_log"]
    assert "INFO" in result["formatted_log"]
    assert "Test message" in result["formatted_log"]
    assert "import_time" in result

def test_lambda_handler_no_message():
    event = {
        "level": "ERROR"
    }
    result = lambda_handler(event, None)
    assert "error" in result
    assert "import_time" in result