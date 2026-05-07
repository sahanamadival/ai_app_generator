import asyncio
import json
import time
import os
from dotenv import load_dotenv
load_dotenv()

from app.compiler import Compiler

def load_dataset():
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset", "prompts.json")
    with open(dataset_path, "r") as f:
        data = json.load(f)
    
    prompts = data["real_prompts"] + [item["prompt"] for item in data["edge_cases"]]
    return prompts

PROMPTS = load_dataset()

async def run_evaluation():
    compiler = Compiler()
    results = []
    
    print(f"Starting evaluation of {len(PROMPTS)} prompts...")
    
    for i, prompt in enumerate(PROMPTS):
        print(f"\n--- Evaluating Prompt {i+1}/{len(PROMPTS)} ---")
        print(f"Prompt: {prompt}")
        
        start_time = time.time()
        result = compiler.compile(prompt)
        latency = time.time() - start_time
        
        failure_type = "None"
        if not result.get("success"):
            error_str = str(result.get("error", ""))
            if "fatal_error" in [s.get("stage") for s in result.get("stages", [])]:
                failure_type = "Logical Inconsistency (Unrepairable)"
            elif "Empty response" in error_str:
                failure_type = "API Timeout/Empty"
            else:
                failure_type = "JSON Schema Validation Failure"
                
        eval_result = {
            "prompt": prompt,
            "success": result.get("success", False),
            "retries": result.get("retries", 0),
            "latency_seconds": round(latency, 2),
            "stages_count": len(result.get("stages", [])),
            "failure_type": failure_type,
            "error": result.get("error") if not result.get("success") else None
        }
        
        print(f"Success: {eval_result['success']}, Retries: {eval_result['retries']}, Latency: {eval_result['latency_seconds']}s")
        results.append(eval_result)
        
    # Summary
    success_count = sum(1 for r in results if r["success"])
    total_retries = sum(r["retries"] for r in results)
    avg_latency = sum(r["latency_seconds"] for r in results) / len(results) if results else 0
    failure_types = {}
    for r in results:
        if not r["success"]:
            failure_types[r["failure_type"]] = failure_types.get(r["failure_type"], 0) + 1
            
    print("\n=== EVALUATION SUMMARY ===")
    print(f"Total Prompts: {len(PROMPTS)}")
    print(f"Success Rate: {(success_count / len(PROMPTS)) * 100}%")
    print(f"Average Retries per Request: {total_retries / len(PROMPTS)}")
    print(f"Average Latency: {round(avg_latency, 2)}s")
    print(f"Failure Types: {failure_types}")
    
    summary = {
        "Total Prompts": len(PROMPTS),
        "Success Rate": f"{(success_count / len(PROMPTS)) * 100}%",
        "Average Retries per Request": total_retries / len(PROMPTS),
        "Average Latency": f"{round(avg_latency, 2)}s",
        "Failure Types": failure_types
    }
    
    with open("evaluation_results.json", "w") as f:
        json.dump({"summary": summary, "details": results}, f, indent=2)
        
    print("Results saved to evaluation_results.json")

if __name__ == "__main__":
    asyncio.run(run_evaluation())
