export interface CompileResponse {
  success: boolean;
  final_schema?: any;
  stages: { stage: string; data: any }[];
  retries: number;
  total_tokens?: number;
  error?: string;
}

export const compileApp = async (prompt: string): Promise<CompileResponse> => {
  const res = await fetch("http://localhost:8000/api/compile", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });
  if (!res.ok) {
    throw new Error(`API returned ${res.status}`);
  }
  return res.json();
};

export interface TraceStep {
  step: string;
  message: string;
  status: 'success' | 'info' | 'warning' | 'error' | 'failed';
}

export interface SimulateResponse {
  success: boolean;
  trace: TraceStep[];
}

export const simulateApp = async (schema: any): Promise<SimulateResponse> => {
  const res = await fetch("http://localhost:8000/api/simulate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(schema),
  });
  if (!res.ok) {
    throw new Error(`API returned ${res.status}`);
  }
  return res.json();
};
