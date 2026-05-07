from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

from app.compiler import Compiler
from app.simulator import RuntimeSimulator
from app.models import AppSchema

app = FastAPI(title="AI Platform Engineer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

compiler = Compiler()

class CompileRequest(BaseModel):
    prompt: str

@app.post("/api/compile")
async def compile_app(request: CompileRequest):
    """
    Takes a natural language prompt and returns a full, validated application schema.
    """
    result = compiler.compile(request.prompt)
    return result

@app.post("/api/simulate")
async def simulate_app(schema: AppSchema):
    """
    Takes a generated AppSchema and simulates a runtime execution trace.
    """
    try:
        simulator = RuntimeSimulator(schema)
        trace = simulator.simulate()
        return {"success": True, "trace": trace}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "AI Platform Engineer API is running! Go to /docs to see the API documentation."}
