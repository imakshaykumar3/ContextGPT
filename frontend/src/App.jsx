import React, { useState, useEffect } from 'react';
import Auth from './Auth';
import Dashboard from './Dashboard';
import MeetingDetail from './MeetingDetail';
import { Bot, LogOut, Loader2 } from 'lucide-react';
import { apiClient } from './api';

export default function App() {
  const [user, setUser] = useState(null);
  const [meetings, setMeetings] = useState([]);
  const [selectedMeeting, setSelectedMeeting] = useState(null);
  const [appLoading, setAppLoading] = useState(true);

  // Validate session validation hooks on mount
  useEffect(() => {
    async function bootSession() {
      try {
        if (apiClient.getToken()) {
          const userData = await apiClient.getMe();
          setUser(userData);
        }
      } catch (err) {
        apiClient.logout();
      } finally {
        setAppLoading(false);
      }
    }
    bootSession();
  }, []);

  const handleCreateMeeting = async (sourceConfig) => {
    // Generate a structural temporary object to display progress loading spinners
    const tempId = Date.now();
    const pendingMeeting = {
      id: tempId,
      title: sourceConfig.type === 'url' ? "Processing External Ingestion Stream..." : `Processing Local Binary: ${sourceConfig.source.name || sourceConfig.source}`,
      date: "Just now",
      status: "processing",
      language: "en",
      data: null
    };

    setMeetings(prev => [pendingMeeting, ...prev]);

    try {
      let pipelineResult;
      
      if (sourceConfig.type === 'url') {
        pipelineResult = await apiClient.processUrl(sourceConfig.source);
      } else {
        pipelineResult = await apiClient.uploadFile(sourceConfig.source);
      }

      // Format response properties to align seamlessly with structural detail elements
      const finalizedMeeting = {
        id: pipelineResult.meeting_id,
        title: pipelineResult.title || "Computed Run Manifest",
        date: "Just now",
        status: "completed",
        language: pipelineResult.language || "en",
        data: pipelineResult // Contains segments, action_items, summary maps
      };

      setMeetings(prev => prev.map(m => m.id === tempId ? finalizedMeeting : m));
    } catch (error) {
      alert(`Pipeline Failed: ${error.message}`);
      setMeetings(prev => prev.filter(m => m.id !== tempId));
    }
  };

  const handleLogout = () => {
    apiClient.logout();
    setUser(null);
    setSelectedMeeting(null);
  };

  if (appLoading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-500" />
      </div>
    );
  }

  if (!user) return <Auth onAuthSuccess={(userData) => setUser(userData)} api={apiClient} />;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <nav className="h-16 border-b border-slate-900 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50 px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        <div className="flex items-center gap-2.5 cursor-pointer" onClick={() => setSelectedMeeting(null)}>
          <div className="p-1.5 bg-indigo-600/10 rounded-lg border border-indigo-500/20">
            <Bot className="w-4 h-4 text-indigo-400" />
          </div>
          <span className="text-sm font-bold tracking-tight text-white">Assistant Hub</span>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right">
            <div className="text-xs font-bold text-slate-200">{user.name}</div>
            <div className="text-[10px] text-slate-500 font-mono tracking-wider">{user.email}</div>
          </div>
          <button onClick={handleLogout} className="p-2 bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-red-400 rounded-lg border border-slate-800 transition-colors">
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </nav>

      <main>
        {selectedMeeting ? (
          <MeetingDetail meeting={selectedMeeting} onBack={() => setSelectedMeeting(null)} api={apiClient} />
        ) : (
          <Dashboard user={user} meetings={meetings} onSelectMeeting={setSelectedMeeting} onCreateMeeting={handleCreateMeeting} />
        )}
      </main>
    </div>
  );
}