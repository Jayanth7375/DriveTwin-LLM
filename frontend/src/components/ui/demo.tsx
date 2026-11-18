import React from "react";
import { BentoCard } from "./bento";
import { Activity } from "lucide-react";

export default function DemoOne() {
  return (
    <div className="w-full min-h-screen p-4 md:p-10 bg-gray-50 dark:bg-[#0d1117] flex items-center justify-center">
      <div className="w-full max-w-6xl">
        <BentoCard
          eyebrow={
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-cyan-400" />
              <span>Real-Time Engine Telemetry</span>
            </div>
          }
          title="Full-Sized Command Center"
          description="A complete view of your entire engine fleet diagnostics, predictive maintenance schedules, and real-time telemetry streaming straight from the digital twin model."
          graphic={
            <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2000&auto=format&fit=crop')] bg-cover bg-center" />
          }
          className="w-full h-[600px] rounded-3xl shadow-2xl border-white/10"
          dark={true}
          fade={["bottom"]}
        />
      </div>
    </div>
  );
}
