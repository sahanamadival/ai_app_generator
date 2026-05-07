from app.models import AppSchema
import random

class RuntimeSimulator:
    def __init__(self, schema: AppSchema):
        self.schema = schema

    def simulate(self) -> list:
        """
        Simulates a random but logical user action tracing from UI to API to DB.
        """
        trace = []
        
        if not self.schema.ui_schema:
            return [{"step": "Error", "message": "No UI Schema found to start simulation.", "status": "failed"}]

        # Pick a random UI page 
        page = random.choice(self.schema.ui_schema)
        trace.append({
            "step": "User Navigation",
            "message": f"User navigates to {page.path} ({page.name})",
            "status": "success"
        })

        if page.restricted_to_roles:
            role = page.restricted_to_roles[0]
            trace.append({
                "step": "UI Auth Check",
                "message": f"Checking if user has role: '{role}'. Access Granted.",
                "status": "success"
            })

        if not page.components:
             trace.append({"step": "UI Render", "message": "Page has no components. Simulation ended.", "status": "warning"})
             return trace

        component = random.choice(page.components)
        trace.append({
            "step": "Component Mount",
            "message": f"Rendering UI Component '{component.name}' ({component.type})",
            "status": "success"
        })

        # Try to find an API endpoint it interacts with
        target_api_path = None
        if component.data_source:
            target_api_path = component.data_source
            trace.append({"step": "Network Request", "message": f"Component automatically fetching data from {target_api_path}", "status": "info"})
        elif component.actions:
            target_api_path = component.actions[0].split(' ')[-1] if ' ' in component.actions[0] else component.actions[0]
            trace.append({"step": "User Interaction", "message": f"User clicks button, triggering API {target_api_path}", "status": "info"})
        else:
             trace.append({"step": "Static UI", "message": "Component has no data bindings. Simulation ended.", "status": "success"})
             return trace

        # Match API endpoint
        endpoint = next((e for e in self.schema.api_schema if e.path == target_api_path), None)
        if not endpoint:
            trace.append({"step": "API Gateway", "message": f"404 Not Found. API '{target_api_path}' does not exist!", "status": "failed"})
            return trace

        trace.append({
            "step": "API Gateway Route Match",
            "message": f"Successfully routed to backend controller for {endpoint.method} {endpoint.path}",
            "status": "success"
        })

        if endpoint.roles_allowed:
            trace.append({
                "step": "API Security Middleware",
                "message": f"Validating JWT token for required roles: {endpoint.roles_allowed}. Token valid.",
                "status": "success"
            })

        if endpoint.reads_from_tables:
            tables = ", ".join(endpoint.reads_from_tables)
            trace.append({
                "step": "Database Query",
                "message": f"Executing SELECT query on DB tables: [{tables}]",
                "status": "success"
            })
            
        if endpoint.writes_to_tables:
            tables = ", ".join(endpoint.writes_to_tables)
            trace.append({
                "step": "Database Mutation",
                "message": f"Executing INSERT/UPDATE transaction on DB tables: [{tables}]",
                "status": "success"
            })

        trace.append({
            "step": "API Response",
            "message": f"200 OK. Returning structured JSON data back to client.",
            "status": "success"
        })

        trace.append({
            "step": "UI Update",
            "message": f"Component '{component.name}' updates state with new data.",
            "status": "success"
        })

        return trace
