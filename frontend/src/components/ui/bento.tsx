"use client";
import { clsx } from "clsx";
import { motion } from "framer-motion";
import React from "react";

export function BentoCard({
  dark = false,
  className = "",
  eyebrow,
  title,
  description,
  graphic,
  fade = [],
  children
}: {
  dark?: boolean;
  className?: string;
  eyebrow?: React.ReactNode;
  title?: React.ReactNode;
  description?: React.ReactNode;
  graphic?: React.ReactNode;
  fade?: ("top" | "bottom")[];
  children?: React.ReactNode;
}) {
  return (
    <motion.div
      initial="idle"
      whileHover="active"
      variants={{ idle: {}, active: {} }}
      data-dark={dark ? "true" : undefined}
      className={clsx(
        className,
        "group relative flex flex-col overflow-hidden",
        // Crucial fixes for card structure: strong background, clear border, heavy shadow
        "bg-white dark:bg-[#1e2532] shadow-xl dark:shadow-2xl dark:shadow-black/60",
        "border border-gray-200 dark:border-white/15 rounded-3xl"
      )}
    >
      {/* Background Graphic */}
      <div className="absolute inset-0 z-0 overflow-hidden rounded-3xl pointer-events-none">
        {graphic}
        {fade.includes("top") && (
          <div className="absolute inset-0 bg-gradient-to-b from-white to-70% dark:from-[#1e2532] dark:to-transparent opacity-90" />
        )}
        {fade.includes("bottom") && (
          <div className="absolute inset-0 bg-gradient-to-t from-white to-70% dark:from-[#1e2532] dark:to-transparent opacity-90" />
        )}
      </div>
      
      {/* Content Area */}
      <div className="relative z-20 isolate h-full flex flex-col">
        {(eyebrow || title || description) && (
          <div className="p-6 md:p-8 backdrop-blur-md bg-white/60 dark:bg-black/20 border-b border-black/5 dark:border-white/10">
            {eyebrow && <div className="text-sm font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">{eyebrow}</div>}
            {title && <h2 className="mt-2 text-3xl font-black tracking-tight text-gray-900 dark:text-white">{title}</h2>}
            {description && <p className="mt-3 max-w-2xl text-base text-gray-600 dark:text-gray-300">{description}</p>}
          </div>
        )}
        <div className="flex-1 p-6 md:p-8 overflow-y-auto">
          {children}
        </div>
      </div>
    </motion.div>
  );
}
