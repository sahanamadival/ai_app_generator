# AI Platform Engineer - Compiler Pipeline

A production-grade, multi-stage LLM-powered compiler that transforms natural language instructions into strictly validated, executable application architectures (JSON schemas).

## 🚀 Core Capabilities

1. **Multi-Stage Generation Pipeline**
   - Breaks complex app generation into 4 deterministic stages: Intent Extraction -> System Architecture Design -> Schema Generation -> Validation & Repair.
2. **Pydantic Validation & Auto-Repair Engine**
   - Enforces strict cross-layer consistency (e.g., UI components must call valid APIs, APIs must read/write to valid DB tables).
   - If the LLM hallucinates an endpoint or table, the engine intercepts the error, injects it back into the prompt, and forces the LLM to auto-repair the schema (up to 3 retries).
3. **Failure Handling System**
   - Automatically detects vague, conflicting, or underspecified inputs.
   - Makes reasonable technical assumptions to resolve logical conflicts and transparently documents them in the frontend UI.
4. **Execution Awareness (Runtime Simulator)**
   - Includes a visual execution simulator in the frontend. Clicking "Simulate Runtime" traces a mocked user action through the generated UI, API middleware, and Database queries to prove the generated schema is structurally flawless and directly usable.
5. **API Token Tracking**
   - Extracts and aggregates token usage straight from the Groq API completion responses and displays the total cost natively in the frontend UI.
6. **Evaluation Framework**
   - Includes a standalone test suite with a dataset of 20 strict prompts (10 real product descriptions, 10 edge cases). 
   - Tracks success rates, average retries, latencies, and categorizes API/Logic failures.

## 🛠️ Tech Stack
- **Backend**: FastAPI, Pydantic, Python 3.10+
- **Frontend**: React 19, Vite, Tailwind CSS v4, Lucide React
- **LLM Provider**: Groq SDK (`llama-3.3-70b-versatile`) for blazing-fast inference and structural JSON enforcement.

---

## 💻 Setup Instructions

### 1. Backend Setup
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Set up your environment variables:
   - Create or open `backend/.env` and replace the placeholder with your actual Groq API key:
   ```env
   GROQ_API_KEY="your_groq_api_key_here"
   ```

3. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### 2. Frontend Setup
1. Open a new terminal and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Start the Vite development server:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to the local server URL (usually `http://localhost:5173`).

---

## 📊 Running Evaluations

To run the automated stress-test suite and capture actual performance metrics, ensure you are in the `backend` folder with the virtual environment activated:

```bash
python evaluate.py
```

*Note: The script rapidly fires 20 massive LLM completion requests. If you are using the free-tier Groq API (limited to 6,000 Tokens Per Minute or 100,000 Tokens Per Day), the script will automatically catch the HTTP 429 Rate Limit errors and log them appropriately in `evaluation_results.json`.*
