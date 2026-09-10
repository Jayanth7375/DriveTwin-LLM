import React from 'react';
import { Sparkles, BookOpen, Bot, CheckCircle2, ShieldAlert, Wrench, Activity } from 'lucide-react';

export default function LLMReportView({ diagnosticReport }) {
  if (!diagnosticReport) return null;

  const { report_markdown, retrieved_docs } = diagnosticReport;

  // Helper to format inline markdown formatting (**bold**, `code`, clean raw symbols)
  const formatInlineText = (text) => {
    if (!text) return "";
    
    // Clean LaTeX delimiters like ($1-5-3-6-2-4$) -> 1-5-3-6-2-4
    let cleaned = text.replace(/\(\$([^$]+)\$\)/g, '$1').replace(/\$([^$]+)\$/g, '$1');
    
    // Split by ** for bolding
    const parts = cleaned.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);
    
    return parts.map((part, index) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return (
          <strong key={index} className="font-bold text-white">
            {part.slice(2, -2)}
          </strong>
        );
      }
      if (part.startsWith('`') && part.endsWith('`')) {
        return (
          <code key={index} className="font-mono bg-cyan-500/10 text-cyan-300 px-1.5 py-0.5 rounded text-[11px] border border-cyan-500/30">
            {part.slice(1, -1)}
          </code>
        );
      }
      return part;
    });
  };

  // Robust Markdown block renderer
  const renderFormattedReport = (text) => {
    if (!text) return null;

    const lines = text.split('\n');
    const elements = [];

    lines.forEach((line, idx) => {
      const trimmed = line.trim();
      if (!trimmed) return;

      // H2 Headings
      if (trimmed.startsWith('## ')) {
        const titleText = trimmed.replace('## ', '').replace(/^🔴\s*/, '').replace(/^🟢\s*/, '');
        const isRed = trimmed.includes('🔴') || trimmed.includes('CRITICAL');
        elements.push(
          <div key={idx} className={`p-4 rounded-xl border mb-4 flex items-center gap-3 ${
            isRed ? 'bg-red-950/20 border-red-500/40 text-red-300' : 'bg-emerald-950/20 border-emerald-500/40 text-emerald-300'
          }`}>
            {isRed ? <ShieldAlert className="w-6 h-6 shrink-0 text-red-400" /> : <CheckCircle2 className="w-6 h-6 shrink-0 text-emerald-400" />}
            <h2 className="text-base font-bold text-white tracking-wide">
              {titleText}
            </h2>
          </div>
        );
      }
      // H3 & H4 Headings
      else if (trimmed.startsWith('### ') || trimmed.startsWith('#### ')) {
        const hText = trimmed.replace(/^#{3,4}\s*/, '').replace(/^🧪\s*/, '').replace(/^🔍\s*/, '').replace(/^🛠️\s*/, '').replace(/^📊\s*/, '');
        elements.push(
          <h3 key={idx} className="text-sm font-bold text-cyan-300 mt-5 mb-2.5 flex items-center gap-2 border-b border-[#30363d] pb-1.5">
            <Sparkles className="w-4 h-4 text-cyan-400 shrink-0" />
            <span>{hText}</span>
          </h3>
        );
      }
      // Numbered Step Items (e.g. "1. Step Title", "2. **Kinematic Balance**:")
      else if (/^\d+\.\s+/.test(trimmed)) {
        const stepContent = trimmed.replace(/^\d+\.\s+/, '');
        elements.push(
          <div key={idx} className="p-3.5 bg-[#0d1117] border border-[#30363d] rounded-xl my-2.5 text-xs text-gray-200 leading-relaxed shadow-inner">
            {formatInlineText(stepContent)}
          </div>
        );
      }
      // Bullet Points
      else if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
        const bulletText = trimmed.replace(/^[-*]\s+/, '');
        elements.push(
          <div key={idx} className="flex items-start gap-2 text-xs text-gray-300 my-1.5 ml-2 leading-relaxed">
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 shrink-0 mt-1.5" />
            <span>{formatInlineText(bulletText)}</span>
          </div>
        );
      }
      // Divider
      else if (trimmed === '---') {
        elements.push(<hr key={idx} className="border-[#30363d] my-4" />);
      }
      // Normal Paragraphs
      else {
        elements.push(
          <p key={idx} className="text-xs text-gray-300 my-2 leading-relaxed">
            {formatInlineText(trimmed)}
          </p>
        );
      }
    });

    return elements;
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Main Formatted AI Report Container */}
      <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-6 shadow-xl text-gray-200 space-y-2">
        {renderFormattedReport(report_markdown)}
      </div>

      {/* Retrieved OEM Technical Manual References */}
      {retrieved_docs && retrieved_docs.length > 0 && (
        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-5 space-y-3">
          <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center gap-1.5 border-b border-[#30363d] pb-2">
            <BookOpen className="w-4 h-4 text-cyan-400" />
            Retrieved OEM Technical Manual Documentation (Vector DB):
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
            {retrieved_docs.map((doc, idx) => (
              <div key={idx} className="bg-[#0d1117] border border-[#30363d] p-3.5 rounded-xl text-xs space-y-1.5">
                <div className="font-bold text-cyan-300 text-xs flex items-center justify-between">
                  <span>{doc.title}</span>
                  <span className="text-[9px] font-mono bg-cyan-500/10 text-cyan-400 px-2 py-0.5 rounded border border-cyan-500/30">
                    {doc.category}
                  </span>
                </div>
                <p className="text-gray-300 text-[11px] leading-relaxed">{doc.content}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
