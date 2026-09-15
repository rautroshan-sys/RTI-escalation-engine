import React, { useState } from 'react'
import ResultCard from './components/ResultCard'

function App() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, state_code: "MH" }) 
      })
      
      if (!response.ok) throw new Error('API Error')
      
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError('Failed to connect to the AI Engine. Is the FastAPI server running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto space-y-8">
        
        <div className="text-center">
          <h1 className="text-4xl font-extrabold text-gray-900">RTI Routing Engine</h1>
        </div>

        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Enter RTI Application Text
          </label>
          <textarea
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            rows="4"
            placeholder="e.g., The road in front of my house is full of potholes..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="mt-4 w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-blue-300 transition-colors"
          >
            {loading ? 'Analyzing with AI...' : 'Process Application'}
          </button>
        </form>

        {error && <div className="p-4 bg-red-50 text-red-700 rounded-lg">{error}</div>}
        
        {result && <ResultCard result={result} />}

      </div>
    </div>
  )
}

export default App