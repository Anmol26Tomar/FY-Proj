import { useState } from 'react'
import axios from 'axios'
import { Search, Loader2, CheckCircle2, FileText, Activity } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

const Dashboard = () => {
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [logs, setLogs] = useState([])
  const [draft, setDraft] = useState(null)

  const handleResearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setIsLoading(true)
    setLogs(['Initiating Scholar-Agent multi-agent workflow...'])
    setDraft(null)

    try {
      setLogs(prev => [...prev, "System: Dispatching request to LangGraph Orchestration..."])
      
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await axios.post(`${API_URL}/api/research`, {
        query: query
      })
      
      setLogs(response.data.logs)
      setDraft(response.data.draft)
    } catch (error) {
      console.error(error)
      setLogs(prev => [...prev, `Error: ${error.message}`])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="wrapper">
      <div className="dash-header">
        <h1 className="dash-title">
          Automate your <span>Literature Review</span>
        </h1>
        <p className="dash-subtitle">
          Enter a research topic below. Our multi-agent orchestration will retrieve, critique, and synthesize a verified review.
        </p>
      </div>

      <div className="glass-card">
         <form onSubmit={handleResearch} className="search-bar">
            <div className="search-input-wrapper">
              <Search className="icon-left" size={24} />
              <input 
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="The impact of quantum error correction..."
                className="search-input"
                disabled={isLoading}
              />
            </div>
            <button 
              type="submit"
              disabled={isLoading || !query.trim()}
              className="btn btn-primary"
            >
              {isLoading ? (
                <><Loader2 className="animate-spin" size={20} /> Synthesizing</>
              ) : (
                'Research'
              )}
            </button>
         </form>
      </div>

      <div className="dash-grid">
        <div className="glass-card panel">
          <div className="panel-header" style={{ color: 'var(--brand-primary)' }}>
            <Activity size={20} />
            <span>Orchestration Logs</span>
          </div>
          <div className="panel-content">
            {logs.length === 0 && !isLoading && (
              <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', fontSize: 'var(--fs-sm)' }}>
                No agent activity yet. Awaiting search query.
              </p>
            )}
            {logs.map((log, index) => (
              <div key={index} className="log-item">
                <div style={{ flexShrink: 0, marginTop: '2px' }}>
                  {index === logs.length - 1 && isLoading ? (
                    <Loader2 size={16} className="animate-spin" style={{ color: 'var(--brand-primary)' }} />
                  ) : (
                    <CheckCircle2 size={16} style={{ color: '#22c55e' }} />
                  )}
                </div>
                <p>{log}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-card panel">
          <div className="panel-header" style={{ color: '#3b82f6' }}>
            <FileText size={20} />
            <span>Drafted Synthesis</span>
          </div>
          
          <div className="panel-content">
            {draft ? (
              <div className="markdown-body">
                <ReactMarkdown
                  components={{
                    a: ({node, ...props}) => <a {...props} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--brand-primary)', textDecoration: 'underline', textUnderlineOffset: '2px' }} />
                  }}
                >
                  {draft}
                </ReactMarkdown>
              </div>
            ) : (
               <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)', opacity: 0.5, gap: '1rem', textAlign: 'center' }}>
                <FileText size={64} style={{ opacity: 0.5 }} />
                <p style={{ maxWidth: '250px' }}>Your drafted literature review will securely render here.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
