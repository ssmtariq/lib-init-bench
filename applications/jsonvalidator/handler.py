import time
start_time = time.perf_counter()

# Inefficient: Import heavy validation framework for simple validation
from pydantic import BaseModel, EmailStr, Field, ValidationError

# Calculate import time
import_time = time.perf_counter() - start_time

class Person(BaseModel):
    """
    Define a Pydantic model for validation.
    This triggers heavy type system initialization,
    even though we're just validating simple types.
    """
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    email: EmailStr

def validate_person(data: dict) -> tuple[bool, dict, str]:
    """
    Validate person data using Pydantic.
    We could do this with simple dict access and isinstance checks.
    """
    try:
        person = Person(**data)
        return True, person.model_dump(), None
    except ValidationError as e:
        return False, data, str(e)

def lambda_handler(event, context):
    """Validate JSON data against our schema."""
    data = event.get('data', {})
    
    if not data:
        return {
            'error': 'No data provided',
            'import_time': import_time
        }
    
    try:
        is_valid, normalized_data, error = validate_person(data)
        
        result = {
            'valid': is_valid,
            'normalized_data': normalized_data,
            'import_time': import_time
        }
        
        if error:
            result['validation_error'] = error
            
        # Add metadata about the validation framework
        result['pydantic_version'] = Person.model_config['title']
        
        return result
        
    except Exception as e:
        return {
            'error': str(e),
            'import_time': import_time
        }