// Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
// Receptionist Dashboard & Check-In Verifier Component connected to FastAPI

import React, { useEffect, useState } from "react";
import { RosterItem } from "../types";
import { fetchRoster, verifyCheckin } from "../lib/api";

interface ReceptionistDashboardProps {
  activeTier?: string;
}

export const ReceptionistDashboard: React.FC<ReceptionistDashboardProps> = ({
  activeTier = "🟡 Tier 2: Pro"
}) => {
  const [rosterItems, setRosterItems] = useState<RosterItem[]>([]);
  const [checkInCode, setCheckInCode] = useState<string>("APX-4928");
  const [paymentMethod, setPaymentMethod] = useState<string>("UPI (GPay/PhonePe)");
  const [loading, setLoading] = useState<boolean>(false);
  const [verifying, setVerifying] = useState<boolean>(false);

  const loadRoster = async () => {
    try {
      setLoading(true);
      const data = await fetchRoster();
      setRosterItems(data.items);
    } catch (err) {
      console.error("Failed to load waiting room roster:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRoster();
    const interval = setInterval(loadRoster, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleVerify = async () => {
    if (!checkInCode.trim()) return;

    try {
      setVerifying(true);
      await verifyCheckin(checkInCode, paymentMethod);
      await loadRoster();
    } catch (err) {
      // Error handling managed by API layer toast
    } finally {
      setVerifying(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4 sm:p-6 bg-slate-100 min-h-screen font-sans">
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm mb-6">
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
          👩‍💼 Receptionist Desk & Check-In Verifier
        </h1>
        <p className="text-xs text-slate-500 mt-1">Real-time desk arrival verification and payment status tracker.</p>
      </div>

      {activeTier.includes("Tier 1") && (
        <div className="p-4 bg-amber-50 border-2 border-amber-400 rounded-2xl text-xs font-bold text-amber-900 mb-6 shadow-sm">
          🔒 Tier 2 Pro Upgrade Required: Offline check-in code verification (`APX-XXXX`) and live roster sync require Tier 2 Pro, Tier 2.5, or Tier 3 Enterprise.
        </div>
      )}

      {/* Verification Control Form */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm mb-6">
        <h3 className="text-sm font-bold text-slate-800 mb-3">🎫 Verify Arriving Patient Check-In</h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 items-end">
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Check-In Code (`APX-XXXX`):</label>
            <input
              type="text"
              value={checkInCode}
              onChange={(e) => setCheckInCode(e.target.value.toUpperCase())}
              placeholder="e.g. APX-4928"
              className="w-full p-2.5 border border-slate-300 rounded-lg text-xs font-bold uppercase tracking-wider focus:ring-2 focus:ring-emerald-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Payment Method Collected:</label>
            <select
              value={paymentMethod}
              onChange={(e) => setPaymentMethod(e.target.value)}
              className="w-full p-2.5 border border-slate-300 rounded-lg text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-none"
            >
              <option value="UPI (GPay/PhonePe)">UPI (GPay/PhonePe)</option>
              <option value="Cash">Cash</option>
              <option value="Credit/Debit Card">Credit/Debit Card</option>
              <option value="Direct Zero-Cost EMI">Direct Zero-Cost EMI</option>
            </select>
          </div>

          <button
            onClick={handleVerify}
            disabled={verifying || activeTier.includes("Tier 1")}
            className="py-2.5 px-4 bg-emerald-600 text-white font-bold text-xs rounded-lg hover:bg-emerald-700 disabled:opacity-50 transition-all shadow-sm"
          >
            {verifying ? "Verifying..." : "Verify Patient & Collect Payment"}
          </button>
        </div>
      </div>

      {/* Waiting Room Roster List */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-sm font-bold text-slate-800">📋 Today's Waiting Room Roster ({rosterItems.length})</h3>
          <button
            onClick={loadRoster}
            className="text-xs text-emerald-600 hover:text-emerald-700 font-bold"
          >
            🔄 Refresh List
          </button>
        </div>

        {loading ? (
          <div className="text-center py-6 text-xs text-slate-500">Refreshing waiting room list...</div>
        ) : rosterItems.length === 0 ? (
          <div className="text-center py-6 text-xs text-slate-500">No patient bookings in today's roster.</div>
        ) : (
          <div className="space-y-2">
            {rosterItems.map((item, idx) => {
              const isPaid = item.status.includes("PAID");
              return (
                <div
                  key={idx}
                  className="p-3.5 border border-slate-200 rounded-xl bg-white flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2"
                >
                  <div className="flex items-center gap-3">
                    <span className="font-mono font-bold text-xs bg-slate-100 text-slate-800 px-2.5 py-1 rounded-md border border-slate-300">
                      {item.check_in_code}
                    </span>
                    <div>
                      <span className="font-bold text-sm text-slate-900">{item.patient_name}</span>
                      <span className="text-xs text-slate-500 ml-2">({item.phone_number})</span>
                      <div className="text-xs text-slate-600 mt-0.5">
                        <b>Doctor</b>: {item.doctor_name} • <b>Procedure</b>: {item.procedure}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 self-end sm:self-center">
                    <span className="text-xs text-slate-500 font-medium">{item.slot_time}</span>
                    <span
                      className={`text-xs font-bold px-2.5 py-1 rounded-full ${
                        isPaid ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800"
                      }`}
                    >
                      {isPaid ? "🟢 " + item.status : "🟡 PENDING AT DESK"}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
