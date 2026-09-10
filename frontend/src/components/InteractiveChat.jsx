import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, Send, Bot, User, Sparkles, Paperclip, FileSpreadsheet, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { sendChatMessage, uploadEcuFile } from '../api';

export default function InteractiveChat({ diagnosticContext }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: 'Hello! I am your Inline-6 Automotive RAG Diagnostic Expert. You can upload an ECU log file directly here or ask me any diagnostic question about torque specs, part numbers, or thermodynamic physics!'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input;
    setInput('');
    setMessages((prev) => [...prev, { id: Date.now(), sender: 'user', text: userText }]);
    setLoading(true);

    try {
      const res = await sendChatMessage(userText, diagnosticContext);
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: 'bot', text: res.reply }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: 'bot', text: 'Error connecting to LLM backend chat service.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUploadInChat = async (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      
      setMessages((prev) => [
        ...prev,
        { id: Date.now(), sender: 'user', text: `Uploaded ECU Log File: ${file.name}` }
      ]);
      setLoading(true);

      try {
        const res = await uploadEcuFile(file);
        const ml = res.ml_prediction;
        const phys = res.physics_summary;
        const hasIssue = ml.has_issue;
        
        const aiResponse = hasIssue
          ? `🔴 **ECU Diagnostic Findings for ${file.name}**:\n\n` +
            `- **Issue Status**: ISSUE DETECTED (${ml.severity} Severity)\n` +
            `- **Fault Classification**: \`${ml.fault_code}\`\n` +
            `- **Isolated Location**: **${ml.isolated_location}**\n` +
            `- **Model Confidence Score**: **${ml.confidence_score}%** (PyTorch PINN: ${ml.pinn_transformer?.pinn_confidence_score || ml.confidence_score}%)\n\n` +
            `**Thermodynamic Summary**: MAF residual error ratio is ${((phys.maf_residual_ratio || 0) * 100).toFixed(1)}%. Cylinder Power Index (CPI) indicates localized power drop on ${ml.isolated_location}.\n\n` +
            `*Ask me for step-by-step physical inspection commands or bolt torque specifications for this component!*`
          : `🟢 **ECU Diagnostic Findings for ${file.name}**:\n\n` +
            `- **Issue Status**: NO ISSUE (System Nominal)\n` +
            `- **Confidence Score**: **${ml.confidence_score}%**\n` +
            `- All 6 cylinders are balanced across the 120° firing order (1-5-3-6-2-4).`;

        setMessages((prev) => [
          ...prev,
          { id: Date.now() + 1, sender: 'bot', text: aiResponse }
        ]);
      } catch (err) {
        setMessages((prev) => [
          ...prev,
          { id: Date.now() + 1, sender: 'bot', text: "Error analyzing attached file: " + (err.response?.data?.detail || err.message) }
        ]);
      } finally {
        setLoading(false);
      }
    }
  };

  const renderMessageText = (text) => {
    const lines = text.split('\n');
    return lines.map((line, idx) => {
      if (line.startsWith('🔴 ') || line.startsWith('🟢 ')) {
        return <div key={idx} className="font-bold text-white mb-2 text-sm">{line}</div>;
      }
      if (line.startsWith('- ')) {
        return <li key={idx} className="ml-4 list-disc text-xs text-gray-200 my-1">{line.replace('- ', '')}</li>;
      }
      if (line.startsWith('*') && line.endsWith('*')) {
        return <div key={idx} className="italic text-cyan-300 text-xs my-1">{line.replace(/\*/g, '')}</div>;
      }
      return <p key={idx} className="text-xs text-gray-200 my-1">{line}</p>;
    });
  };

  return (
    <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-5 shadow-xl flex flex-col h-[75vh] max-w-5xl mx-auto">
      {/* Chat Header */}
      <div className="flex items-center justify-between pb-3 border-b border-[#30363d]">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-cyan-400">
            <Bot className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              Conversational RAG AI Diagnostic Expert
            </h2>
            <p className="text-xs text-gray-400 mt-0.5">
              Upload ECU telemetry files directly in chat or ask follow-up repair questions.
            </p>
          </div>
        </div>

        <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/30">
          Domain LLM Active
        </span>
      </div>

      {/* Messages Scroll View */}
      <div className="flex-1 overflow-y-auto space-y-4 py-4 pr-2 text-xs">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex items-start gap-3 ${m.sender === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <div className={`p-2 rounded-xl text-white shrink-0 shadow ${
              m.sender === 'user'
                ? 'bg-cyan-600'
                : 'bg-[#0d1117] border border-cyan-500/30 text-cyan-400'
            }`}>
              {m.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>
            <div className={`p-4 rounded-2xl max-w-[82%] leading-relaxed shadow-md ${
              m.sender === 'user'
                ? 'bg-cyan-600/25 text-white border border-cyan-500/40 rounded-tr-none'
                : 'bg-[#0d1117] text-gray-200 border border-[#30363d] rounded-tl-none'
            }`}>
              {renderMessageText(m.text)}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-2 text-xs text-cyan-400 italic bg-cyan-500/10 border border-cyan-500/20 p-3 rounded-xl max-w-xs">
            <Sparkles className="w-4 h-4 animate-spin text-cyan-400" />
            <span>AI Expert analyzing telemetry & technical manual...</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Input Form with File Attachment Button */}
      <form onSubmit={handleSend} className="flex items-center gap-2 border-t border-[#30363d] pt-3">
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          title="Upload ECU CSV/Excel file directly in chat"
          className="p-2.5 bg-[#0d1117] hover:bg-[#21262d] border border-[#30363d] hover:border-cyan-400 text-cyan-400 rounded-xl transition-colors shrink-0"
        >
          <Paperclip className="w-4 h-4" />
        </button>

        <input
          type="file"
          ref={fileInputRef}
          accept=".csv,.xlsx,.xls"
          onChange={handleFileUploadInChat}
          className="hidden"
        />

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a diagnostic question or attach an ECU file..."
          className="flex-1 bg-[#0d1117] border border-[#30363d] rounded-xl px-4 py-2.5 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 shadow-inner"
        />

        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-colors shadow"
        >
          <span>Send</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>
    </div>
  );
}
