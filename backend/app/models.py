from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

# --- INTERMEDIATE INTENT ---
class IntermediateIntent(BaseModel):
    features: List[str] = Field(description="List of core features extracted from the prompt")
    roles: List[str] = Field(description="User roles identified (e.g., admin, user)")
    core_entities: List[str] = Field(description="Core data entities (e.g., User, Invoice, Contact)")
    assumptions_made: List[str] = Field(default_factory=list, description="If the prompt is vague or underspecified, list the reasonable assumptions made to build the system.")

# --- SYSTEM ARCHITECTURE ---
class SystemArchitecture(BaseModel):
    services: List[str] = Field(description="High level services (e.g., auth_service, crm_service)")
    db_tables: List[str] = Field(description="Names of database tables needed")
    api_endpoints: List[str] = Field(description="List of API endpoints (e.g., /api/users)")

# --- FINAL SCHEMA ---
class DBField(BaseModel):
    name: str = Field(description="Field name")
    type: str = Field(description="Data type (string, integer, boolean, datetime, etc.)")
    required: bool = Field(default=True)
    relation: Optional[str] = Field(None, description="If this is a foreign key, the target table name")

class DBTable(BaseModel):
    name: str
    fields: List[DBField]

class APIEndpoint(BaseModel):
    path: str = Field(description="Endpoint path, e.g., /api/users")
    method: str = Field(description="HTTP method (GET, POST, PUT, DELETE)")
    request_body: Optional[Dict[str, str]] = Field(None, description="Expected request body schema mapping field name to type")
    response_body: Optional[Dict[str, str]] = Field(None, description="Expected response body schema")
    roles_allowed: List[str] = Field(description="Roles allowed to access this endpoint")
    reads_from_tables: List[str] = Field(description="DB tables this endpoint reads from")
    writes_to_tables: List[str] = Field(description="DB tables this endpoint writes to")

class UIComponent(BaseModel):
    name: str
    type: str = Field(description="Type of component (form, table, dashboard, list, etc.)")
    data_source: Optional[str] = Field(None, description="API endpoint path this component fetches data from")
    actions: List[str] = Field(default_factory=list, description="API endpoint paths this component can trigger (e.g., POST /api/login)")

class UIPage(BaseModel):
    path: str = Field(description="URL route for the page")
    name: str
    components: List[UIComponent]
    restricted_to_roles: List[str] = Field(description="Roles allowed to view this page")

class AuthRule(BaseModel):
    role: str
    permissions: List[str] = Field(description="List of permissions, e.g., read:users, write:contacts")

class AppSchema(BaseModel):
    db_schema: List[DBTable]
    api_schema: List[APIEndpoint]
    ui_schema: List[UIPage]
    auth_rules: List[AuthRule]
    business_logic: List[str] = Field(description="List of core business rules (e.g., 'Premium users can access X')")
