import json
from app.models import IntermediateIntent, SystemArchitecture, AppSchema
from app.llm import llm_provider
from app.validator import validate_cross_layer_consistency

class Compiler:
    def __init__(self):
        self.llm = llm_provider

    def compile(self, prompt: str) -> dict:
        """
        Main entrypoint. Compiles a natural language prompt into a validated AppSchema.
        """
        stages = []
        total_tokens = 0
        try:
            # Stage 1: Intent Extraction
            print("Running Stage 1: Intent Extraction...")
            intent_prompt = f"""Extract the core intent from the following application description.
            Description: {prompt}
            Identify the core features, user roles, and main data entities.
            FAILURE HANDLING: If the prompt is vague, conflicting, or underspecified, you MUST make reasonable technical assumptions to resolve conflicts and design a complete system. Document your choices clearly in the 'assumptions_made' array."""
            intent, tokens = self.llm.generate_structured(intent_prompt, IntermediateIntent)
            total_tokens += tokens
            stages.append({"stage": "intent", "data": json.loads(intent.model_dump_json())})

            # Stage 2: System Architecture
            print("Running Stage 2: System Architecture Design...")
            arch_prompt = f"""Based on the following intent, design the high-level system architecture.
            Intent: {intent.model_dump_json()}
            Define the high-level services, database tables needed, and the API endpoints that will power the features."""
            architecture, tokens = self.llm.generate_structured(arch_prompt, SystemArchitecture)
            total_tokens += tokens
            stages.append({"stage": "architecture", "data": json.loads(architecture.model_dump_json())})

            # Stage 3: Schema Generation
            print("Running Stage 3: Schema Generation...")
            schema_prompt = f"""Based on the following architecture, generate the full application schema.
            Architecture: {architecture.model_dump_json()}
            You must define the strict UI pages and components, API endpoints with their inputs/outputs, Database tables with columns and types, and Auth rules.
            Ensure cross-layer consistency (e.g. UI calls valid APIs, APIs read from valid DB tables)."""
            app_schema, tokens = self.llm.generate_structured(schema_prompt, AppSchema)
            total_tokens += tokens
            stages.append({"stage": "initial_schema", "data": json.loads(app_schema.model_dump_json())})

            # Stage 4: Validation and Repair Loop
            print("Running Stage 4: Validation and Repair...")
            max_retries = 3
            retries = 0
            is_valid = False
            
            while retries < max_retries and not is_valid:
                validation_result = validate_cross_layer_consistency(app_schema)
                if validation_result.is_valid:
                    is_valid = True
                    break
                
                print(f"Validation failed (Attempt {retries + 1}). Errors: {validation_result.errors}")
                stages.append({"stage": f"validation_error_{retries}", "data": validation_result.errors})
                
                # Repair Request
                repair_prompt = f"""The generated AppSchema has logical inconsistencies. 
                Original Schema: {app_schema.model_dump_json()}
                Validation Errors: {json.dumps(validation_result.errors)}
                
                Please fix these specific errors and output the corrected, full AppSchema. Do not hallucinate new tables or endpoints unless necessary to fix the error. Ensure all references are fully resolved."""
                app_schema, tokens = self.llm.generate_structured(repair_prompt, AppSchema)
                total_tokens += tokens
                stages.append({"stage": f"repaired_schema_{retries}", "data": json.loads(app_schema.model_dump_json())})
                retries += 1

            if not is_valid:
                stages.append({"stage": "fatal_error", "data": "Failed to resolve schema inconsistencies after maximum retries."})
                return {"success": False, "final_schema": json.loads(app_schema.model_dump_json()), "stages": stages, "retries": retries, "total_tokens": total_tokens}

            stages.append({"stage": "final_schema", "data": json.loads(app_schema.model_dump_json())})
            return {"success": True, "final_schema": json.loads(app_schema.model_dump_json()), "stages": stages, "retries": retries, "total_tokens": total_tokens}

        except Exception as e:
            stages.append({"stage": "exception", "data": str(e)})
            return {"success": False, "error": str(e), "stages": stages, "total_tokens": total_tokens}
