// Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
// Doctor Command Center Component connected to FastAPI

import React, { useEffect, useState } from "react";
import { Doctor } from "../types";
import { fetchDoctors, triggerOTOverride } from "../lib/api";

export const DoctorCommandCenter: React.FC = () => {
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [selectedDoctorId, setSelectedDoctorId] = useState<string>("DOC_1");
  const [affectedSlot, setAffectedSlot] = useState<string>("11:30 AM – 01:00 PM IST");
  const [overrideReason, setOverrideReason] = useState<string>("Emergency surgical intervention");
  const [submitting, setSubmitting] = useState<boolean>(false);

  const loadDoctors = async () => {
    try {
      const data = await fetchDoctors();
      setDoctors(data);
    } catch (err) {
      console.error("Failed to load doctor directory:", err);
    }
  };

  useEffect(() => {
    loadDoctors();
  }, []);

  const handleOTOverride = async () => {
    if (!affectedSlot.trim() || !overrideReason.trim()) return;

    try {
      setSubmitting(true);
      await triggerOTOverride(selectedDoctorId, affectedSlot, overrideReason);
      await loadDoctors();
    } catch (err) {
      // Handled by toast notification system
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4 sm:p-6 bg-slate-100 min-h-screen font-sans">
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm mb-6">
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
          👨‍⚕️ Doctor Command Center
        </h1>
        <p className="text-xs text-slate-500 mt-1">Lead Surgeon OT Management & Schedule Override Operations.</p>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs text-slate-500 font-medium">Today's Roster</div>
          <div className="text-2xl font-extrabold text-emerald-600 mt-1">3 Patients</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs text-slate-500 font-medium">Confirmed Check-Ins</div>
          <div className="text-2xl font-extrabold text-emerald-600 mt-1">2 Verified</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs text-slate-500 font-medium">Emergency Priority</div>
          <div className="text-2xl font-extrabold text-amber-600 mt-1">1 Acute</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs text-slate-500 font-medium">Revenue Protected</div>
          <div className="text-2xl font-extrabold text-emerald-600 mt-1">₹48,500</div>
        </div>
      </div>

      {/* Emergency OT Override Control Form */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm mb-6">
        <h3 className="text-sm font-bold text-rose-700 mb-3 flex items-center gap-1.5">
          🚨 OT Emergency Schedule Override
        </h3>

        <div className="space-y-3 max-w-lg">
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Select Surgeon:</label>
            <select
              value={selectedDoctorId}
              onChange={(e) => setSelectedDoctorId(e.target.value)}
              className="w-full p-2.5 border border-slate-300 rounded-lg text-xs font-medium focus:ring-2 focus:ring-rose-500 focus:outline-none"
            >
              {doctors.map((doc) => (
                <option key={doc.id} value={doc.id}>
                  {doc.name} ({doc.degree}) {doc.status ? `— ${doc.status}` : ""}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Select OT Slot to Clear:</label>
            <select
              value={affectedSlot}
              onChange={(e) => setAffectedSlot(e.target.value)}
              className="w-full p-2.5 border border-slate-300 rounded-lg text-xs font-medium focus:ring-2 focus:ring-rose-500 focus:outline-none"
            >
              <option value="11:30 AM – 01:00 PM IST">11:30 AM – 01:00 PM IST</option>
              <option value="03:00 PM – 04:30 PM IST">03:00 PM – 04:30 PM IST</option>
              <option value="05:00 PM – 06:30 PM IST">05:00 PM – 06:30 PM IST</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Override Reason:</label>
            <input
              type="text"
              value={overrideReason}
              onChange={(e) => setOverrideReason(e.target.value)}
              placeholder="e.g. Acute surgical intervention"
              className="w-full p-2.5 border border-slate-300 rounded-lg text-xs font-medium focus:ring-2 focus:ring-rose-500 focus:outline-none"
            />
          </div>

          <button
            onClick={handleOTOverride}
            disabled={submitting}
            className="w-full py-2.5 px-4 bg-rose-600 text-white font-bold text-xs rounded-lg hover:bg-rose-700 disabled:opacity-50 transition-all shadow-sm"
          >
            {submitting ? "Dispatching Alerts..." : "⚡ Issue Proactive Reschedule Alerts"}
          </button>
        </div>
      </div>

      {/* Active Surgeon Status Board */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
        <h3 className="text-sm font-bold text-slate-800 mb-3">👨‍⚕️ Surgeon Operational Status Board</h3>
        <div className="space-y-2">
          {doctors.map((doc) => (
            <div key={doc.id} className="p-3 border border-slate-200 rounded-xl flex justify-between items-center bg-white">
              <div>
                <div className="font-bold text-sm text-slate-900">{doc.name}</div>
                <div className="text-xs text-slate-500">{doc.degree} • {doc.specialty}</div>
              </div>
              <span className="text-xs font-bold px-3 py-1 rounded-full bg-slate-100 text-slate-800">
                {doc.status || "🟢 Available"}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
