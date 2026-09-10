import React, { useState } from 'react';
import { RotateCw } from 'lucide-react';

export default function DigitalTwinView() {
  const [iframeLoaded, setIframeLoaded] = useState(false);
  const digitalTwinUrl = "/3d-viewer/index.html";

  return (
    <div className="max-w-7xl mx-auto h-[82vh]">
      {/* 3D Viewport Container - Clean Full Height Viewport */}
      <div className="bg-[#0d1117] border border-[#30363d] rounded-xl overflow-hidden shadow-2xl relative h-full flex flex-col">
        {!iframeLoaded && (
          <div className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-[#0d1117] text-gray-400 text-xs">
            <RotateCw className="w-8 h-8 text-cyan-400 animate-spin mb-3" />
            <p className="font-semibold text-white">Loading C18 3D Digital Twin Model...</p>
            <p className="text-[10px] text-gray-500 mt-1">Initializing Three.js WebGL CAD Viewport</p>
          </div>
        )}

        <iframe
          src={digitalTwinUrl}
          title="3D Digital Twin Engine Viewer"
          onLoad={() => setIframeLoaded(true)}
          className="w-full h-full border-0 rounded-xl"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        />
      </div>
    </div>
  );
}
