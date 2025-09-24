import time
start_time = time.perf_counter()

# Inefficient: Importing rich just for basic log formatting
from rich.console import Console
from rich.theme import Theme
from rich.text import Text
from datetime import datetime

# Calculate import time
import_time = time.perf_counter() - start_time

# Create console with custom theme - this could be done with simple string formatting
console = Console(theme=Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red bold",
    "debug": "grey50"
}))

def format_log_message(level: str, message: str, service: str = None) -> str:
    """
    Format a log message with timestamp, level, and optional service name.
    This could be done with a simple f-string instead of rich.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create styled text - unnecessary complexity for simple log formatting
    text = Text()
    text.append(f"[{timestamp}] ", style="grey70")
    text.append(level.upper(), style=level.lower())
    if service:
        text.append(f" [{service}]", style="grey70")
    text.append(f": {message}")
    
    return str(text)

def lambda_handler(event, context):
    """Format a log message with rich styling."""
    level = event.get('level', 'INFO')
    message = event.get('message', '')
    service = event.get('service')
    
    if not message:
        return {
            'error': 'No message provided',
            'import_time': import_time
        }
    
    # All of this could be achieved with:
    # formatted = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {level} [{service}]: {message}"
    
    try:
        formatted_log = format_log_message(level, message, service)
        result = {
            'formatted_log': formatted_log,
            'raw_message': message,
            'level': level,
            'import_time': import_time
        }
        if service:
            result['service'] = service
        return result
        
    except Exception as e:
        return {
            'error': str(e),
            'import_time': import_time
        }