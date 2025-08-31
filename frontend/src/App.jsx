import React, { useEffect, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE ?? '/api';

const api = (path, opts = {}) =>
  fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  }).then(r => r.json());


export default function App() {
  const [logged, setLogged] = useState(false)
  const [balance, setBalance] = useState(null)
  const [tx, setTx] = useState([])
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleLogin = async (e) => {
    e.preventDefault()
    setLoading(true); setError("")
    const username = e.target.username.value
    const password = e.target.password.value
    const res = await api('/login', { method: 'POST', body: JSON.stringify({ username, password }) })
    setLoading(false)
    if (res?.token) setLogged(true)
    else setError(res?.error || "Login failed")
  }

  useEffect(() => {
    if (!logged) return
    (async () => {
      const b = await api('/balance')
      const t = await api('/transactions')
      const a = await api('/fraud-alerts')
      setBalance(b)
      setTx(t.items || [])
      setAlerts(a.alerts || [])
    })()
  }, [logged])

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: 24, maxWidth: 900, margin: '0 auto' }}>
      <h1>Secure Banking Dashboard</h1>
      {!logged && (
        <form onSubmit={handleLogin} style={{ display: 'grid', gap: 8, maxWidth: 320 }}>
          <input name="username" placeholder="username" defaultValue="demo@bank.com" />
          <input name="password" placeholder="password" type="password" defaultValue="demo123" />
          <button disabled={loading}>{loading ? 'Logging in...' : 'Login'}</button>
          {error && <div style={{ color: 'crimson' }}>{error}</div>}
          <small>Hint: demo@bank.com / demo123</small>
        </form>
      )}

      {logged && (
        <div style={{ display: 'grid', gap: 16 }}>
          <section style={{ padding: 16, border: '1px solid #e5e5e5', borderRadius: 12 }}>
            <h2>Account</h2>
            {balance ? (
              <div>
                <div><b>Account:</b> {balance.account}</div>
                <div><b>Available:</b> {balance.currency} {balance.available.toLocaleString()}</div>
              </div>
            ) : 'Loading...'}
          </section>

          <section style={{ padding: 16, border: '1px solid #e5e5e5', borderRadius: 12 }}>
            <h2>Recent Transactions</h2>
            <table width="100%" cellPadding="8">
              <thead>
                <tr><th>ID</th><th>Date</th><th>Description</th><th style={{ textAlign: 'right' }}>Amount</th></tr>
              </thead>
              <tbody>
                {tx.map(t => (
                  <tr key={t.id}>
                    <td>{t.id}</td>
                    <td>{t.date}</td>
                    <td>{t.desc}</td>
                    <td style={{ textAlign: 'right', color: t.amount < 0 ? 'crimson' : 'green' }}>{t.amount}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>

          <section style={{ padding: 16, border: '1px solid #e5e5e5', borderRadius: 12, background: '#fff8f8' }}>
            <h2>Fraud Alerts</h2>
            {alerts.length === 0 ? <div>No alerts 🎉</div> : (
              <ul>
                {alerts.map(a => (
                  <li key={a.transaction_id}>
                    Tx #{a.transaction_id} • {a.reason} • {a.date} • {a.desc} • {a.amount}
                  </li>
                ))}
              </ul>
            )}
            <small>Rule: any debit ≥ 50,000 is flagged.</small>
          </section>
        </div>
      )}
    </div>
  )
}
