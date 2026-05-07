import { useState } from 'react'
import { compileApp, type CompileResponse, simulateApp, type TraceStep } from './api'
import { BrainCircuit, Sparkles, TerminalSquare, CheckCircle2, XCircle, Clock, Check, Copy, Play } from 'lucide-react'
import './App.css'

function App() {
  const [prompt, setPrompt] = useState('Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments. Admins can see analytics.')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<CompileResponse | null>(null)
  const [copied, setCopied] = useState(false)
  const [simulation, setSimulation] = useState<TraceStep[] | null>(null)
  const [simulating, setSimulating] = useState(false)

  const handleCompile = async () => {
    setLoading(true)
    setResult(null)
    setSimulation(null)
    try {
      const data = await compileApp(prompt)
      setResult(data)
    } catch (err) {
      console.error(err)
      alert("Failed to compile. Ensure backend is running.")
    }
    setLoading(false)
  }

  const handleSimulate = async () => {
    if (!result?.final_schema) return;
    setSimulating(true)
    setSimulation(null)
    try {
      const data = await simulateApp(result.final_schema)
      setSimulation(data.trace)
    } catch (err) {
      console.error(err)
      alert("Failed to run simulation.")
    }
    setSimulating(false)
  }

  const copyToClipboard = () => {
    if (result?.final_schema) {
      navigator.clipboard.writeText(JSON.stringify(result.final_schema, null, 2))
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-blue-500/30 pb-20">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-2 sm:space-x-3 overflow-hidden">
            <div className="flex-shrink-0 bg-blue-500/10 p-1.5 sm:p-2 rounded-lg border border-blue-500/20">
              <BrainCircuit className="w-5 h-5 sm:w-6 sm:h-6 text-blue-400" />
            </div>
            <h1 className="text-lg sm:text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 truncate">
              AI Platform Engineer
            </h1>
          </div>
          <div className="flex items-center space-x-4 text-sm text-slate-400 flex-shrink-0 ml-2">
            <span className="flex items-center space-x-1.5 bg-slate-800/50 px-2.5 sm:px-3 py-1 rounded-full border border-slate-700/50">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="hidden sm:inline">System Online</span>
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
        <div className="max-w-3xl mx-auto text-center mb-8 sm:mb-12">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
            Natural Language to <br className="hidden sm:block"/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">Executable Architecture</span>
          </h2>
          <p className="text-slate-400 text-base sm:text-lg">
            Describe your application intent. Our pipeline extracts requirements, designs the system, generates schemas, and validates logic automatically.
          </p>
        </div>

        {/* Input Area */}
        <div className="glass-panel rounded-2xl p-1.5 sm:p-2 mb-10 max-w-4xl mx-auto transition-all duration-300 hover:border-slate-600/50 focus-within:border-blue-500/50 focus-within:ring-4 focus-within:ring-blue-500/10">
          <div className="bg-slate-900/50 rounded-xl p-3 sm:p-4">
            <div className="flex items-center justify-between mb-3">
              <label className="text-sm font-semibold text-slate-300 flex items-center space-x-2">
                <TerminalSquare className="w-4 h-4 text-slate-400" />
                <span>Application Intent Prompt</span>
              </label>
            </div>
            <textarea
              className="w-full h-28 sm:h-32 bg-transparent text-slate-200 placeholder-slate-500 resize-none focus:outline-none text-sm sm:text-base leading-relaxed"
              placeholder="Describe what you want to build..."
              value={prompt}
              onChange={e => setPrompt(e.target.value)}
            />
            <div className="flex justify-end mt-4 pt-4 border-t border-slate-800/50">
              <button
                onClick={handleCompile}
                disabled={loading}
                className={`w-full sm:w-auto flex items-center justify-center space-x-2 px-6 py-2.5 rounded-lg font-medium transition-all duration-200 ${
                  loading 
                  ? 'bg-slate-800 text-slate-400 cursor-not-allowed border border-slate-700' 
                  : 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/25 border border-blue-500'
                }`}
              >
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-slate-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>Compiling Pipeline...</span>
                  </>
                ) : (
                  <>
                    <span>Run Pipeline</span>
                    <Sparkles className="w-4 h-4 ml-1" />
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Results Area */}
        {result && (
          <div className="space-y-6 sm:space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Status Banner */}
            <div className={`flex flex-col sm:flex-row sm:items-center justify-between p-3 sm:p-4 rounded-xl border ${
              result.success 
                ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' 
                : 'bg-rose-500/10 border-rose-500/20 text-rose-400'
            }`}>
              <div className="flex items-center space-x-3 mb-2 sm:mb-0">
                {result.success ? <CheckCircle2 className="w-5 h-5 sm:w-6 sm:h-6 flex-shrink-0" /> : <XCircle className="w-5 h-5 sm:w-6 sm:h-6 flex-shrink-0" />}
                <span className="font-semibold text-base sm:text-lg">
                  {result.success ? 'Compilation Successful' : 'Compilation Failed'}
                </span>
              </div>
              <div className="flex flex-wrap gap-2 items-center">
                {result.total_tokens !== undefined && (
                  <div className={`flex items-center space-x-2 text-xs sm:text-sm px-3 py-1.5 rounded-lg border ${
                    result.total_tokens > 4000 ? 'bg-amber-500/10 border-amber-500/20 text-amber-400' : 'bg-slate-900/50 border-slate-700/50 text-slate-300'
                  }`} title="Tracks how close you are to the Groq API rate limit (6000 TPM for free tier).">
                    <BrainCircuit className="w-4 h-4 opacity-70" />
                    <span>Tokens: <span className="font-bold">{result.total_tokens.toLocaleString()}</span></span>
                  </div>
                )}
                <div className="flex items-center space-x-2 text-xs sm:text-sm bg-slate-900/50 px-3 py-1.5 rounded-lg border border-slate-700/50 text-slate-300">
                  <Clock className="w-4 h-4 opacity-70" />
                  <span>Retries used: <span className="font-bold">{result.retries}</span> / 3</span>
                </div>
              </div>
            </div>

            {/* Assumptions Alert (Failure Handling) */}
            {result.stages?.[0]?.data?.assumptions_made?.length > 0 && (
              <div className="bg-amber-500/10 border border-amber-500/20 rounded-xl p-4 sm:p-5">
                <div className="flex items-start space-x-3">
                  <TerminalSquare className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-amber-400 font-bold mb-2">Failure Handling: Assumptions Made</h4>
                    <p className="text-sm text-slate-300 mb-3">The prompt was vague or underspecified. The AI Platform Engineer made the following technical assumptions to ensure a complete, working system:</p>
                    <ul className="list-disc pl-5 space-y-1 text-sm text-slate-300">
                      {result.stages[0].data.assumptions_made.map((assumption: string, idx: number) => (
                        <li key={idx}>{assumption}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 sm:gap-8 items-start">
              {/* Pipeline Stages (Left Column) */}
              <div className="lg:col-span-5 space-y-4">
                <h3 className="text-lg sm:text-xl font-bold text-slate-200 flex items-center space-x-2 mb-4 sm:mb-6">
                  <span className="bg-slate-800 p-1 sm:p-1.5 rounded border border-slate-700">
                    <BrainCircuit className="w-4 h-4 sm:w-5 sm:h-5 text-purple-400" />
                  </span>
                  <span>Execution Trace</span>
                </h3>
                
                <div className="space-y-4 sm:space-y-6">
                  {result.stages.map((stage, idx) => (
                    <div key={idx} className="relative flex items-start group">
                      {/* Vertical Line */}
                      {idx !== result.stages.length - 1 && (
                        <div className="absolute left-[11px] top-6 bottom-[-24px] sm:bottom-[-32px] w-0.5 bg-slate-800"></div>
                      )}
                      
                      {/* Dot */}
                      <div className="flex-shrink-0 mt-1 mr-3 sm:mr-4 relative z-10 w-6 h-6 flex items-center justify-center bg-slate-900 rounded-full border border-slate-700 group-hover:border-purple-500 transition-colors shadow-[0_0_10px_rgba(168,85,247,0.1)] group-hover:shadow-[0_0_10px_rgba(168,85,247,0.4)]">
                        <div className="w-2 h-2 rounded-full bg-purple-500"></div>
                      </div>

                      {/* Content */}
                      <div className="flex-1 bg-slate-900/50 border border-slate-800 rounded-xl p-4 hover:border-slate-700 transition-colors min-w-0">
                        <h4 className="text-sm font-bold text-purple-400 mb-3 flex items-center capitalize truncate">
                          {stage.stage.replace(/_/g, ' ')}
                        </h4>
                        <div className="bg-slate-950 rounded-lg p-3 overflow-x-auto border border-slate-800/50">
                          <pre className="text-[10px] sm:text-[11px] text-slate-300 font-mono">
                            {JSON.stringify(stage.data, null, 2)}
                          </pre>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Final Schema (Right Column) */}
              <div className="lg:col-span-7 lg:sticky lg:top-24 mt-6 lg:mt-0">
                <div className="glass-panel rounded-xl overflow-hidden flex flex-col h-auto lg:h-[calc(100vh-120px)] max-h-[800px]">
                  <div className="bg-slate-900 px-3 sm:px-4 py-2 sm:py-3 border-b border-slate-800 flex items-center justify-between">
                    <div className="flex items-center space-x-2 truncate pr-2">
                      <TerminalSquare className="w-4 h-4 text-slate-400 flex-shrink-0" />
                      <span className="font-semibold text-xs sm:text-sm text-slate-200 truncate">Final Executable Schema</span>
                    </div>
                    <div className="flex items-center space-x-2 flex-shrink-0">
                      <span className="text-[9px] sm:text-[10px] font-mono bg-blue-500/20 text-blue-300 px-1.5 sm:px-2 py-0.5 rounded border border-blue-500/30">
                        application/json
                      </span>
                      {result.final_schema && (
                        <button 
                          onClick={copyToClipboard}
                          className="p-1 sm:p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded transition-colors"
                          title="Copy to clipboard"
                        >
                          {copied ? <Check className="w-3 h-3 sm:w-4 sm:h-4 text-green-400" /> : <Copy className="w-3 h-3 sm:w-4 sm:h-4" />}
                        </button>
                      )}
                    </div>
                  </div>
                  <div className="flex-1 p-0 overflow-auto bg-[#0d1117] relative">
                    {result.final_schema ? (
                      <div className="p-4 sm:p-6 h-[400px] lg:h-auto">
                        <pre className="text-xs sm:text-sm text-emerald-400 font-mono leading-relaxed">
                          {JSON.stringify(result.final_schema, null, 2)}
                        </pre>
                      </div>
                    ) : (
                      <div className="h-[400px] flex flex-col items-center justify-center text-slate-500 p-6 sm:p-8 text-center">
                        <XCircle className="w-10 h-10 sm:w-12 sm:h-12 text-rose-500/30 mb-3 sm:mb-4" />
                        <p className="text-sm sm:text-base">No final schema generated.</p>
                        {result.error && (
                          <p className="mt-2 text-xs sm:text-sm text-rose-400 font-mono bg-rose-500/10 p-2 sm:p-3 rounded-lg border border-rose-500/20 w-full overflow-hidden text-ellipsis">
                            {result.error}
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                  
                  {/* Simulate Runtime Button Area */}
                  {result.final_schema && (
                    <div className="p-4 border-t border-slate-800 bg-slate-900 flex justify-between items-center">
                      <span className="text-sm text-slate-400">Ready for execution test</span>
                      <button
                        onClick={handleSimulate}
                        disabled={simulating}
                        className="flex items-center space-x-2 px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
                      >
                        {simulating ? (
                           <>
                             <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                             </svg>
                             <span>Simulating...</span>
                           </>
                        ) : (
                          <>
                            <span>Simulate Runtime</span>
                            <Play className="w-4 h-4 ml-1" />
                          </>
                        )}
                      </button>
                    </div>
                  )}

                  {/* Simulation Trace Output */}
                  {simulation && (
                    <div className="border-t border-slate-800 bg-[#0a0a0a] p-4 sm:p-6 overflow-auto max-h-[300px]">
                      <h4 className="text-sm font-bold text-slate-200 mb-4 flex items-center space-x-2">
                        <TerminalSquare className="w-4 h-4 text-purple-400" />
                        <span>Execution Trace Terminal</span>
                      </h4>
                      <div className="space-y-3 font-mono text-xs sm:text-sm">
                        {simulation.map((step, idx) => (
                          <div key={idx} className="flex items-start space-x-3">
                            <span className="text-slate-500 flex-shrink-0 mt-0.5">[{new Date().toLocaleTimeString().split(' ')[0]}]</span>
                            <span className={`flex-shrink-0 mt-0.5 font-semibold ${
                              step.status === 'success' ? 'text-emerald-400' :
                              step.status === 'error' || step.status === 'failed' ? 'text-rose-400' :
                              step.status === 'warning' ? 'text-amber-400' : 'text-blue-400'
                            }`}>
                              [{step.step}]
                            </span>
                            <span className="text-slate-300">{step.message}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
