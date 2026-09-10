import React, { useState, useEffect } from 'react';
import { Database, FolderCheck, FileText, Search, Download, CheckCircle2, RefreshCw } from 'lucide-react';
import { fetchDatasetFiles } from '../api';

export default function DatasetManagerPage({ onSelectDatasetFile, isLoading }) {
  const [datasetInfo, setDatasetInfo] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFolder, setSelectedFolder] = useState('ALL');

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    try {
      const info = await fetchDatasetFiles();
      setDatasetInfo(info);
    } catch (err) {
      console.error("Dataset load error:", err);
    }
  };

  const categories = datasetInfo?.categories ? Object.keys(datasetInfo.categories) : [];

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-[#161b22] border border-[#30363d] p-5 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Database className="w-5 h-5 text-cyan-400" />
            5.0 GB Diesel ECU Telemetry Dataset Workspace
          </h2>
          <p className="text-xs text-gray-400 mt-1">
            Explore 4,000 multi-channel CSV log files (40 Million telemetry records) generated across 8 Diesel fault categories.
          </p>
        </div>

        <div className="flex items-center gap-3 font-mono text-xs">
          <div className="bg-[#0d1117] border border-[#30363d] px-3.5 py-1.5 rounded-lg text-emerald-400">
            Total Files: <span className="font-bold text-white">{datasetInfo?.total_count || 4000}</span>
          </div>
          <div className="bg-[#0d1117] border border-[#30363d] px-3.5 py-1.5 rounded-lg text-cyan-400">
            Total Volume: <span className="font-bold text-white">5.08 GB</span>
          </div>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-[#161b22] border border-[#30363d] p-4 rounded-xl flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Category Filters */}
        <div className="flex items-center gap-2 overflow-x-auto w-full sm:w-auto pb-2 sm:pb-0 no-scrollbar">
          <button
            onClick={() => setSelectedFolder('ALL')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
              selectedFolder === 'ALL'
                ? 'bg-cyan-600 text-white'
                : 'bg-[#0d1117] text-gray-400 hover:text-white border border-[#30363d]'
            }`}
          >
            All Subfolders ({categories.length})
          </button>
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedFolder(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
                selectedFolder === cat
                  ? 'bg-cyan-600 text-white'
                  : 'bg-[#0d1117] text-gray-400 hover:text-white border border-[#30363d]'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Search Input */}
        <div className="relative w-full sm:w-64">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-2.5" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search log files..."
            className="w-full bg-[#0d1117] border border-[#30363d] rounded-lg pl-9 pr-3 py-1.5 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400"
          />
        </div>
      </div>

      {/* Categories File Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {categories
          .filter((cat) => selectedFolder === 'ALL' || selectedFolder === cat)
          .map((cat) => {
            const files = datasetInfo?.categories[cat] || [];
            const filteredFiles = files.filter((f) => f.toLowerCase().includes(searchQuery.toLowerCase()));

            return (
              <div key={cat} className="bg-[#161b22] border border-[#30363d] rounded-xl p-4 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-3 border-b border-[#30363d] pb-2">
                    <span className="text-xs font-bold text-cyan-300 font-mono flex items-center gap-1.5">
                      <FolderCheck className="w-4 h-4 text-cyan-400" />
                      {cat}
                    </span>
                    <span className="text-[10px] text-gray-400 font-mono">
                      ~500 CSV files (~635 MB)
                    </span>
                  </div>

                  <div className="space-y-1.5 max-h-48 overflow-y-auto pr-1">
                    {filteredFiles.map((file) => (
                      <div
                        key={file}
                        onClick={() => onSelectDatasetFile(`${cat}/${file}`)}
                        className="flex items-center justify-between p-2 rounded bg-[#0d1117] hover:bg-cyan-500/10 border border-[#30363d] hover:border-cyan-400/50 cursor-pointer text-xs transition-colors group"
                      >
                        <div className="flex items-center gap-2 font-mono text-gray-300 group-hover:text-cyan-300">
                          <FileText className="w-3.5 h-3.5 text-gray-500 group-hover:text-cyan-400 shrink-0" />
                          <span className="text-[11px] truncate">{file}</span>
                        </div>
                        <span className="text-[10px] text-cyan-400 font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
                          Load & Analyze →
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="mt-3 pt-2 border-t border-[#30363d] text-[10px] text-gray-400 flex items-center justify-between">
                  <span>Channels: 15 Telemetry Streams</span>
                  <span>Row Count: 10,000</span>
                </div>
              </div>
            );
          })}
      </div>
    </div>
  );
}
