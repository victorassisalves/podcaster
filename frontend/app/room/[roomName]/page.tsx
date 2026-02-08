"use client"
import {
  LiveKitRoom,
  VideoConference,
  RoomAudioRenderer,
  ControlBar,
  MessageFormatter,
  useParticipants,
  AudioVisualizer,
} from '@livekit/components-react';
import '@livekit/components-styles';
import { useEffect, useState, useMemo } from 'react';
import { useLogs } from '../../context/LogContext';
import { Mic, Users, ScrollText, Radio, LogOut, ChevronLeft } from 'lucide-react';
import Link from 'next/link';

export default function PodcastRoom({ params }: { params: { roomName: string } }) {
  const [token, setToken] = useState<string | null>(null);
  const { addLog } = useLogs();
  const [view, setView] = useState<'booth' | 'script'>('booth');

  useEffect(() => {
    (async () => {
      addLog(`Requesting token for room: ${params.roomName}`, 'info');
      try {
        const res = await fetch(`http://localhost:8000/api/token?room=${params.roomName}&identity=human-host-${Math.floor(Math.random() * 1000)}`);
        const data = await res.json();
        setToken(data.token);
        addLog('Successfully joined LiveKit session', 'success');
      } catch (err: any) {
        addLog(`Failed to join room: ${err.message}`, 'error');
      }
    })();
  }, [params.roomName]);

  if (!token) return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-950 gap-4">
      <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      <div className="text-gray-400 font-medium animate-pulse">Initializing Podcast Booth...</div>
    </div>
  );

  return (
    <div className="h-screen flex flex-col bg-black text-white overflow-hidden">
      <LiveKitRoom
        video={false}
        audio={true}
        token={token}
        serverUrl={process.env.NEXT_PUBLIC_LIVEKIT_URL}
        data-lk-theme="default"
        className="flex-1 flex flex-col"
        onDisconnected={() => addLog('Disconnected from room', 'warning')}
      >
        {/* Room Header */}
        <header className="h-16 border-b border-gray-800 flex items-center justify-between px-6 bg-gray-900/50">
          <div className="flex items-center gap-4">
            <Link href="/" className="p-2 hover:bg-gray-800 rounded-lg transition text-gray-400 hover:text-white">
              <ChevronLeft size={20} />
            </Link>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
              <span className="font-bold tracking-tight uppercase text-xs text-gray-400">Live Session</span>
              <span className="text-sm font-medium ml-2">{params.roomName}</span>
            </div>
          </div>

          <div className="flex bg-gray-950 p-1 rounded-xl border border-gray-800">
            <button
              onClick={() => setView('booth')}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition ${view === 'booth' ? 'bg-blue-600 text-white shadow-lg' : 'text-gray-400 hover:text-white'}`}
            >
              <div className="flex items-center gap-2">
                <Mic size={14} />
                <span>Booth</span>
              </div>
            </button>
            <button
              onClick={() => setView('script')}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition ${view === 'script' ? 'bg-blue-600 text-white shadow-lg' : 'text-gray-400 hover:text-white'}`}
            >
              <div className="flex items-center gap-2">
                <ScrollText size={14} />
                <span>Script</span>
              </div>
            </button>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden md:flex flex-col items-end mr-2">
              <span className="text-[10px] text-gray-500 font-bold uppercase">Host Identity</span>
              <span className="text-xs text-blue-400">Human Producer</span>
            </div>
            <button className="p-2 bg-red-500/10 text-red-500 hover:bg-red-500 hover:text-white rounded-lg transition" title="Leave Session">
              <LogOut size={20} />
            </button>
          </div>
        </header>

        <div className="flex-1 flex overflow-hidden">
          {/* Main Content Area */}
          <div className="flex-1 p-6 overflow-y-auto">
            {view === 'booth' ? (
              <div className="h-full flex flex-col gap-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 flex-1">
                  {/* Participant List / Grid */}
                  <div className="bg-gray-900/30 rounded-3xl border border-gray-800 p-6 flex flex-col">
                    <div className="flex items-center gap-2 mb-6">
                      <Users size={18} className="text-blue-400" />
                      <h2 className="font-bold">Active Participants</h2>
                    </div>
                    <VideoConference />
                  </div>

                  {/* Visualizer / Status Area */}
                  <div className="bg-gray-900/30 rounded-3xl border border-gray-800 p-8 flex flex-col items-center justify-center relative overflow-hidden group">
                     <div className="absolute inset-0 bg-blue-600/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                     <div className="w-48 h-48 bg-blue-600/20 rounded-full flex items-center justify-center animate-pulse border-2 border-blue-500/20 relative z-10">
                        <Radio size={64} className="text-blue-500" />
                     </div>
                     <h3 className="text-2xl font-bold mt-8 mb-2">Podcast Live</h3>
                     <p className="text-gray-400 text-center max-w-xs text-sm">
                       AI Agents are currently processing the script and engaging in the conversation.
                     </p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="max-w-3xl mx-auto py-8">
                 <div className="space-y-8">
                    <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 inline-block">Production Script</h2>
                    <div className="prose prose-invert max-w-none">
                      <p className="text-gray-400 italic">Script content is generated by Gemini 2.0 based on your chosen theme.</p>
                      {/* Placeholder for real script data */}
                      <div className="mt-8 space-y-6">
                        {[1, 2, 3].map(i => (
                          <div key={i} className="p-6 bg-gray-900/50 rounded-2xl border border-gray-800 border-l-4 border-l-blue-500">
                            <h4 className="text-blue-400 font-bold mb-2 uppercase text-xs tracking-widest">Section {i}</h4>
                            <div className="h-4 w-3/4 bg-gray-800 rounded mb-2" />
                            <div className="h-4 w-1/2 bg-gray-800 rounded" />
                          </div>
                        ))}
                      </div>
                    </div>
                 </div>
              </div>
            )}
          </div>
        </div>

        {/* LiveKit Controls */}
        <div className="bg-gray-950 border-t border-gray-800 p-4 flex justify-center sticky bottom-0 z-30">
          <ControlBar variation="minimal" />
        </div>

        <RoomAudioRenderer />
      </LiveKitRoom>
    </div>
  );
}
