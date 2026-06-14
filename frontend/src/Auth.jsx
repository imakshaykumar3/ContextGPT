import React, { useState } from 'react';
import { Mail, Lock, User, Bot, Sparkles, ArrowRight, AlertCircle } from 'lucide-react';

export default function Auth({ onAuthSuccess, api }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ name: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isLogin) {
        // 1. Authenticate user credentials and save token to localStorage
        await api.login(formData.email.toLowerCase().trim(), formData.password);
        
        // 2. Fetch the fully validated user record model from /api/auth/me
        const userData = await api.getMe();
        onAuthSuccess(userData);
      } else {
        // 1. Commit new user to the SQLAlchemy database
        await api.register(formData.name.trim(), formData.email.toLowerCase().trim(), formData.password);
        
        // 2. Auto-authenticate immediately following registration
        await api.login(formData.email.toLowerCase().trim(), formData.password);
        const userData = await api.getMe();
        onAuthSuccess(userData);
      }
    } catch (err) {
      // Catch exceptions thrown by API errors (e.g., "Email already registered", "Invalid credentials")
      setError(err.message || 'Authentication lifecycle failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex text-slate-100 font-sans">
      {/* Branding Column */}
      <div className="hidden lg:flex flex-col justify-between w-1/2 p-12 bg-gradient-to-br from-indigo-950 via-slate-950 to-emerald-950 border-r border-slate-800/50 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(99,102,241,0.15),transparent_50%)]" />
        <div className="flex items-center gap-3 relative z-10">
          <div className="p-2.5 bg-indigo-600/10 rounded-xl border border-indigo-500/20 backdrop-blur-md">
            <Bot className="w-4 h-4 text-indigo-400" />
          </div>
          <span className="text-sm font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-slate-400 tracking-tight">
            AI Meeting Assistant
          </span>
        </div>
        
        <div className="space-y-6 relative z-10 max-w-md">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-indigo-500/10 rounded-full border border-indigo-500/20 text-xs font-medium text-indigo-300">
            <Sparkles className="w-3.5 h-3.5" /> Enterprise Intelligence Platform
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight leading-tight text-white">
            Turn raw conversations into execution metrics.
          </h1>
          <p className="text-slate-400 text-sm leading-relaxed">
            Automated transcription, deep semantic summaries, action item tracking, and an interactive RAG interface for your organizational knowledge base.
          </p>
        </div>
        <div className="text-xs text-slate-500 relative z-10">
          &copy; 2026 AI Meeting Assistant Inc. All rights reserved.
        </div>
      </div>

      {/* Form Column */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-12 relative">
        <div className="w-full max-w-md space-y-8">
          <div className="text-center lg:text-left">
            <h2 className="text-3xl font-bold tracking-tight text-white">
              {isLogin ? 'Welcome back' : 'Create an enterprise account'}
            </h2>
            <p className="mt-2 text-sm text-slate-400">
              {isLogin ? 'Access your meeting analytics hub' : 'Get started with centralized intelligence'}
            </p>
          </div>

          {/* Dynamic Server Error Banner */}
          {error && (
            <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl flex items-start gap-3 text-sm text-red-400 animate-fadeIn">
              <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold text-white">Authentication Refused:</span> {error}
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="mt-8 space-y-6">
            <div className="space-y-4">
              {!isLogin && (
                <div>
                  <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Full Name</label>
                  <div className="relative">
                    <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                    <input
                      type="text"
                      required
                      placeholder="Alex Mercer"
                      className="w-full bg-slate-900/50 border border-slate-800 rounded-xl py-3 pl-11 pr-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                      value={formData.name}
                      onChange={e => setFormData({...formData, name: e.target.value})}
                    />
                  </div>
                </div>
              )}

              <div>
                <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Corporate Email</label>
                <div className="relative">
                  <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                  <input
                    type="email"
                    required
                    placeholder="name@company.com"
                    className="w-full bg-slate-900/50 border border-slate-800 rounded-xl py-3 pl-11 pr-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                    value={formData.email}
                    onChange={e => setFormData({...formData, email: e.target.value})}
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Password</label>
                <div className="relative">
                  <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                  <input
                    type="password"
                    required
                    placeholder="••••••••"
                    className="w-full bg-slate-900/50 border border-slate-800 rounded-xl py-3 pl-11 pr-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                    value={formData.password}
                    onChange={e => setFormData({...formData, password: e.target.value})}
                  />
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm py-3.5 rounded-xl shadow-lg shadow-indigo-600/10 flex items-center justify-center gap-2 transition-all transform active:scale-[0.98] disabled:opacity-50"
            >
              {loading ? 'Processing Workspace Token...' : isLogin ? 'Sign In' : 'Register Platform Account'}
              {!loading && <ArrowRight className="w-4 h-4" />}
            </button>
          </form>

          <div className="text-center">
            <button
              onClick={() => {
                setIsLogin(!isLogin);
                setError('');
              }}
              className="text-sm text-indigo-400 hover:text-indigo-300 font-medium transition-colors"
            >
              {isLogin ? "Don't have an account? Sign up" : 'Already registered? Log in'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}