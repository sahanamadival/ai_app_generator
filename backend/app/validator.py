from app.models import AppSchema
from typing import List, Dict

class ValidationResult:
    def __init__(self, is_valid: bool, errors: List[str]):
        self.is_valid = is_valid
        self.errors = errors

def validate_cross_layer_consistency(schema: AppSchema) -> ValidationResult:
    errors = []
    
    # 1. Gather all API endpoint paths and DB table names
    db_tables = {table.name for table in schema.db_schema}
    api_paths = {endpoint.path for endpoint in schema.api_schema}
    roles = {rule.role for rule in schema.auth_rules}
    
    # 2. Validate API layer references DB tables that exist
    for endpoint in schema.api_schema:
        for table in endpoint.reads_from_tables:
            if table not in db_tables:
                errors.append(f"API Endpoint '{endpoint.path}' reads from non-existent table: '{table}'")
        for table in endpoint.writes_to_tables:
            if table not in db_tables:
                errors.append(f"API Endpoint '{endpoint.path}' writes to non-existent table: '{table}'")
        for role in endpoint.roles_allowed:
            if role not in roles:
                errors.append(f"API Endpoint '{endpoint.path}' allows unknown role: '{role}'")
                
    # 3. Validate UI layer references API endpoints that exist
    for page in schema.ui_schema:
        for role in page.restricted_to_roles:
            if role not in roles:
                errors.append(f"UI Page '{page.path}' restricted to unknown role: '{role}'")
                
        for comp in page.components:
            if comp.data_source and comp.data_source not in api_paths:
                errors.append(f"UI Component '{comp.name}' uses non-existent data_source API: '{comp.data_source}'")
            for action in comp.actions:
                # Handle cases where action might be 'POST /api/users' or just '/api/users'
                action_path = action.split(' ')[-1] if ' ' in action else action
                if action_path not in api_paths:
                     errors.append(f"UI Component '{comp.name}' triggers non-existent action API: '{action_path}' (Full action string: {action})")
                     
    return ValidationResult(is_valid=len(errors) == 0, errors=errors)
