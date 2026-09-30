import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [claim, setClaim] = useState('')
  const [unit, setUnit] = useState('')
  const [visuallyVerifiable, setVisuallyVerifiable] = useState(false)
  const [sourceReliability, setSourceReliability] = useState(0.8)
  const [actionRisk, setActionRisk] = useState(0.5)
  
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  const [history, setHistory] = useState([])
  const [activeTab, setActiveTab] = useState('verify') // 'verify' or 'history'

  const verifyClaim = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    
    try {
      const res = await axios.post('http://localhost:8001/verify', {
        agent_response: claim,
        context: {
          unit: unit,
          visually_verifiable: visuallyVerifiable,
          source_reliability: parseFloat(sourceReliability),
          action_risk: parseFloat(actionRisk)
        }
      })
      setResult(res.data)
      fetchHistory()
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  const fetchHistory = async () => {
    try {
      const res = await axios.get('http://localhost:8001/history')
      setHistory(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    fetchHistory()
  }, [])

  const getDecisionStyles = (decision) => {
    if (decision === 'APPROVE') return { color: '#059669', bg: '#d1fae5', border: '#34d399' }
    if (decision === 'HUMAN_REVIEW') return { color: '#d97706', bg: '#fef3c7', border: '#fbbf24' }
    return { color: '#dc2626', bg: '#fee2e2', border: '#f87171' }
  }

  return (
    <div className="dashboard-container">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo-icon">TA</div>
          <h2>TrustAgent</h2>
        </div>
        <nav className="sidebar-nav">
          <button 
            className={`nav-item ${activeTab === 'verify' ? 'active' : ''}`}
            onClick={() => setActiveTab('verify')}
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
            Verification Desk
          </button>
          <button 
            className={`nav-item ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            Audit Logs
          </button>
        </nav>
        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="avatar">A</div>
            <div>
              <div className="user-name">Admin User</div>
              <div className="user-role">Compliance Officer</div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="main-content">
        <header className="topbar">
          <div className="page-title">
            <h1>{activeTab === 'verify' ? 'Verification Desk' : 'Audit Logs'}</h1>
            <p className="subtitle">
              {activeTab === 'verify' 
                ? 'Evaluate AI agent claims against multi-modal evidence.' 
                : 'Review historical verification decisions and system logs.'}
            </p>
          </div>
        </header>

        <div className="content-wrapper">
          {activeTab === 'verify' ? (
            <div className="dashboard-grid">
              {/* Left Column: Form */}
              <div className="card form-card">
                <div className="card-header">
                  <h3>New Verification Request</h3>
                </div>
                <div className="card-body">
                  <form onSubmit={verifyClaim}>
                    <div className="form-group">
                      <label>Agent Claim / Response</label>
                      <textarea 
                        value={claim} 
                        onChange={(e) => setClaim(e.target.value)} 
                        placeholder="e.g. Price of GameStation X1 is 499 USD."
                        required
                      />
                    </div>
                    
                    <div className="form-row">
                      <div className="form-group">
                        <label>Unit of Measurement (Optional)</label>
                        <input type="text" value={unit} onChange={(e) => setUnit(e.target.value)} placeholder="e.g. USD, inches" />
                      </div>
                      <div className="form-group">
                        <label className="checkbox-label">
                          <input type="checkbox" checked={visuallyVerifiable} onChange={(e) => setVisuallyVerifiable(e.target.checked)} />
                          <span>Visually Verifiable Attribute</span>
                        </label>
                      </div>
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label>Source Reliability (0.0 - 1.0)</label>
                        <input type="number" step="0.1" min="0" max="1" value={sourceReliability} onChange={(e) => setSourceReliability(e.target.value)} />
                      </div>
                      <div className="form-group">
                        <label>Action Risk (0.0 - 1.0)</label>
                        <input type="number" step="0.1" min="0" max="1" value={actionRisk} onChange={(e) => setActionRisk(e.target.value)} />
                      </div>
                    </div>

                    <div className="form-actions">
                      <button type="submit" disabled={loading} className="btn-primary">
                        {loading ? (
                          <><span className="loading-spinner"></span> Processing...</>
                        ) : 'Execute Verification'}
                      </button>
                    </div>
                  </form>
                </div>
              </div>

              {/* Right Column: Result */}
              <div className="result-column">
                {error && (
                  <div className="card alert-card error">
                    <div className="alert-icon">!</div>
                    <div>
                      <strong>System Error</strong>
                      <p>{error}</p>
                    </div>
                  </div>
                )}
                
                {!result && !error && (
                  <div className="card empty-state-card">
                    <div className="empty-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    </div>
                    <h3>Awaiting Request</h3>
                    <p>Submit a claim on the left to view the decision analysis.</p>
                  </div>
                )}

                {result && (() => {
                  const styles = getDecisionStyles(result.decision);
                  return (
                    <div className="card result-card">
                      <div className="card-header border-bottom">
                        <h3>Decision Analysis</h3>
                        <div className="decision-badge" style={{ backgroundColor: styles.bg, color: styles.color, border: `1px solid ${styles.border}` }}>
                          {result.decision}
                        </div>
                      </div>
                      
                      <div className="card-body">
                        <div className="score-section">
                          <div className="score-circle" style={{ borderColor: styles.color, backgroundColor: styles.bg }}>
                            <div className="score-value" style={{ color: styles.color }}>{result.trust_score}</div>
                          </div>
                          <div className="score-meta">
                            <h4>Trust Score</h4>
                            <p>Calculated by TrustScoreNet</p>
                          </div>
                        </div>
                        
                        <div className="explanation-section">
                          <h4>System Explanation</h4>
                          <div className="explanation-box">
                            <pre>{result.explanation}</pre>
                          </div>
                        </div>
                        
                        <div className="modality-details">
                          <h4>Verifier Diagnostics</h4>
                          <div className="modality-grid">
                            {result.claims[0].modality_scores.text.label !== 'NO_EVIDENCE' && (
                              <div className="modality-card">
                                <div className="modality-header">Text Engine</div>
                                <div className="modality-status" style={{ color: result.claims[0].modality_scores.text.label === 'SUPPORT' ? '#059669' : '#dc2626' }}>
                                  {result.claims[0].modality_scores.text.label}
                                </div>
                                <div className="modality-conf">Conf: {(result.claims[0].modality_scores.text.score * 100).toFixed(1)}%</div>
                              </div>
                            )}
                            {result.claims[0].modality_scores.image.label !== 'NO_EVIDENCE' && (
                              <div className="modality-card">
                                <div className="modality-header">Image Engine</div>
                                <div className="modality-status" style={{ color: result.claims[0].modality_scores.image.label === 'SUPPORT' ? '#059669' : '#dc2626' }}>
                                  {result.claims[0].modality_scores.image.label}
                                </div>
                                <div className="modality-conf">Conf: {(result.claims[0].modality_scores.image.score * 100).toFixed(1)}%</div>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  )
                })()}
              </div>
            </div>
          ) : (
            /* History View */
            <div className="card data-table-card">
              <div className="card-header border-bottom">
                <h3>Verification Audit Logs</h3>
                <div className="table-actions">
                  <span className="record-count">Total Records: {history.length}</span>
                </div>
              </div>
              <div className="card-body no-padding">
                {history.length === 0 ? (
                  <div className="empty-state">No historical data available.</div>
                ) : (
                  <div className="table-responsive">
                    <table className="data-table">
                      <thead>
                        <tr>
                          <th>ID</th>
                          <th>Claim Evaluated</th>
                          <th>Date & Time</th>
                          <th>Score</th>
                          <th>Decision</th>
                        </tr>
                      </thead>
                      <tbody>
                        {history.map((h) => {
                          const styles = getDecisionStyles(h.decision);
                          return (
                            <tr key={h.id}>
                              <td className="col-id">#{h.id}</td>
                              <td className="col-claim">
                                <div className="truncate-text" title={h.claim}>{h.claim}</div>
                              </td>
                              <td className="col-date">
                                {new Date(h.created_at).toLocaleString(undefined, {
                                  month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                                })}
                              </td>
                              <td className="col-score">
                                <strong>{h.trust_score}</strong>
                              </td>
                              <td className="col-decision">
                                <span className="status-pill" style={{ backgroundColor: styles.bg, color: styles.color, border: `1px solid ${styles.border}` }}>
                                  {h.decision}
                                </span>
                              </td>
                            </tr>
                          )
                        })}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
