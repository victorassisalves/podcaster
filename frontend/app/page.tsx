"use client"
import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function Home() {
  const [theme, setTheme] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const handleStartResearch = async () => {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/api/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ theme })
      })
      const data = await res.json()
      // Redirect to episode page or show results
      alert('Research complete! Outline: ' + JSON.stringify(data.script_outline))
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-8">Podcaster AI</h1>
      <div className="w-full max-w-md space-y-4">
        <input
          type="text"
          placeholder="Enter Podcast Theme..."
          className="w-full p-4 rounded bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={theme}
          onChange={(e) => setTheme(e.target.value)}
        />
        <button
          onClick={handleStartResearch}
          disabled={loading || !theme}
          className="w-full p-4 bg-blue-600 rounded font-bold hover:bg-blue-700 disabled:opacity-50 transition"
        >
          {loading ? 'Researching...' : 'Start Deep Research'}
        </button>
      </div>
    </main>
  )
}
