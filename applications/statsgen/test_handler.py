import pytest
from handler import calculate_statistics, lambda_handler

def test_calculate_statistics():
    numbers = [1, 2, 3, 4, 5]
    stats = calculate_statistics(numbers)
    assert stats["mean"] == 3
    assert stats["median"] == 3
    assert abs(stats["std_dev"] - 1.5811388300841898) < 0.0001

def test_calculate_statistics_single_number():
    numbers = [42]
    stats = calculate_statistics(numbers)
    assert stats["mean"] == 42
    assert stats["median"] == 42
    assert stats["std_dev"] == 0

def test_calculate_statistics_empty():
    with pytest.raises(ValueError):
        calculate_statistics([])

def test_lambda_handler():
    event = {"numbers": [1, 2, 3, 4, 5]}
    result = lambda_handler(event, None)
    assert "mean" in result
    assert "median" in result
    assert "std_dev" in result
    assert "import_time" in result
    assert "matplotlib_backend" in result
    assert "numpy_version" in result

def test_lambda_handler_no_numbers():
    event = {}
    result = lambda_handler(event, None)
    assert "error" in result
    assert "import_time" in result

def test_lambda_handler_invalid_input():
    event = {"numbers": []}
    result = lambda_handler(event, None)
    assert "error" in result
    assert "import_time" in result