// Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
// Main Lovable Tabbed Application Container

import React, { useState } from "react";
import { PatientConcierge } from "./components/PatientConcierge";
import { DoctorCommandCenter } from "./components/DoctorCommandCenter";
import { ReceptionistDashboard } from "./components/ReceptionistDashboard";
import { ToastContainer } from "./components/ToastContainer";

export function App() {
  const [activeTab, setActiveTab] = useState<"patient" | "doctor" | "reception">("patient");
  const [activeTier, setActiveTier] = useState<string>("🟡 Tier 2: Pro");

  return (
    <div className="min-h-screen bg-slate-100 font-sans text-slate-900">
      <ToastContainer />

      {/* Main Header & Navigation Tabs */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center h-auto sm:h-16 py-3 sm:py-0 gap-3">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🏥</span>
            <div>
              <h1 className="font-extrabold text-base text-slate-900 tracking-tight">APEX AI — Copus Concierge</h1>
              <p className="text-[11px] text-slate-500 font-medium">FastAPI Backend (`http://localhost:8000/api/v1`)</p>
            </div>
            {/* Admin Tier Switcher */}
            <div className="ml-2">
              <select
                value={activeTier}
                onChange={(e) => setActiveTier(e.target.value)}
                className="p-1.5 bg-slate-100 border border-slate-300 rounded-lg text-xs font-bold text-slate-800 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="🟢 Tier 1: Essential">🟢 Tier 1: Essential</option>
                <option value="🟡 Tier 2: Pro">🟡 Tier 2: Pro</option>
                <option value="🧪 Tier 2.5: Beta Testing">🧪 Tier 2.5: Beta Testing</option>
                <option value="🔴 Tier 3: Enterprise">🔴 Tier 3: Enterprise</option>
              </select>
            </div>
          </div>

          <nav className="flex gap-1.5 bg-slate-100 p-1 rounded-xl border border-slate-200 w-full sm:w-auto justify-center">
            <button
              onClick={() => setActiveTab("patient")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeTab === "patient"
                  ? "bg-white text-emerald-700 shadow-sm"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              💬 WhatsApp Patient View
            </button>
            <button
              onClick={() => setActiveTab("doctor")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeTab === "doctor"
                  ? "bg-white text-emerald-700 shadow-sm"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              👨‍⚕️ Doctor Command Center
            </button>
            <button
              onClick={() => setActiveTab("reception")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeTab === "reception"
                  ? "bg-white text-emerald-700 shadow-sm"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              👩‍💼 Receptionist Dashboard
            </button>
          </nav>
        </div>
      </header>

      {/* Main Tab View Renderer */}
      <main className="py-4">
        {activeTab === "patient" && <PatientConcierge activeTier={activeTier} />}
        {activeTab === "doctor" && <DoctorCommandCenter activeTier={activeTier} />}
        {activeTab === "reception" && <ReceptionistDashboard activeTier={activeTier} />}
      </main>
    </div>
  );
}

export default App;
