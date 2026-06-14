import React, { useState, useEffect } from 'react';
import { 
  ArrowLeft, MessageSquare, Send, Sparkles, ShieldCheck, 
  ClipboardList, CheckSquare, HelpCircle, Bookmark, Loader2, 
  FileText, Calendar, User2, Activity
} from 'lucide-react';

export default function MeetingDetail({ meeting, onBack, api }) {
  const [activeTab, setActiveTab] = useState('action_items');
  const [chatInput, setChatInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [currentMeeting, setCurrentMeeting] = useState(meeting);
  const [messages, setMessages] = useState([
    { role: 'assistant', text: "Vector context engine online. Ask any system prompt anchored strictly to this transcript's contextual architecture." }
  ]);

  useEffect(() => {
    async function loadFullMeetingPayload() {
      const hasSegments = (currentMeeting.segments && currentMeeting.segments.length > 0) || 
                         (currentMeeting.data?.segments && currentMeeting.data.segments.length > 0);
      const hasTranscript = (currentMeeting.transcript && currentMeeting.transcript.trim() !== "") || 
                            (currentMeeting.data?.transcript && currentMeeting.data.transcript.trim() !== "");

      if (!hasSegments && !hasTranscript) {
        setLoadingDetails(true);
        try {
          const targetId = currentMeeting.id || currentMeeting.meeting_id || meeting.id;
          const token = api.getToken ? api.getToken() : localStorage.getItem("token");
          
          const res = await fetch(`http://127.0.0.1:9000/api/meeting/${targetId}`, {
            method: "GET",
            headers: {
              "Authorization": `Bearer ${token}`,
              "Content-Type": "application/json"
            }
          });
          
          if (res.ok) {
            const freshData = await res.json();
            setCurrentMeeting(freshData);
          }
        } catch (err) {
          console.error("Failed to sync backend transcript streams:", err);
        } finally {
          setLoadingDetails(false);
        }
      }
    }
    loadFullMeetingPayload();
  }, [meeting.id]);

  // Normalization Layers
  const meetingId = currentMeeting.id || currentMeeting.meeting_id || meeting.id;
  const segments = currentMeeting.segments || currentMeeting.data?.segments || [];
  const rawTranscript = currentMeeting.transcript || currentMeeting.data?.transcript || "";
  
  const summaryObj = currentMeeting.summary || currentMeeting.data?.summary || {};
  const overview = summaryObj.overview || "";
  const keyPoints = summaryObj.key_points || [];

  const actionItems = currentMeeting.action_items || currentMeeting.data?.action_items || [];
  const keyDecisions = currentMeeting.key_decisions || currentMeeting.data?.key_decisions || [];
  const openQuestions = currentMeeting.open_questions || currentMeeting.data?.open_questions || [];

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!chatInput.trim() || isSending) return;
    
    const userMsg = chatInput;
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setChatInput('');
    setIsSending(true);

    try {
      const data = await api.askQuestion(meetingId, userMsg);
      setMessages(prev => [...prev, { role: 'assistant', text: data.answer }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', text: "Error parsing vector space fragments." }]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="flex flex-col lg:flex-row min-h-[calc(100vh-4rem)] bg-[#030712] text-slate-100 antialiased selection:bg-indigo-500/30">
      
      {/* Primary Analytics Workspace */}
      <div className="flex-1 p-6 lg:p-10 space-y-8 lg:max-h-[calc(100vh-4rem)] overflow-y-auto scrollbar-thin">
        
        {/* Navigation Action Bar */}
        <div className="flex items-center justify-between">
          <button 
            onClick={onBack} 
            className="flex items-center gap-2.5 text-xs font-semibold tracking-wide text-slate-400 hover:text-white transition-all duration-200 group uppercase"
          >
            <ArrowLeft className="w-3.5 h-3.5 group-hover:-translate-x-1 transition-transform" /> 
            Back to pipeline matrix
          </button>
          
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-slate-900/60 rounded-full border border-white/[0.06] shadow-[inner_0_1px_0_rgba(255,255,255,0.03)] text-[11px] font-mono tracking-wider text-slate-400">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse" />
            NODE // MAP_{meetingId}
          </div>
        </div>

        {/* Title Block & Structural Metrics */}
        <div className="space-y-2 max-w-4xl">
          <h1 className="text-2xl font-semibold text-white tracking-tight leading-tight">
            {currentMeeting.title}
          </h1>
          <p className="text-sm text-slate-400 font-normal leading-relaxed">
            Automated intelligence indexing completed successfully. Comprehensive analytics generated below.
          </p>
        </div>

        {/* Premium Tab Selector Switch */}
        <div className="flex gap-2 p-1 bg-slate-900/40 rounded-xl border border-white/[0.04] backdrop-blur-md max-w-md shadow-2xl">
          {[
            { id: 'summary', label: 'Summary Maps' },
            { id: 'transcript', label: 'Live Core Transcript' },
            { id: 'action_items', label: 'Action & Metrics' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 py-2 rounded-lg text-xs font-medium tracking-wide transition-all duration-200 ${
                activeTab === tab.id 
                  ? 'bg-gradient-to-b from-white/[0.08] to-white/[0.01] text-white border border-white/[0.08] shadow-[0_4px_12px_rgba(0,0,0,0.5),inner_0_1px_0_rgba(255,255,255,0.1)] backdrop-blur-xl' 
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/[0.02]'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Main Content Render Box */}
        <div className="relative min-h-[460px]">
          {loadingDetails ? (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-[#030712]/50 backdrop-blur-sm rounded-2xl border border-white/[0.04]">
              <Loader2 className="w-6 h-6 animate-spin text-indigo-500" />
              <span className="text-xs font-medium text-slate-400 tracking-widest uppercase font-mono">Syncing system matrices...</span>
            </div>
          ) : (
            <div className="animate-fadeIn space-y-8">
              
              {/* Summary Tab View */}
              {activeTab === 'summary' && (
                <div className="grid grid-cols-1 gap-6">
                  <div className="bg-gradient-to-b from-slate-900/40 to-slate-900/10 border border-white/[0.06] rounded-2xl p-6 shadow-xl">
                    <h3 className="text-sm font-semibold text-white flex items-center gap-2 tracking-wide uppercase border-b border-white/[0.06] pb-3">
                      <Sparkles className="w-4 h-4 text-indigo-400" /> Semantic Core Overview
                    </h3>
                    <p className="text-sm text-slate-300 leading-relaxed font-normal mt-4">
                      {overview || "Analysis summary layer vector not populated."}
                    </p>
                  </div>
                  
                  <div className="bg-gradient-to-b from-slate-900/40 to-slate-900/10 border border-white/[0.06] rounded-2xl p-6 shadow-xl">
                    <h3 className="text-sm font-semibold text-white flex items-center gap-2 tracking-wide uppercase border-b border-white/[0.06] pb-3">
                      <ClipboardList className="w-4 h-4 text-emerald-400" /> Strategic Highlights Matrix
                    </h3>
                    <ul className="mt-4 space-y-3.5 text-sm">
                      {keyPoints.map((pt, i) => (
                        <li key={i} className="flex items-start gap-3 text-slate-300 hover:text-white transition-colors duration-150">
                          <span className="flex-shrink-0 w-1.5 h-1.5 rounded-full bg-indigo-500 mt-2 shadow-[0_0_8px_#6366f1]" />
                          <span className="leading-relaxed font-normal">{pt}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}

              {/* Transcript Tab View */}
              {activeTab === 'transcript' && (
                <div className="bg-gradient-to-b from-slate-900/20 to-transparent border border-white/[0.06] rounded-2xl p-6 max-h-[550px] overflow-y-auto scrollbar-thin space-y-4">
                  {segments.length > 0 ? (
                    segments.map((seg, i) => (
                      <div key={i} className="flex gap-6 p-3.5 rounded-xl border border-transparent hover:border-white/[0.04] hover:bg-white/[0.02] transition-all duration-200 group">
                        <div className="font-mono text-[11px] font-medium text-indigo-400 bg-indigo-500/5 px-2.5 py-1 h-fit rounded-md border border-indigo-500/10 shadow-sm">
                          {seg.start}s - {seg.end}s
                        </div>
                        <p className="text-sm text-slate-300 leading-relaxed font-normal group-hover:text-white transition-colors">
                          {seg.text}
                        </p>
                      </div>
                    ))
                  ) : rawTranscript ? (
                    <div className="space-y-3">
                      <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 border-b border-white/[0.06] pb-2 font-mono">
                        <FileText className="w-4 h-4 text-indigo-400" /> CORE_TEXT_LOGS
                      </div>
                      <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap font-mono p-4 bg-black/40 border border-white/[0.04] rounded-xl">
                        {rawTranscript}
                      </p>
                    </div>
                  ) : (
                    <div className="text-xs text-slate-500 font-mono italic text-center py-16">
                      No computational logging data discovered.
                    </div>
                  )}
                </div>
              )}

              {/* Action Items Tab View */}
              {activeTab === 'action_items' && (
                <div className="space-y-8">
                  <div>
                    <h3 className="text-xs font-bold tracking-widest text-slate-400 flex items-center gap-2 uppercase">
                      <CheckSquare className="w-4 h-4 text-amber-400" /> Action Assignment Metrics
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                      {actionItems.map((item, i) => (
                        <div 
                          key={i} 
                          className="bg-gradient-to-b from-slate-900/60 to-slate-900/20 border border-white/[0.06] p-5 rounded-2xl flex flex-col justify-between shadow-xl transition-all duration-300 hover:-translate-y-0.5 hover:border-white/[0.12] hover:shadow-[0_8px_24px_rgba(0,0,0,0.6)] relative group overflow-hidden"
                        >
                          <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                          <p className="text-sm font-medium text-slate-200 leading-relaxed group-hover:text-white transition-colors">
                            {item.task}
                          </p>
                          <div className="flex flex-wrap items-center gap-3 mt-6 border-t border-white/[0.04] pt-4">
                            <span className="inline-flex items-center gap-1.5 text-xs text-slate-400 font-medium">
                              <User2 className="w-3.5 h-3.5 text-slate-500" /> {item.owner}
                            </span>
                            <span className="inline-flex items-center gap-1.5 text-xs text-slate-400 font-medium">
                              <Calendar className="w-3.5 h-3.5 text-slate-500" /> {item.due_date}
                            </span>
                            <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full border ${
                              item.priority === 'High' 
                                ? 'bg-rose-500/10 text-rose-400 border-rose-500/20 shadow-[0_0_12px_rgba(244,63,94,0.1)]' 
                                : 'bg-slate-800/40 text-slate-400 border-white/[0.06]'
                            }`}>
                              {item.priority}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Decisions & Questions Split Infrastructure */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8 border-t border-white/[0.06] pt-8">
                    {/* Decisions Panel */}
                    <div className="space-y-4">
                      <h3 className="text-xs font-bold tracking-widest text-slate-400 flex items-center gap-2 uppercase">
                        <Bookmark className="w-4 h-4 text-indigo-400" /> Verified System Decisions
                      </h3>
                      <div className="space-y-3 mt-3">
                        {keyDecisions.map((dec, i) => (
                          <div 
                            key={i} 
                            className="flex items-start gap-3 bg-gradient-to-r from-slate-900/50 to-transparent px-4 py-3.5 rounded-xl border border-white/[0.04] shadow-md hover:border-white/[0.08] transition-all duration-200"
                          >
                            <ShieldCheck className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" /> 
                            <span className="text-sm text-slate-300 font-normal leading-relaxed">{dec.decision}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Questions Panel */}
                    <div className="space-y-4">
                      <h3 className="text-xs font-bold tracking-widest text-slate-400 flex items-center gap-2 uppercase">
                        <HelpCircle className="w-4 h-4 text-violet-400" /> Open Engineering Questions
                      </h3>
                      <div className="space-y-3 mt-3">
                        {openQuestions.map((q, i) => (
                          <div 
                            key={i} 
                            className="flex items-start gap-3 bg-gradient-to-r from-slate-900/50 to-transparent px-4 py-3.5 rounded-xl border border-white/[0.04] shadow-md hover:border-white/[0.08] transition-all duration-200"
                          >
                            <HelpCircle className="w-4 h-4 text-violet-400 flex-shrink-0 mt-0.5" /> 
                            <span className="text-sm text-slate-300 font-normal leading-relaxed">{q.question}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                </div>
              )}
            </div> 
          )}
        </div>
      </div>

      {/* RAG Context Chat Panel Sidebar */}
      <div className="w-full lg:w-[400px] bg-gradient-to-b from-[#090d16] to-[#030712] border-t lg:border-t-0 lg:border-l border-white/[0.06] lg:max-h-[calc(100vh-4rem)] flex flex-col shadow-2xl relative z-10">
        
        {/* Sidebar Header */}
        <div className="p-4 border-b border-white/[0.06] bg-slate-950/40 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <MessageSquare className="w-4 h-4 text-indigo-400" />
            <span className="text-xs font-bold text-white uppercase tracking-wider">RAG Retrieval Matrix</span>
          </div>
          <div className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-[10px] font-mono border border-emerald-500/20">
            <Activity className="w-2.5 h-2.5 animate-pulse" /> ENGINE_ACTIVE
          </div>
        </div>
        
        {/* Chat Feed Box Container */}
        <div className="flex-1 p-5 overflow-y-auto space-y-4 max-h-[400px] lg:max-h-none text-xs leading-relaxed scrollbar-thin">
          {messages.map((msg, i) => (
            <div 
              key={i} 
              className={`p-3.5 rounded-2xl max-w-[88%] text-sm shadow-md transition-all ${
                msg.role === 'user' 
                  ? 'bg-indigo-600 text-white ml-auto shadow-indigo-600/5 rounded-tr-none font-normal' 
                  : 'bg-slate-900/60 border border-white/[0.06] text-slate-300 mr-auto rounded-tl-none font-normal leading-relaxed'
              }`}
            >
              {msg.text}
            </div>
          ))}
          {isSending && (
            <div className="p-3.5 rounded-2xl max-w-[88%] bg-slate-900/30 border border-white/[0.04] text-slate-400 mr-auto rounded-tl-none flex items-center gap-2.5 font-mono text-xs">
              <Loader2 className="w-3.5 h-3.5 animate-spin text-indigo-500" /> Parsing indexed graph tensors...
            </div>
          )}
        </div>

        {/* Message Input Container */}
        <form onSubmit={handleSendMessage} className="p-4 border-t border-white/[0.06] bg-slate-950/40 flex gap-2">
          <div className="relative flex-1">
            <input
              type="text"
              disabled={isSending}
              placeholder={isSending ? "Calculating inference..." : "Query localized embedding maps..."}
              className="w-full bg-black/40 border border-white/[0.06] rounded-xl pl-3 pr-10 py-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all shadow-inner disabled:opacity-40"
              value={chatInput}
              onChange={e => setChatInput(e.target.value)}
            />
            <button 
              type="submit" 
              disabled={isSending || !chatInput.trim()}
              className="absolute right-1.5 top-1/2 -translate-y-1/2 p-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-900 text-white disabled:text-slate-600 rounded-lg transition-all duration-200 disabled:cursor-not-allowed"
            >
              <Send className="w-3 h-3" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}