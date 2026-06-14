import React, { useState } from 'react';
import { UploadCloud, Link2, FileVideo, Clock, Globe, ArrowUpRight, Plus, HelpCircle, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function Dashboard({ user, meetings, onSelectMeeting, onCreateMeeting }) {
  const [url, setUrl] = useState('');
  const [isDragging, setIsDragging] = useState(false);

  const handleUrlSubmit = (e) => {
    e.preventDefault();
    if (!url) return;
    onCreateMeeting({ type: 'url', source: url });
    setUrl('');
  };

  const handleFileDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files.length) {
      // FIX: Passing the actual binary File object down to the API layer
      onCreateMeeting({ type: 'file', source: e.dataTransfer.files[0] });
    }
  };

  return (
    <div className="space-y-10 max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
      {/* Header Panel */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-900/40 p-6 rounded-2xl border border-slate-800/60 backdrop-blur-md">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Welcome, {user.name}</h1>
          <p className="text-sm text-slate-400 mt-1">Deploy automated models against pipelines to generate analytics maps.</p>
        </div>
        <div className="flex gap-3 text-xs font-semibold text-slate-400">
          <div className="bg-slate-900 px-4 py-2 rounded-xl border border-slate-800">
            Total Computes: <span className="text-white ml-1">{meetings.length}</span>
          </div>
        </div>
      </div>

      {/* Upload Matrix Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* File Dropzone */}
        <div
          onDragOver={e => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleFileDrop}
          className={`group border-2 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center text-center transition-all cursor-pointer relative ${
            isDragging ? 'border-indigo-500 bg-indigo-500/5' : 'border-slate-800 bg-slate-900/20 hover:border-slate-700 hover:bg-slate-900/40'
          }`}
        >
          <div className="p-4 bg-slate-900 rounded-2xl border border-slate-800 mb-4 group-hover:scale-105 transition-transform">
            <UploadCloud className="w-8 h-8 text-indigo-400" />
          </div>
          <h3 className="text-base font-semibold text-white">Upload Local Meeting Data</h3>
          <p className="text-xs text-slate-400 mt-2 max-w-xs leading-relaxed">
            Drag and drop audio or video extensions here. Supports <span className="text-slate-300 font-mono">.mp3, .wav, .mp4, .m4a</span> up to 60MB.
          </p>
          {/* FIX: Passing the actual binary File object here on change event */}
          <input 
            type="file" 
            accept=".mp3,.wav,.mp4,.m4a"
            className="absolute inset-0 opacity-0 cursor-pointer" 
            onChange={e => e.target.files.length && onCreateMeeting({ type: 'file', source: e.target.files[0] })} 
          />
        </div>

        {/* URL Ingestion Engine */}
        <div className="bg-slate-900/30 border border-slate-800/80 rounded-2xl p-8 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2.5 bg-slate-900 rounded-xl border border-slate-800">
                <Link2 className="w-5 h-5 text-emerald-400" />
              </div>
              <div>
                <h3 className="text-base font-semibold text-white">Ingest Public Stream URL</h3>
                <p className="text-xs text-slate-400 mt-0.5">Process YouTube index feeds asynchronously</p>
              </div>
            </div>
            <form onSubmit={handleUrlSubmit} className="mt-6 relative">
              <input
                type="url"
                placeholder="https://www.youtube.com/watch?v=..."
                className="w-full bg-slate-950 border border-slate-800 rounded-xl py-3.5 pl-4 pr-32 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                value={url}
                onChange={e => setUrl(e.target.value)}
              />
              <button
                type="submit"
                className="absolute right-2 top-1/2 -translate-y-1/2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs px-4 py-2 rounded-lg transition-colors flex items-center gap-1.5"
              >
                Inference <Plus className="w-3.5 h-3.5" />
              </button>
            </form>
          </div>
          <div className="flex items-center gap-2 mt-4 text-xs text-slate-500 bg-slate-900/40 p-3 rounded-xl border border-slate-800/40">
            <AlertCircle className="w-4 h-4 flex-shrink-0 text-slate-400" />
            <span>URLs are automatically parsed and downsampled into single-channel WAV vectors.</span>
          </div>
        </div>
      </div>

      {/* History Infrastructure */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-white tracking-tight">Recent Computational Pipelines</h2>
        <div className="bg-slate-900/20 border border-slate-800 rounded-2xl overflow-hidden backdrop-blur-md">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 bg-slate-900/40 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  <th className="p-4 pl-6">Meeting Manifest</th>
                  <th className="p-4">Platform Pipeline Status</th>
                  <th className="p-4">Language Matrix</th>
                  <th className="p-4 text-right pr-6">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50 text-sm">
                {meetings.map((meeting) => (
                  <tr key={meeting.id} className="hover:bg-slate-900/30 transition-colors group">
                    <td className="p-4 pl-6">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-slate-900 rounded-lg border border-slate-800 text-slate-400">
                          <FileVideo className="w-4 h-4" />
                        </div>
                        <div>
                          <div className="font-semibold text-slate-200 group-hover:text-white transition-colors">{meeting.title}</div>
                          <div className="flex items-center gap-1 text-xs text-slate-500 mt-1">
                            <Clock className="w-3 h-3" /> {meeting.date}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="p-4">
                      {meeting.status === 'completed' && (
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-400 text-xs font-medium border border-emerald-500/10">
                          <CheckCircle2 className="w-3.5 h-3.5" /> Completed
                        </span>
                      )}
                      {meeting.status === 'processing' && (
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-indigo-500/10 text-indigo-400 text-xs font-medium border border-indigo-500/10 animate-pulse">
                          <HelpCircle className="w-3.5 h-3.5" /> Transcribing
                        </span>
                      )}
                    </td>
                    <td className="p-4 text-slate-400">
                      <span className="inline-flex items-center gap-1 font-mono text-xs uppercase bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                        <Globe className="w-3 h-3" /> {meeting.language}
                      </span>
                    </td>
                    <td className="p-4 text-right pr-6">
                      <button
                        onClick={() => onSelectMeeting(meeting)}
                        disabled={meeting.status === 'processing'}
                        className="p-1.5 bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg border border-slate-800 transition-colors inline-flex items-center gap-1 text-xs font-medium disabled:opacity-40 disabled:cursor-not-allowed"
                      >
                        Analyze <ArrowUpRight className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}