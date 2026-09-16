import React from 'react';
import { Sidebar as AceternitySidebar, SidebarBody, SidebarLink, useSidebar } from './ui/sidebar';
import { motion } from 'framer-motion';
import { 
  FileSpreadsheet, 
  Activity, 
  BarChart3, 
  Sparkles, 
  MessageSquare, 
  Gauge, 
  Box,
  Sun,
  Moon
} from 'lucide-react';


const LogoText = () => {
  const { open, animate } = useSidebar();
  return (
    <motion.div
      animate={{
        display: animate ? (open ? "block" : "none") : "block",
        opacity: animate ? (open ? 1 : 0) : 1,
      }}
      className="overflow-hidden whitespace-nowrap font-sans"
    >
      <h1 className="text-sm font-bold tracking-wide dark:text-white leading-tight bg-clip-text text-transparent bg-[linear-gradient(to_right,#3264AD,#00008b,red)] dark:bg-none dark:text-white dark:bg-transparent">DIESEL I6 ENGINE</h1>
      <p className="text-[10px] text-cyan-600 dark:text-cyan-400 font-mono font-semibold">LLM Diagnostic Suite</p>
    </motion.div>
  );
};

export default function Sidebar({ activeTab, setActiveTab, hardwareInfo, isCollapsed, setIsCollapsed, isDarkMode, setIsDarkMode }) {
  const navItems = [
    { id: 'overview', label: 'Diagnostics Overview', icon: <FileSpreadsheet className="class-for-icon" /> },
    { id: 'llm', label: 'RAG LLM Repair Report', icon: <Sparkles className="class-for-icon" /> },
    { id: 'digitaltwin', label: '3D Engine Digital Twin', icon: <Box className="class-for-icon" /> },
    { id: 'schematic', label: 'Engine Visual HUD', icon: <Activity className="class-for-icon" /> },
    { id: 'physics', label: 'Physics & PINN Metrics', icon: <BarChart3 className="class-for-icon" /> },
    { id: 'chat', label: 'Mechanic AI Chat', icon: <MessageSquare className="class-for-icon" /> },
  ];

  return (
    <AceternitySidebar open={!isCollapsed} setOpen={(val) => setIsCollapsed(!val)}>
      <SidebarBody className="justify-between gap-10 h-screen bg-white dark:bg-[#161b22] border-r border-gray-200 dark:border-[#30363d]">
        <div className="flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
          <div className="flex items-center gap-2 py-2">
            <div className="flex items-center justify-center bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 shrink-0 rounded-lg w-6 h-6">
              <Gauge className="w-4 h-4 animate-pulse" />
            </div>
            <LogoText />
          </div>
          
          <div className="mt-8 flex flex-col gap-2">
            {navItems.map((item) => (
              <SidebarLink 
                key={item.id} 
                link={{
                  label: item.label,
                  href: "#",
                  icon: React.cloneElement(item.icon, { 
                    className: `h-5 w-5 flex-shrink-0 transition-colors ${activeTab === item.id ? 'text-red-600 dark:text-cyan-400' : 'text-[#3264AD] group-hover/sidebar:text-[#00008b] dark:text-neutral-400'}` 
                  })
                }} 
                onClick={() => setActiveTab(item.id)}
                className={activeTab === item.id ? "bg-gray-100 dark:bg-[#21262d] rounded-lg text-red-600 dark:text-cyan-400" : "rounded-lg text-[#3264AD] hover:text-[#00008b] dark:text-neutral-400"}
              />
            ))}
          </div>
        </div>

        <div>
           <SidebarLink 
              onClick={() => setIsDarkMode(!isDarkMode)}
              link={{
                label: isDarkMode ? "Light Mode" : "Dark Mode",
                href: "#",
                icon: isDarkMode 
                  ? <Sun className="text-gray-500 dark:text-neutral-400 h-5 w-5 flex-shrink-0" /> 
                  : <Moon className="text-gray-500 dark:text-neutral-400 h-5 w-5 flex-shrink-0" />
              }}
           />
        </div>
      </SidebarBody>
    </AceternitySidebar>
  );
}