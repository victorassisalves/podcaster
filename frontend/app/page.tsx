"use client"
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useLogs } from '../context/LogContext'
import { Mic, Zap, Search, Settings, ArrowRight, Sparkles } from 'lucide-react'
import { clsx } from 'clsx'

export default function Home() {
  const [theme, setTheme] = useState('')
  const [loading, setLoading] = useState(false)
  const { addLog } = useLogs()
  const router = useRouter()

  const handleStartResearch = async () => {
    setLoading(true)
    addLog(`Starting deep research for theme: "${theme}"`, 'info')

    try {
      const res = await fetch('http://localhost:8000/api/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ theme })
      })

      if (!res.ok) {
        throw new Error(`Backend returned ${res.status}: ${res.statusText}`)
      }

      const data = await res.json()
      addLog('Research complete successfully!', 'success')
      addLog(`Script Outline generated with ${data.script_outline?.topics_to_approach?.length || 0} topics.`, 'info')

      // Auto-create episode
      addLog('Creating new episode...', 'info')
      const episodeRes = await fetch(`http://localhost:8000/api/episodes?theme=${encodeURIComponent(theme)}`, {
        method: 'POST'
      })
      const episode = await episodeRes.json()
      addLog(`Episode created with ID: ${episode.id}`, 'success')

      setTimeout(() => {
        router.push(`/room/${episode.id}`)
      }, 1500)

    } catch (err: any) {
      console.error(err)
      addLog(`Error during research: ${err.message}`, 'error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="border-b border-gray-800 px-8 py-4 flex items-center justify-between bg-black/50 backdrop-blur-md sticky top-0 z-40">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Mic size={24} className="text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight">Podcaster AI</span>
        </div>
        <div className="flex items-center gap-6 text-sm font-medium text-gray-400">
          <a href="#" className="hover:text-white transition">Dashboard</a>
          <a href="#" className="hover:text-white transition">Recordings</a>
          <div className="h-4 w-[1px] bg-gray-800" />
          <Settings size={20} className="hover:text-white cursor-pointer transition" />
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center p-8 md:p-24 relative overflow-hidden">
        {/* Background Gradients */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-blue-600/10 blur-[120px] rounded-full -z-10" />
        <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-purple-600/10 blur-[100px] rounded-full -z-10" />

        <div className="max-w-3xl w-full text-center space-y-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold uppercase tracking-wider mb-4 animate-in fade-in zoom-in duration-500">
            <Sparkles size={14} />
            <span>Next Generation AI Podcasting</span>
          </div>

          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-white mb-6">
            Create professional <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">podcasts</span> in minutes.
          </h1>

          <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            Our multi-agent system researches your topic, writes a comprehensive script, and hosts a live session with realistic voices.
          </p>

          <div className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 p-2 rounded-2xl shadow-2xl flex flex-col md:flex-row gap-2 max-w-2xl mx-auto ring-1 ring-white/5">
            <div className="flex-1 flex items-center px-4 gap-3">
              <Search className="text-gray-500" size={20} />
              <input
                type="text"
                placeholder="What should we talk about today?"
                className="w-full py-4 bg-transparent text-white focus:outline-none placeholder:text-gray-600"
                value={theme}
                onChange={(e) => setTheme(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && theme && handleStartResearch()}
              />
            </div>
            <button
              onClick={handleStartResearch}
              disabled={loading || !theme}
              className={clsx(
                "px-8 py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all duration-300",
                loading
                  ? "bg-gray-800 text-gray-500 cursor-not-allowed"
                  : "bg-blue-600 text-white hover:bg-blue-500 hover:scale-[1.02] active:scale-[0.98] shadow-[0_0_20px_rgba(37,99,235,0.3)]"
              )}
            >
              {loading ? (
                <>
                  <Zap className="animate-pulse" size={18} />
                  <span>Researching...</span>
                </>
              ) : (
                <>
                  <span>Start Live Show</span>
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </div>

          {/* Quick Options */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 pt-12 animate-in fade-in slide-in-from-bottom-4 duration-700 delay-300">
            <div className="p-4 rounded-xl border border-gray-800 bg-gray-900/30 text-left space-y-2">
              <div className="text-blue-400 text-xs font-bold uppercase tracking-widest">Provider</div>
              <div className="text-white font-medium">Google Gemini 2.0</div>
            </div>
            <div className="p-4 rounded-xl border border-gray-800 bg-gray-900/30 text-left space-y-2">
              <div className="text-purple-400 text-xs font-bold uppercase tracking-widest">Agents</div>
              <div className="text-white font-medium">3 AI Personas</div>
            </div>
            <div className="hidden md:block p-4 rounded-xl border border-gray-800 bg-gray-900/30 text-left space-y-2">
              <div className="text-green-400 text-xs font-bold uppercase tracking-widest">Audio</div>
              <div className="text-white font-medium">Journey (TTS)</div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
