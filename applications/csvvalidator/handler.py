import time
start_time = time.perf_counter()

# Inefficient: Import heavy XML library even though it's rarely used
import xmlschema

# Calculate import time
import_time = time.perf_counter() - start_time

def parse_csv(data: str) -> tuple[list[str], list[list[str]]]:
    """Parse CSV data into headers and rows."""
    lines = data.strip().split('\n')
    if not lines:
        return [], []
    
    headers = lines[0].split(',')
    rows = [line.split(',') for line in lines[1:]]
    return headers, rows

def validate_xml_schema(headers: list[str], rows: list[list[str]]) -> bool:
    """
    Validate CSV data against XML schema.
    This is a rare operation that most invocations don't need,
    yet we imported xmlschema at module level.
    """
    # Convert CSV to XML format for validation
    xml_data = f'<csv><headers>{"".join(f"<col>{h}</col>" for h in headers)}</headers>'
    xml_data += f'<rows>{"".join("<row>" + "".join(f"<col>{c}</col>" for c in row) + "</row>" for row in rows)}</rows></csv>'
    
    # Simple schema requiring at least one header and row
    schema_str = '''<?xml version="1.0" encoding="UTF-8"?>
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
      <xs:element name="csv">
        <xs:complexType>
          <xs:sequence>
            <xs:element name="headers">
              <xs:complexType>
                <xs:sequence>
                  <xs:element name="col" type="xs:string" maxOccurs="unbounded"/>
                </xs:sequence>
              </xs:complexType>
            </xs:element>
            <xs:element name="rows">
              <xs:complexType>
                <xs:sequence>
                  <xs:element name="row" maxOccurs="unbounded">
                    <xs:complexType>
                      <xs:sequence>
                        <xs:element name="col" type="xs:string" maxOccurs="unbounded"/>
                      </xs:sequence>
                    </xs:complexType>
                  </xs:element>
                </xs:sequence>
              </xs:complexType>
            </xs:element>
          </xs:sequence>
        </xs:complexType>
      </xs:element>
    </xs:schema>'''
    
    schema = xmlschema.XMLSchema(schema_str)
    try:
        schema.validate(xml_data)
        return True
    except Exception:
        return False

def lambda_handler(event, context):
    """Process and optionally validate CSV data."""
    data = event.get('data', '')
    validate_schema = event.get('validate_schema', False)
    
    if not data:
        return {
            'error': 'No CSV data provided',
            'import_time': import_time
        }
    
    try:
        headers, rows = parse_csv(data)
        result = {
            'valid': True,
            'rows': len(rows),
            'columns': len(headers),
            'import_time': import_time
        }
        
        # XML schema validation is rarely needed
        if validate_schema:
            result['schema_valid'] = validate_xml_schema(headers, rows)
        
        return result
    
    except Exception as e:
        return {
            'error': str(e),
            'import_time': import_time
        }