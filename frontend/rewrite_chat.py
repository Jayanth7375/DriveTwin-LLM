import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"

react_code = """import React, { useState, useRef, useEffect } from 'react';
import { 
  MessageSquare, Send, Bot, User, Sparkles, Paperclip, FileSpreadsheet, ShieldAlert, 
  CheckCircle2, Wrench, FileText, Activity, Box, ChevronRight, UploadCloud, PlayCircle,
  Zap, BookOpen, BarChart3, AlertTriangle
} from 'lucide-react';
import { sendChatMessage, uploadEcuFile } from '../api';

export default function InteractiveChat({ diagnosticContext }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e, customText = null) => {
    if (e) e.preventDefault();
    const userText = customText || input;
    if (!userText.trim() || loading) return;

    setInput('');
    setMessages((prev) => [...prev, { id: Date.now(), sender: 'user', text: userText }]);
    setLoading(true);

    try {
      const res = await sendChatMessage(userText, diagnosticContext, messages);
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: 'bot', text: res.response || "No response received." }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: 'bot', text: "Error communicating with the diagnostic AI. Please check the backend connection." }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setMessages((prev) => [
      ...prev,
      { id: Date.now(), sender: 'user', text: `Uploaded diagnostic log: ${file.name}` },
      { id: Date.now() + 1, sender: 'bot', text: "Analyzing ECU log file... Please wait." }
    ]);
    setLoading(true);

    try {
      const res = await uploadEcuFile(file);
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 2, sender: 'bot', text: `Log analyzed successfully! Fault detected: **${res.fault_code}**.\n\nConfidence: ${(res.confidence * 100).toFixed(1)}%\n\nI have updated the diagnostic context. What would you like to know about this issue?` }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 2, sender: 'bot', text: "Failed to parse the ECU log. Make sure it's a valid CSV." }
      ]);
    } finally {
      setLoading(false);
      e.target.value = null; // reset
    }
  };

  const hasStarted = messages.length > 0;

  // Render Markdown safely (simple bold parser for mockup)
  const renderText = (txt) => {
    return txt.split('\\n').map((line, i) => (
      <span key={i}>
        {line.split(/(\*\*.*?\*\*)/).map((part, j) => {
          if (part.startsWith('**') && part.endsWith('**')) {
            return <strong key={j} className="text-gray-900 dark:text-white">{part.slice(2, -2)}</strong>;
          }
          return part;
        })}
        <br />
      </span>
    ));
  };

  return (
    <div className="h-full min-h-[85vh] flex flex-col">
      {!hasStarted ? (
        // HERO UI (Empty State)
        <div className="flex-1 flex flex-col xl:flex-row gap-6 animate-in fade-in duration-500">
          {/* Main Left Content */}
          <div className="flex-1 flex flex-col relative bg-gradient-to-br from-[#e0eaf5]/50 to-white dark:from-[#0d1117] dark:to-[#161b22] rounded-3xl border border-blue-100 dark:border-white/5 overflow-hidden shadow-xl p-8">
            
            {/* Top Engine & Text Area */}
            <div className="flex-1 flex flex-col lg:flex-row gap-8 relative z-10 mb-8">
              
              {/* Engine Graphic with Pointers */}
              <div className="flex-1 relative min-h-[300px] flex items-center justify-center">
                {/* Glow */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-cyan-400/20 dark:bg-cyan-500/10 rounded-full blur-[100px]"></div>
                
                <img 
                  src="/engine-render.jpg" 
                  alt="3D Engine" 
                  className="relative z-10 max-w-[120%] lg:max-w-[140%] object-contain scale-110 mix-blend-multiply dark:invert-0 invert dark:mix-blend-screen opacity-90"
                  style={{
                    WebkitMaskImage: 'radial-gradient(circle at center, black 40%, transparent 70%)',
                    maskImage: 'radial-gradient(circle at center, black 40%, transparent 70%)'
                  }}
                />

                {/* Floating Tags */}
                <div className="absolute top-[20%] left-[10%] bg-white/90 dark:bg-[#161b22]/90 backdrop-blur border border-emerald-500/30 rounded-xl p-2 shadow-lg z-20 flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 flex items-center justify-center"><Wrench className="w-4 h-4" /></div>
                  <div>
                    <p className="text-[11px] font-bold text-gray-900 dark:text-white leading-tight">Injectors</p>
                    <p className="text-[9px] text-emerald-600 dark:text-emerald-400">Working Normal</p>
                  </div>
                </div>

                <div className="absolute top-[15%] right-[10%] bg-white/90 dark:bg-[#161b22]/90 backdrop-blur border border-amber-500/30 rounded-xl p-2 shadow-lg z-20 flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-amber-100 dark:bg-amber-500/20 text-amber-600 flex items-center justify-center"><AlertTriangle className="w-4 h-4" /></div>
                  <div>
                    <p className="text-[11px] font-bold text-gray-900 dark:text-white leading-tight">Fuel Rail</p>
                    <p className="text-[9px] text-amber-600 dark:text-amber-400">Check Pressure</p>
                  </div>
                </div>

                <div className="absolute bottom-[20%] left-[5%] bg-white/90 dark:bg-[#161b22]/90 backdrop-blur border border-blue-500/30 rounded-xl p-2 shadow-lg z-20 flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-500/20 text-blue-600 flex items-center justify-center"><Settings className="w-4 h-4" /></div>
                  <div>
                    <p className="text-[11px] font-bold text-gray-900 dark:text-white leading-tight">Turbocharger</p>
                    <p className="text-[9px] text-emerald-600 dark:text-emerald-400">Optimal</p>
                  </div>
                </div>

              </div>

              {/* Text Area */}
              <div className="flex-1 flex flex-col justify-center">
                <h1 className="text-4xl lg:text-5xl font-black text-blue-500 dark:text-blue-400 leading-tight tracking-tight mb-2">
                  Ask. <span className="text-gray-900 dark:text-white">Diagnose.</span><br/>
                  <span className="text-blue-500 dark:text-blue-400">Repair.</span> <span className="text-gray-900 dark:text-white">Learn.</span>
                </h1>
                <p className="text-gray-600 dark:text-gray-400 text-lg mb-8 max-w-sm">
                  Your AI-powered mechanic for Inline-6 diesel engines.
                </p>

                <div className="flex gap-6">
                  <div className="flex flex-col items-center gap-2 text-center">
                    <Zap className="w-6 h-6 text-blue-500" />
                    <span className="text-[10px] font-bold text-gray-500">Instant<br/>Answers</span>
                  </div>
                  <div className="flex flex-col items-center gap-2 text-center">
                    <BookOpen className="w-6 h-6 text-blue-500" />
                    <span className="text-[10px] font-bold text-gray-500">OEM<br/>Knowledge</span>
                  </div>
                  <div className="flex flex-col items-center gap-2 text-center">
                    <BarChart3 className="w-6 h-6 text-blue-500" />
                    <span className="text-[10px] font-bold text-gray-500">Physics<br/>Insights</span>
                  </div>
                  <div className="flex flex-col items-center gap-2 text-center">
                    <Wrench className="w-6 h-6 text-blue-500" />
                    <span className="text-[10px] font-bold text-gray-500">Step-by-Step<br/>Repair</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Bottom Prompt Area */}
            <div className="relative z-10 mt-auto bg-white/60 dark:bg-white/5 backdrop-blur-xl border border-white/50 dark:border-white/10 p-6 rounded-2xl shadow-xl">
              
              <div className="flex items-center gap-4 mb-6">
                <div className="w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-500/20 flex items-center justify-center">
                  <Bot className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="bg-white dark:bg-[#161b22] px-4 py-2 rounded-2xl rounded-tl-sm shadow-sm border border-gray-100 dark:border-white/10">
                  <p className="text-sm font-bold text-gray-900 dark:text-white">Hi! I'm DriveTwin AI 👋</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">What would you like to diagnose today?</p>
                </div>
              </div>

              {/* Suggestion Cards */}
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                {[
                  { icon: <Wrench className="w-5 h-5 text-red-500" />, title: "Diagnose\na Fault", prompt: "Help me diagnose a fault on my engine." },
                  { icon: <FileText className="w-5 h-5 text-blue-500" />, title: "Explain\na Code", prompt: "Explain how OBD-II fault codes are generated." },
                  { icon: <Activity className="w-5 h-5 text-indigo-500" />, title: "Analyze\nSensor Data", prompt: "Analyze the current sensor data in the context." },
                  { icon: <Box className="w-5 h-5 text-cyan-500" />, title: "Show in\n3D Model", prompt: "Where is the EGR valve located?" }
                ].map((card, i) => (
                  <button 
                    key={i}
                    onClick={() => handleSend(null, card.prompt)}
                    className="flex items-center justify-between p-4 bg-white dark:bg-[#161b22] border border-gray-100 dark:border-white/5 rounded-2xl hover:border-blue-400 dark:hover:border-blue-500/50 hover:shadow-lg transition-all text-left group"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-gray-50 dark:bg-white/5 flex items-center justify-center group-hover:scale-110 transition-transform">
                        {card.icon}
                      </div>
                      <span className="text-xs font-bold text-gray-700 dark:text-gray-300 whitespace-pre-line leading-tight">{card.title}</span>
                    </div>
                    <ChevronRight className="w-4 h-4 text-gray-300 group-hover:text-blue-500" />
                  </button>
                ))}
              </div>

              {/* Input Bar */}
              <form onSubmit={handleSend} className="relative flex items-center bg-white dark:bg-[#161b22] border border-gray-200 dark:border-white/10 rounded-full p-1.5 shadow-sm focus-within:ring-2 focus-within:ring-blue-500/50 focus-within:border-blue-500">
                <button type="button" className="p-3 text-gray-400 hover:text-blue-500 transition-colors" onClick={() => fileInputRef.current?.click()}>
                  <Paperclip className="w-5 h-5" />
                </button>
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask a question, upload a log file, or speak..."
                  className="flex-1 bg-transparent border-none outline-none text-gray-900 dark:text-white px-2 placeholder-gray-400 text-sm"
                />
                <button type="button" className="p-3 text-gray-400 hover:text-blue-500 transition-colors">
                  <div className="w-5 h-5 border-[1.5px] border-current rounded-full flex flex-col items-center justify-center gap-0.5"><div className="w-1 h-1.5 bg-current rounded-full"></div><div className="w-2 h-0.5 bg-current rounded-sm"></div></div>
                </button>
                <button type="submit" disabled={!input.trim() || loading} className="ml-2 bg-blue-500 hover:bg-blue-600 disabled:opacity-50 text-white p-3 rounded-full transition-colors">
                  <Send className="w-4 h-4" />
                </button>
              </form>
              <input type="file" ref={fileInputRef} className="hidden" accept=".csv" onChange={handleFileUpload} />
              
              <div className="flex justify-center gap-4 mt-4 text-[10px] text-gray-400">
                <span>e.g. "Why is P0299 set?"</span>
                <span>"Torque specs for head bolts"</span>
                <span>"Show EGR in 3D"</span>
                <span>"Analyze my log file"</span>
              </div>
            </div>
          </div>

          {/* Right Sidebar Area */}
          <div className="w-full xl:w-80 flex flex-col gap-6">
            
            <div className="bg-white/60 dark:bg-[#161b22]/60 backdrop-blur-xl border border-gray-200/50 dark:border-white/5 rounded-3xl p-5 shadow-lg">
              <div className="flex items-center gap-2 mb-4 text-sm font-bold text-gray-900 dark:text-white">
                <Sparkles className="w-4 h-4 text-amber-500" /> Suggested for You
              </div>
              <div className="space-y-2">
                {[
                  { icon: <AlertTriangle className="text-red-500"/>, bg: 'bg-red-50 dark:bg-red-500/10', title: 'P0299', sub: 'Turbo Underboost' },
                  { icon: <Settings className="text-emerald-500"/>, bg: 'bg-emerald-50 dark:bg-emerald-500/10', title: 'Cylinder 3', sub: 'Compression Check' },
                  { icon: <Wrench className="text-purple-500"/>, bg: 'bg-purple-50 dark:bg-purple-500/10', title: 'Torque Specs', sub: 'Head Bolts (Inline-6)' },
                  { icon: <BookOpen className="text-blue-500"/>, bg: 'bg-blue-50 dark:bg-blue-500/10', title: 'SAE OBD-II Codes', sub: 'Quick Reference' }
                ].map((item, i) => (
                  <button key={i} onClick={() => handleSend(null, `Tell me about ${item.title}: ${item.sub}`)} className="w-full flex items-center justify-between p-3 bg-white dark:bg-[#0d1117] border border-gray-100 dark:border-white/5 rounded-2xl hover:border-blue-400 transition-colors group text-left">
                    <div className="flex items-center gap-3">
                      <div className={`w-10 h-10 rounded-full ${item.bg} flex items-center justify-center [&>svg]:w-5 [&>svg]:h-5`}>
                        {item.icon}
                      </div>
                      <div>
                        <p className="text-sm font-bold text-gray-900 dark:text-white">{item.title}</p>
                        <p className="text-[10px] text-gray-500">{item.sub}</p>
                      </div>
                    </div>
                    <ChevronRight className="w-4 h-4 text-gray-300 group-hover:text-blue-500" />
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-white/60 dark:bg-[#161b22]/60 backdrop-blur-xl border border-gray-200/50 dark:border-white/5 rounded-3xl p-5 shadow-lg">
              <div className="flex items-center gap-2 mb-4 text-sm font-bold text-gray-900 dark:text-white">
                <UploadCloud className="w-4 h-4 text-blue-500" /> Upload & Analyze
              </div>
              <div onClick={() => fileInputRef.current?.click()} className="border-2 border-dashed border-gray-300 dark:border-white/20 rounded-2xl p-6 flex flex-col items-center justify-center text-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-500/10 transition-colors">
                <FileSpreadsheet className="w-8 h-8 text-gray-400 mb-2" />
                <p className="text-[11px] text-gray-500 mb-3">Drag & drop ECU log file<br/>(.csv, .log, .txt, .ecu)</p>
                <button className="px-4 py-2 bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400 text-xs font-bold rounded-lg">Choose File</button>
              </div>
            </div>

            <div className="bg-white/60 dark:bg-[#161b22]/60 backdrop-blur-xl border border-gray-200/50 dark:border-white/5 rounded-3xl p-5 shadow-lg">
              <div className="flex items-center gap-2 mb-4 text-sm font-bold text-gray-900 dark:text-white">
                <Box className="w-4 h-4 text-blue-500" /> Explore the Engine
              </div>
              <div className="relative rounded-2xl overflow-hidden border border-gray-200 dark:border-white/10 group cursor-pointer">
                <img src="/engine-render.jpg" className="w-full h-32 object-cover object-center dark:mix-blend-screen opacity-80 group-hover:opacity-100 transition-opacity" />
                <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
                  <PlayCircle className="w-10 h-10 text-white/80 group-hover:scale-110 transition-transform" />
                </div>
              </div>
              <div className="flex items-center justify-between mt-3 text-xs text-gray-500">
                <span>Interactive 3D Engine Twin</span>
                <ChevronRight className="w-3 h-3" />
              </div>
            </div>

          </div>
        </div>
      ) : (
        // ACTIVE CHAT UI
        <div className="flex-1 flex flex-col bg-white/80 dark:bg-[#161b22]/80 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-3xl shadow-xl overflow-hidden animate-in slide-in-from-bottom-4 duration-300">
          
          <div className="bg-white dark:bg-[#0d1117] border-b border-gray-100 dark:border-white/5 p-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-500/20 flex items-center justify-center">
                <Bot className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-gray-900 dark:text-white">Conversational RAG AI Diagnostic Expert</h3>
                <p className="text-[10px] text-gray-500">Powered by RAG OEM Knowledge Base & Active ECU Physics</p>
              </div>
            </div>
            <div className="px-3 py-1 bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs font-mono font-bold rounded-full">
              Domain LLM Active
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] lg:max-w-[75%] rounded-2xl p-4 shadow-sm ${
                  msg.sender === 'user' 
                    ? 'bg-blue-500 text-white rounded-br-sm' 
                    : 'bg-gray-50 dark:bg-[#0d1117] text-gray-800 dark:text-gray-300 border border-gray-200/50 dark:border-white/5 rounded-bl-sm'
                }`}>
                  <div className="flex items-center gap-2 mb-2 opacity-80 text-xs font-bold">
                    {msg.sender === 'user' ? <User className="w-4 h-4" /> : <Sparkles className="w-4 h-4 text-amber-500" />}
                    <span>{msg.sender === 'user' ? 'You' : 'DriveTwin AI'}</span>
                  </div>
                  <div className="text-sm leading-relaxed whitespace-pre-wrap">
                    {renderText(msg.text)}
                  </div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-50 dark:bg-[#0d1117] border border-gray-200/50 dark:border-white/5 rounded-2xl rounded-bl-sm p-4 flex items-center gap-3">
                  <Sparkles className="w-4 h-4 text-amber-500 animate-pulse" />
                  <span className="text-sm text-gray-500">Analyzing context & querying knowledge base...</span>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <div className="p-4 bg-gray-50 dark:bg-[#0d1117] border-t border-gray-100 dark:border-white/5">
            <form onSubmit={handleSend} className="max-w-4xl mx-auto flex items-end gap-3">
              <button 
                type="button" 
                onClick={() => fileInputRef.current?.click()}
                className="p-3.5 bg-white dark:bg-[#161b22] border border-gray-200 dark:border-white/10 rounded-2xl hover:border-blue-500 hover:text-blue-500 text-gray-400 transition-colors shadow-sm"
              >
                <Paperclip className="w-5 h-5" />
              </button>
              <div className="flex-1 bg-white dark:bg-[#161b22] border border-gray-200 dark:border-white/10 rounded-2xl shadow-sm focus-within:ring-2 focus-within:ring-blue-500/50 focus-within:border-blue-500 flex items-end">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) handleSend(e); }}
                  placeholder="Ask a diagnostic question or attach an ECU file..."
                  className="flex-1 max-h-32 min-h-[52px] bg-transparent border-none outline-none text-gray-900 dark:text-white p-4 resize-none placeholder-gray-400 text-sm"
                  rows="1"
                />
              </div>
              <button 
                type="submit" 
                disabled={!input.trim() || loading}
                className="p-3.5 bg-blue-500 hover:bg-blue-600 disabled:opacity-50 text-white rounded-2xl shadow-md shadow-blue-500/20 transition-colors flex items-center justify-center"
              >
                <Send className="w-5 h-5" />
              </button>
            </form>
            <input type="file" ref={fileInputRef} className="hidden" accept=".csv" onChange={handleFileUpload} />
          </div>
        </div>
      )}
    </div>
  );
}
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(react_code)

