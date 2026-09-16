import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, Send, Bot, User, Sparkles, FileSpreadsheet, ShieldAlert, CheckCircle2, Wrench, Activity, BarChart3, AlertTriangle } from 'lucide-react';
import { sendChatMessage, uploadEcuFile } from '../api';

export default function InteractiveChat({ diagnosticContext }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: `### Welcome to the Inline-6 RAG AI Diagnostic Assistant!

I am your domain-trained automotive AI diagnostic expert. Ask me anything about:
- **Fastener & Bolt Torque Specs** (Spark plugs, cylinder head, manifold, fuel rail, clamps)
- **SAE OBD-II Fault Codes** (P0300-P0306 misfires, P0299 boost leak, P0101 MAF drift, P0401 EGR, P0087 HPFP, P0217 head gasket)
- **Diagnostic Procedures** (Compression tests, electrical pinout resistance, component swap tests, smoke leak testing)
- **I6 Kinematic Physics & Equations** (120-degree firing order balance, CPI index, ideal gas volume airflow, stoichiometry)
- **AI Hardware & Execution Stack** (PyTorch CUDA GPU acceleration, Hugging Face LLM, XGBoost ensemble)`
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
      const res = await sendChatMessage(userText, diagnosticContext, messages);
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
          ? `≡ƒö┤ **ECU Diagnostic Findings for ${file.name}**:\n\n` +
            `- **Issue Status**: ISSUE DETECTED (${ml.severity} Severity)\n` +
            `- **Fault Classification**: \`${ml.fault_code}\`\n` +
            `- **Isolated Location**: **${ml.isolated_location}**\n` +
            `- **Model Confidence Score**: **${ml.confidence_score}%** (PyTorch PINN: ${ml.pinn_transformer?.pinn_confidence_score || ml.confidence_score}%)\n\n` +
            `**Thermodynamic Summary**: MAF residual error ratio is ${((phys.maf_residual_ratio || 0) * 100).toFixed(1)}%. Cylinder Power Index (CPI) indicates localized power drop on ${ml.isolated_location}.\n\n` +
            `*Ask me for step-by-step physical inspection commands or bolt torque specifications for this component!*`
          : `≡ƒƒó **ECU Diagnostic Findings for ${file.name}**:\n\n` +
            `- **Issue Status**: NO ISSUE (System Nominal)\n` +
            `- **Confidence Score**: **${ml.confidence_score}%**\n` +
            `- All 6 cylinders are balanced across the 120┬░ firing order (1-5-3-6-2-4).`;

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

  const renderFormattedText = (rawText) => {
    // Process inline bold **text** and code `code`
    const parts = rawText.split(/(\*\*.*?\*\*|`.*?`)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} className="font-bold text-gray-900 dark:text-white">{part.slice(2, -2)}</strong>;
      }
      if (part.startsWith('`') && part.endsWith('`')) {
        return <code key={i} className="bg-gray-100 dark:bg-cyan-950/80 text-cyan-700 dark:text-cyan-300 font-mono text-[11px] px-1.5 py-0.5 rounded border border-cyan-300 dark:border-cyan-500/30">{part.slice(1, -1)}</code>;
      }
      return part;
    });
  };

  const renderMessageText = (text) => {
    const lines = text.split('\n');
    let inTable = false;
    let tableRows = [];

    const rendered = [];

    lines.forEach((line, idx) => {
      const trimmed = line.trim();

      // Check table lines
      if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
        inTable = true;
        if (!trimmed.includes('---')) { // Skip separator row
          const cells = trimmed.split('|').slice(1, -1).map(c => c.trim());
          tableRows.push(cells);
        }
        return;
      } else if (inTable) {
        // Flush table
        inTable = false;
        if (tableRows.length > 0) {
          const header = tableRows[0];
          const rows = tableRows.slice(1);
          rendered.push(
            <div key={`table-${idx}`} className="my-3 overflow-x-auto border border-gray-200 dark:border-[#30363d] rounded-lg">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="bg-gray-100 dark:bg-[#161b22] text-blue-600 dark:text-cyan-600 dark:text-cyan-400 border-b border-gray-200 dark:border-gray-200 dark:border-[#30363d]">
                    {header.map((h, i) => <th key={i} className="p-2 font-semibold">{renderFormattedText(h)}</th>)}
                  </tr>
                </thead>
                <tbody>
                  {rows.map((r, ri) => (
                    <tr key={ri} className="border-b border-gray-200 dark:border-[#30363d]/50 hover:bg-cyan-500/5">
                      {r.map((c, ci) => <td key={ci} className="p-2 text-gray-600 dark:text-gray-300">{renderFormattedText(c)}</td>)}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
          tableRows = [];
        }
      }

      if (trimmed.startsWith('### ')) {
        rendered.push(<h3 key={idx} className="text-sm font-bold text-cyan-600 dark:text-cyan-400 mt-3 mb-1.5 flex items-center gap-1.5">{renderFormattedText(trimmed.replace('### ', ''))}</h3>);
      } else if (trimmed.startsWith('#### ')) {
        rendered.push(<h4 key={idx} className="text-xs font-bold text-gray-900 dark:text-white mt-2.5 mb-1">{renderFormattedText(trimmed.replace('#### ', ''))}</h4>);
      } else if (trimmed.startsWith('## ')) {
        rendered.push(<h2 key={idx} className="text-base font-bold text-cyan-700 dark:text-cyan-300 mt-3 mb-2">{renderFormattedText(trimmed.replace('## ', ''))}</h2>);
      } else if (trimmed.startsWith('≡ƒö┤ ') || trimmed.startsWith('≡ƒƒó ')) {
        rendered.push(<div key={idx} className="font-bold text-gray-900 dark:text-white mb-2 text-sm">{renderFormattedText(trimmed)}</div>);
      } else if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
        rendered.push(<li key={idx} className="ml-4 list-disc text-xs text-gray-700 dark:text-gray-200 my-1">{renderFormattedText(trimmed.substring(2))}</li>);
      } else if (/^\d+\.\s/.test(trimmed)) {
        rendered.push(<div key={idx} className="ml-2 font-medium text-xs text-cyan-800 dark:text-cyan-200 my-1">{renderFormattedText(trimmed)}</div>);
      } else if (trimmed.startsWith('*') && trimmed.endsWith('*')) {
        rendered.push(<div key={idx} className="italic text-cyan-700 dark:text-cyan-300 text-xs my-1 bg-cyan-50 dark:bg-cyan-500/10 p-2 rounded-lg border border-cyan-200 dark:border-cyan-500/20">{renderFormattedText(trimmed.replace(/\*/g, ''))}</div>);
      } else if (trimmed === '---') {
        rendered.push(<hr key={idx} className="border-gray-200 dark:border-[#30363d] my-3" />);
      } else if (trimmed.length > 0) {
        rendered.push(<p key={idx} className="text-xs text-gray-700 dark:text-gray-200 my-1.5 leading-relaxed">{renderFormattedText(trimmed)}</p>);
      }
    });

    if (inTable && tableRows.length > 0) {
      const header = tableRows[0];
      const rows = tableRows.slice(1);
      rendered.push(
        <div key="table-end" className="my-3 overflow-x-auto border border-gray-200 dark:border-[#30363d] rounded-lg">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-gray-100 dark:bg-[#161b22] text-blue-600 dark:text-cyan-600 dark:text-cyan-400 border-b border-gray-200 dark:border-gray-200 dark:border-[#30363d]">
                {header.map((h, i) => <th key={i} className="p-2 font-semibold">{renderFormattedText(h)}</th>)}
              </tr>
            </thead>
            <tbody>
              {rows.map((r, ri) => (
                <tr key={ri} className="border-b border-gray-200 dark:border-[#30363d]/50 hover:bg-cyan-500/5">
                  {r.map((c, ci) => <td key={ci} className="p-2 text-gray-600 dark:text-gray-300">{renderFormattedText(c)}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }

    return rendered;
  };

  return (
    <div className="bg-white/60 dark:bg-[#161b22]/60 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-3xl p-6 shadow-2xl shadow-black/5 dark:shadow-black/40 ring-1 ring-black/5 dark:ring-white/5 transition-all duration-300 flex flex-col h-[85vh] w-full">
      {/* Chat Header */}
      <div className="flex items-center justify-between pb-3 border-b border-gray-200 dark:border-[#30363d]">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-cyan-50 dark:bg-cyan-500/10 border border-cyan-300 dark:border-cyan-500/30 rounded-2xl text-cyan-600 dark:text-cyan-400">
            <Bot className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-gray-900 dark:text-white flex items-center gap-2">
              Conversational RAG AI Diagnostic Expert
            </h2>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
              Powered by RAG OEM Knowledge Base & Active ECU Physics Analytics
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
            <div className={`p-2 rounded-2xl text-gray-900 dark:text-white shrink-0 shadow ${
              m.sender === 'user'
                ? 'bg-cyan-600'
                : 'bg-[#0d1117] border border-cyan-300 dark:border-cyan-500/30 text-cyan-600 dark:text-cyan-400'
            }`}>
              {m.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>
            <div className={`p-4 rounded-2xl max-w-[95%] leading-relaxed shadow-md ${
              m.sender === 'user'
                ? 'bg-cyan-600/25 text-gray-900 dark:text-white border border-cyan-500/40 rounded-tr-none'
                : 'bg-gray-50 dark:bg-[#0d1117] text-gray-800 dark:text-gray-200 border border-gray-200 dark:border-[#30363d] rounded-tl-none'
            }`}>
              {renderMessageText(m.text)}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-2 text-xs text-cyan-600 dark:text-cyan-400 italic bg-cyan-50 dark:bg-cyan-500/10 border border-cyan-200 dark:border-cyan-500/20 p-3 rounded-2xl max-w-xs">
            <Sparkles className="w-4 h-4 animate-spin text-cyan-600 dark:text-cyan-400" />
            <span>AI Expert querying RAG vector store & manual database...</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Input Form with File Attachment Button */}
      <form onSubmit={handleSend} className="flex items-center gap-2 pt-2">
        

        

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a diagnostic question, torque spec, or attach an ECU file..."
          className="flex-1 bg-white dark:bg-[#0d1117] border border-gray-200 dark:border-gray-200 dark:border-[#30363d] rounded-2xl px-4 py-2.5 text-xs text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400 shadow-inner"
        />

        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white px-4 py-2.5 rounded-2xl text-xs font-bold flex items-center gap-1.5 transition-colors shadow"
        >
          <Send className="w-3.5 h-3.5" />
          <span>Send</span>
        </button>
      </form>
      
      {/* Quick Prompt Suggestions (Bottom Aligned Pills) */}
      <div className="flex items-center justify-center gap-3 pt-4 pb-1 overflow-x-auto text-[11px] no-scrollbar">
        <button
          type="button"
          onClick={() => setInput("What are the exact torque specs for spark plugs and cylinder head bolts?")}
          className="bg-transparent hover:bg-gray-100 dark:hover:bg-[#21262d] text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-[#30363d] px-3.5 py-1.5 rounded-full shrink-0 transition-colors flex items-center gap-2"
        >
          <Wrench className="w-3.5 h-3.5 text-gray-500" /> Torque Specs
        </button>
        <button
          type="button"
          onClick={() => setInput("How do I perform a compression test and component swap test for cylinder 3 misfire?")}
          className="bg-transparent hover:bg-gray-100 dark:hover:bg-[#21262d] text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-[#30363d] px-3.5 py-1.5 rounded-full shrink-0 transition-colors flex items-center gap-2"
        >
          <Activity className="w-3.5 h-3.5 text-gray-500" /> Cylinder 3 Repair
        </button>
        <button
          type="button"
          onClick={() => setInput("Explain the 120 degree firing order and Cylinder Power Index (CPI) formula.")}
          className="bg-transparent hover:bg-gray-100 dark:hover:bg-[#21262d] text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-[#30363d] px-3.5 py-1.5 rounded-full shrink-0 transition-colors flex items-center gap-2"
        >
          <BarChart3 className="w-3.5 h-3.5 text-gray-500" /> I6 Physics & Firing Order
        </button>
        <button
          type="button"
          onClick={() => setInput("What causes P0299 boost leak and P0101 MAF drift?")}
          className="bg-transparent hover:bg-gray-100 dark:hover:bg-[#21262d] text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-[#30363d] px-3.5 py-1.5 rounded-full shrink-0 transition-colors flex items-center gap-2"
        >
          <AlertTriangle className="w-3.5 h-3.5 text-gray-500" /> P0299 & P0101 Faults
        </button>
      </div>
    </div>
  );
}
