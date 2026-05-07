import os
import json
from typing import Type, TypeVar, Any
from pydantic import BaseModel, ValidationError
from groq import Groq

T = TypeVar('T', bound=BaseModel)

class LLMProvider:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            print("WARNING: GROQ_API_KEY is not set.")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        # Use llama-3.3-70b-versatile for complex reasoning/structured JSON
        self.model_name = "llama-3.3-70b-versatile"

    def generate_structured(self, prompt: str, response_schema: Type[T], max_retries: int = 3) -> tuple[T, int]:
        """
        Calls the LLM and forces the output to match the provided Pydantic schema.
        Includes a CORE Repair Engine that detects invalid JSON, missing keys, schema 
        mismatches, and automatically prompts the LLM to fix specific fields.
        Returns a tuple of (parsed_schema, total_tokens_used).
        """
        if not self.client:
             raise ValueError("LLM client not initialized. Check your API key.")

        # Groq supports JSON mode but to enforce schema, we can inject it into the prompt
        schema_json = response_schema.model_json_schema()
        
        system_prompt = (
            "You are a strict JSON compiler. You MUST output ONLY valid JSON that matches "
            "the provided JSON schema exactly. Do not output any markdown formatting, explanations, or text "
            "outside of the JSON block."
        )

        user_prompt = (
            f"{prompt}\n\n"
            f"Here is the JSON schema you MUST follow:\n{json.dumps(schema_json)}\n\n"
            f"Output JSON:"
        )

        total_tokens = 0

        for attempt in range(max_retries):
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1, # low temp for determinism
            )
            
            if response.usage and response.usage.total_tokens:
                total_tokens += response.usage.total_tokens
                
            response_text = response.choices[0].message.content
            if not response_text:
                if attempt == max_retries - 1:
                    raise ValueError("Empty response from LLM")
                continue
                
            try:
                # CORE ENGINE: This catches invalid JSON, missing keys, hallucinated fields, and schema mismatches!
                parsed = response_schema.model_validate_json(response_text)
                return parsed, total_tokens
            except ValidationError as e:
                if attempt == max_retries - 1:
                    raise ValueError(f"Failed to generate valid schema after {max_retries} attempts. Last validation error: {str(e)}")
                
                # REPAIR AUTOMATICALLY: Feed the exact error back to regenerate specific parts
                print(f"Validation Error caught in LLM layer. Auto-repairing attempt {attempt + 1}...")
                error_details = e.errors()
                user_prompt += f"\n\nERROR: Your previous JSON failed schema validation. DO NOT blindly retry. Fix these specific schema mismatches/missing keys:\n{json.dumps(error_details)}\n\nOutput the repaired JSON:"

# Singleton instance
llm_provider = LLMProvider()
