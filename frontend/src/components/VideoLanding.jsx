import React, { useRef, useEffect } from 'react';

export default function VideoLanding({ onEnter }) {
  const videoRef = useRef(null);

  useEffect(() => {
    // Attempt to auto-play the video when mounted
    if (videoRef.current) {
      videoRef.current.play().catch(error => {
        console.warn("Auto-play was prevented. The user might need to interact first.", error);
      });
    }
  }, []);

  return (
    <div className="w-full h-screen bg-black relative flex items-center justify-center overflow-hidden">
      <video
        ref={videoRef}
        src="/landing-video.mp4"
        className="absolute w-full h-full object-cover"
        muted
        playsInline
        onEnded={onEnter} // Automatically enter the dashboard when the video finishes
      />
      
      {/* Enter Dashboard Button positioned absolutely over the video */}
      <div className="absolute bottom-12 left-0 right-0 flex justify-center z-50">
        <button 
          onClick={onEnter}
          className="px-8 py-4 bg-cyan-600/80 hover:bg-cyan-500 text-white font-bold rounded-full shadow-[0_0_20px_rgba(34,211,238,0.4)] hover:shadow-[0_0_30px_rgba(34,211,238,0.6)] backdrop-blur-sm transition-all uppercase tracking-widest"
        >
          Skip to Dashboard
        </button>
      </div>
    </div>
  );
}

