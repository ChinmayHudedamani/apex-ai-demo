// Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
// Patient Concierge WhatsApp Interface Component connected to FastAPI

import React, { useEffect, useState } from "react";
import {
  Doctor,
  ClinicLocation,
  ClinicalServiceItem,
  BookingResponse
} from "../types";
import {
  fetchDoctors,
  fetchClinicLocation,
  fetchClinicalServices,
  createBooking
} from "../lib/api";

interface ChatMessage {
  sender: "user" | "assistant";
  text: string;
  time: string;
}

export const PatientConcierge: React.FC = () => {
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [location, setLocation] = useState<ClinicLocation | null>(null);
  const [services, setServices] = useState<ClinicalServiceItem[]>([]);
  const [servicesMarkdown, setServicesMarkdown] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);

  // Booking State Machine: IDLE -> VIEW_DOCTORS -> VIEW_PRICING -> SELECT_DOC -> SELECT_SLOT -> PATIENT_INFO -> CONFIRMATION
  const [bookingStep, setBookingStep] = useState<string>("IDLE");
  const [selectedDoctor, setSelectedDoctor] = useState<Doctor | null>(null);
  const [selectedSlot, setSelectedSlot] = useState<string>("");
  const [patientName, setPatientName] = useState<string>("");
  const [phoneNumber, setPhoneNumber] = useState<string>("");
  const [visitReason, setVisitReason] = useState<string>("General Consultation");
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [confirmedBooking, setConfirmedBooking] = useState<BookingResponse | null>(null);

  const [expandedServiceId, setExpandedServiceId] = useState<string | null>(null);

  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([
    {
      sender: "assistant",
      text: "Hello! I am **Copus Concierge** at Kasthuri Dental Clinic.\n\nHow can I assist you with your dental health today?",
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) + " IST"
    }
  ]);

  const getTimeStr = () =>
    new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) + " IST";

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [docsData, locData, srvData] = await Promise.all([
          fetchDoctors(),
          fetchClinicLocation(),
          fetchClinicalServices()
        ]);
        setDoctors(docsData);
        setLocation(locData);
        setServices(srvData.services);
        setServicesMarkdown(srvData.directory_markdown);
      } catch (err) {
        console.error("Failed to load initial data from backend:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleSelectDoctor = (doc: Doctor) => {
    setSelectedDoctor(doc);
    setChatHistory((prev) => [
      ...prev,
      { sender: "user", text: `Selected Doctor: ${doc.name}`, time: getTimeStr() },
      { sender: "assistant", text: `Great choice! Please pick an available time slot for **${doc.name}**:`, time: getTimeStr() }
    ]);
    setBookingStep("SELECT_SLOT");
  };

  const handleSelectSlot = (slot: string) => {
    setSelectedSlot(slot);
    setChatHistory((prev) => [
      ...prev,
      { sender: "user", text: `Chosen Slot: ${slot}`, time: getTimeStr() },
      { sender: "assistant", text: "Please provide your registration details to complete the booking:", time: getTimeStr() }
    ]);
    setBookingStep("PATIENT_INFO");
  };

  const handleConfirmBooking = async () => {
    if (!selectedDoctor || !selectedSlot) return;

    try {
      setIsSubmitting(true);
      const response = await createBooking({
        patient_name: patientName,
        phone_number: phoneNumber,
        doctor_id: selectedDoctor.id,
        slot_time: selectedSlot,
        reason: visitReason
      });

      setConfirmedBooking(response);

      const finalReply =
        `🎉 **APPOINTMENT LOCKED & CONFIRMED!**\n\n` +
        `🎫 **Check-In Code**: \`${response.check_in_code}\`\n` +
        `👤 **Patient**: ${response.patient_name}\n` +
        `👨‍⚕️ **Doctor**: ${response.doctor_name}\n` +
        `🕒 **Confirmed Slot**: ${response.slot_time}\n` +
        `💳 **Payment**: **Pay at Clinic Desk** upon arrival (Cash / UPI / Card)\n\n` +
        `📍 **Address**: ${response.clinic_location}\n\n` +
        `Please present check-in code \`${response.check_in_code}\` at the reception desk.`;

      setChatHistory((prev) => [
        ...prev,
        { sender: "assistant", text: finalReply, time: getTimeStr() }
      ]);
      setBookingStep("IDLE");
    } catch (err) {
      // Toast handles error display
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4 sm:p-6 bg-slate-100 min-h-screen font-sans">
      {/* WhatsApp Business Header */}
      <div className="bg-white p-4 sm:p-5 rounded-2xl border-l-8 border-emerald-600 shadow-md flex justify-between items-center mb-6">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            Kasthuri Dental Clinic <span className="text-xs text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full font-bold">✔ Verified</span>
          </h2>
          <p className="text-xs text-slate-500 font-medium">Copus AI Concierge • <span className="text-emerald-600 font-bold">Online</span></p>
        </div>
        <div className="text-xs font-semibold text-slate-500 bg-slate-100 px-3 py-1.5 rounded-lg">
          {location?.branch.split("—")[1] || "Yelahanka Node"}
        </div>
      </div>

      {/* Chat Stream */}
      <div className="space-y-3 mb-6 max-h-[420px] overflow-y-auto pr-1">
        {chatHistory.map((msg, idx) => (
          <div
            key={idx}
            className={`p-4 rounded-2xl max-w-2xl text-sm shadow-sm ${
              msg.sender === "user"
                ? "bg-emerald-600 text-white ml-auto rounded-br-none font-medium"
                : "bg-white text-slate-800 border border-slate-200 rounded-bl-none"
            }`}
          >
            <div className="whitespace-pre-line leading-relaxed">{msg.text}</div>
            <div className={`text-[10px] mt-1.5 text-right ${msg.sender === "user" ? "text-emerald-100" : "text-slate-400"}`}>
              {msg.time}
            </div>
          </div>
        ))}
      </div>

      {/* Action Options Controls */}
      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        {loading ? (
          <div className="text-center py-6 text-slate-500 font-medium">Loading clinical directory from server...</div>
        ) : (
          <>
            {bookingStep === "IDLE" && (
              <div>
                <h3 className="text-sm font-bold text-slate-700 mb-3">📱 Tap an option below:</h3>
                <div className="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
                  <button
                    onClick={() => {
                      setChatHistory((prev) => [...prev, { sender: "user", text: "View Our Doctors", time: getTimeStr() }]);
                      setBookingStep("VIEW_DOCTORS");
                    }}
                    className="p-3 bg-white border-2 border-emerald-600 text-emerald-700 hover:bg-emerald-600 hover:text-white font-bold text-xs rounded-xl transition-all shadow-sm"
                  >
                    👨‍⚕️ View Our Doctors
                  </button>

                  <button
                    onClick={() => {
                      setChatHistory((prev) => [...prev, { sender: "user", text: "Clinic Location & Map", time: getTimeStr() }]);
                      if (location) {
                        const reply =
                          `📍 **${location.branch}**\n\n` +
                          `🏢 **Address**: ${location.address}\n` +
                          `🚩 **Landmark**: ${location.landmark}\n` +
                          `🕒 **Hours**: ${location.hours}\n` +
                          `📞 **Phone**: ${location.phone}\n\n` +
                          `🔗 [📍 Click Here to Open in Google Maps](${location.map_url})`;
                        setChatHistory((prev) => [...prev, { sender: "assistant", text: reply, time: getTimeStr() }]);
                      }
                    }}
                    className="p-3 bg-white border-2 border-emerald-600 text-emerald-700 hover:bg-emerald-600 hover:text-white font-bold text-xs rounded-xl transition-all shadow-sm"
                  >
                    📍 Clinic Location & Map
                  </button>

                  <button
                    onClick={() => {
                      setChatHistory((prev) => [...prev, { sender: "user", text: "Cost Ranges & Pricing", time: getTimeStr() }]);
                      setChatHistory((prev) => [...prev, { sender: "assistant", text: servicesMarkdown, time: getTimeStr() }]);
                      setBookingStep("VIEW_PRICING");
                    }}
                    className="p-3 bg-white border-2 border-emerald-600 text-emerald-700 hover:bg-emerald-600 hover:text-white font-bold text-xs rounded-xl transition-all shadow-sm"
                  >
                    💳 Cost & Pricing Sheet
                  </button>

                  <button
                    onClick={() => {
                      setChatHistory((prev) => [...prev, { sender: "user", text: "Book Appointment", time: getTimeStr() }]);
                      setChatHistory((prev) => [...prev, { sender: "assistant", text: "Step 1 of 4: Please select your specialist doctor:", time: getTimeStr() }]);
                      setBookingStep("SELECT_DOC");
                    }}
                    className="p-3 bg-white border-2 border-emerald-600 text-emerald-700 hover:bg-emerald-600 hover:text-white font-bold text-xs rounded-xl transition-all shadow-sm"
                  >
                    📅 Book Appointment
                  </button>

                  <button
                    onClick={() => {
                      setChatHistory((prev) => [...prev, { sender: "user", text: "Emergency Triage", time: getTimeStr() }]);
                      setChatHistory((prev) => [...prev, { sender: "assistant", text: "🚨 **Dental Emergency**: Call our duty surgeon directly:\n📞 **+91 98765 43210**", time: getTimeStr() }]);
                    }}
                    className="p-3 bg-rose-50 border-2 border-rose-600 text-rose-700 hover:bg-rose-600 hover:text-white font-bold text-xs rounded-xl transition-all shadow-sm col-span-2 sm:col-span-1"
                  >
                    🚨 Emergency Triage
                  </button>
                </div>
              </div>
            )}

            {/* Doctors Directory List View */}
            {bookingStep === "VIEW_DOCTORS" && (
              <div>
                <h3 className="text-base font-bold text-slate-800 mb-3">👨‍⚕️ Our Dental Specialists Directory:</h3>
                <div className="space-y-3 max-h-96 overflow-y-auto pr-1">
                  {doctors.map((doc) => (
                    <div key={doc.id} className="p-4 border border-slate-200 rounded-xl bg-white shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                      <div>
                        <div className="font-bold text-emerald-700 text-base flex items-center gap-2">
                          {doc.name}
                          {doc.status && <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 font-semibold">{doc.status}</span>}
                        </div>
                        <div className="text-xs font-semibold text-slate-600">{doc.degree} • {doc.exp}</div>
                        <div className="text-xs text-slate-600 mt-1"><b>Specialties</b>: {doc.specialty}</div>
                        <div className="text-xs text-slate-600"><b>Hours</b>: {doc.hours}</div>
                        <div className="text-xs text-emerald-600 font-bold mt-1">{doc.rating}</div>
                      </div>
                      <button
                        onClick={() => handleSelectDoctor(doc)}
                        className="px-4 py-2 bg-emerald-600 text-white font-bold text-xs rounded-lg hover:bg-emerald-700 transition-all shadow-sm shrink-0"
                      >
                        📅 Book with {doc.name.split(" ")[1]}
                      </button>
                    </div>
                  ))}
                </div>
                <button
                  onClick={() => setBookingStep("IDLE")}
                  className="mt-4 px-4 py-2 border border-slate-300 text-slate-600 font-bold text-xs rounded-lg hover:bg-slate-50"
                >
                  ⬅️ Back to Main Options
                </button>
              </div>
            )}

            {/* Interactive Clinical Service Directory View */}
            {bookingStep === "VIEW_PRICING" && (
              <div>
                <h3 className="text-base font-bold text-slate-800">🏥 Clinical Services & Fee Directory</h3>
                <p className="text-xs text-slate-500 mb-4">All treatments include painless digital local anesthesia and strict ISO-sterilization protocols.</p>

                <div className="space-y-3 max-h-96 overflow-y-auto pr-1">
                  {services.map((srv) => {
                    const isExpanded = expandedServiceId === srv.id;
                    return (
                      <div key={srv.id} className="border border-slate-200 rounded-xl bg-white overflow-hidden shadow-sm">
                        <button
                          onClick={() => setExpandedServiceId(isExpanded ? null : srv.id)}
                          className="w-full p-4 text-left flex justify-between items-center hover:bg-slate-50 transition-colors"
                        >
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-slate-900 text-sm">{srv.title}</span>
                            <span className="text-[10px] font-bold text-white px-2 py-0.5 rounded-full" style={{ backgroundColor: srv.badge_bg }}>
                              {srv.badge}
                            </span>
                          </div>
                          <span className="font-bold text-emerald-700 text-sm">{srv.fee}</span>
                        </button>

                        {isExpanded && (
                          <div className="p-4 bg-slate-50 border-t border-slate-200 text-xs space-y-2">
                            <div><b>💰 Fee Tiers</b>:</div>
                            <ul className="list-disc pl-5 text-slate-700 space-y-0.5">
                              {srv.tiers.map((t, idx) => <li key={idx}>{t}</li>)}
                            </ul>
                            <div><b>🕒 Duration</b>: {srv.duration}</div>
                            <div><b>✅ What's Included</b>:</div>
                            <ul className="list-disc pl-5 text-slate-700 space-y-0.5">
                              {srv.included.map((inc, idx) => <li key={idx}>{inc}</li>)}
                            </ul>
                            <div><b>🩺 Indications</b>: {srv.indications}</div>

                            <button
                              onClick={() => {
                                setBookingStep("SELECT_DOC");
                              }}
                              className="mt-3 px-4 py-2 bg-emerald-600 text-white font-bold rounded-lg hover:bg-emerald-700"
                            >
                              📅 Book This Procedure
                            </button>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>

                {/* Transparency Guarantee Box */}
                <div className="mt-4 p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-xs">
                  <div className="font-bold text-emerald-800 mb-1">💳 Patient Payment Transparency & Guarantee</div>
                  <div className="text-slate-700">
                    <b>No hidden charges.</b> Full written cost estimate provided prior to treatment. Flexible payment options (Cash, UPI, Credit Card, Direct Zero-Cost EMI) collected at the desk after consultation.
                  </div>
                </div>

                <button
                  onClick={() => setBookingStep("IDLE")}
                  className="mt-4 px-4 py-2 border border-slate-300 text-slate-600 font-bold text-xs rounded-lg hover:bg-slate-50"
                >
                  ⬅️ Back to Main Options
                </button>
              </div>
            )}

            {/* Select Doctor Step */}
            {bookingStep === "SELECT_DOC" && (
              <div>
                <h3 className="text-sm font-bold text-slate-800 mb-3">👨‍⚕️ Step 1: Select Your Preferred Doctor</h3>
                <div className="space-y-2">
                  {doctors.map((doc) => (
                    <div key={doc.id} className="p-3 border border-slate-200 rounded-xl flex justify-between items-center bg-white">
                      <div>
                        <div className="font-bold text-sm text-slate-900">{doc.name} ({doc.degree})</div>
                        <div className="text-xs text-slate-500">{doc.specialty} • {doc.hours}</div>
                      </div>
                      <button
                        onClick={() => handleSelectDoctor(doc)}
                        className="px-3 py-1.5 bg-emerald-600 text-white font-bold text-xs rounded-lg hover:bg-emerald-700"
                      >
                        Select
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Select Slot Step */}
            {bookingStep === "SELECT_SLOT" && selectedDoctor && (
              <div>
                <h3 className="text-sm font-bold text-slate-800 mb-3">⏰ Step 2: Available Slots for {selectedDoctor.name}</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedDoctor.slots.map((slot, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSelectSlot(slot)}
                      className="px-4 py-2 bg-white border-2 border-emerald-600 text-emerald-700 hover:bg-emerald-600 hover:text-white font-bold text-xs rounded-xl transition-all"
                    >
                      ⏰ {slot}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Patient Registration Form Step */}
            {bookingStep === "PATIENT_INFO" && (
              <div>
                <h3 className="text-sm font-bold text-slate-800 mb-3">📋 Step 3: Patient Information</h3>
                <div className="space-y-3 max-w-md">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Full Name:</label>
                    <input
                      type="text"
                      value={patientName}
                      onChange={(e) => setPatientName(e.target.value)}
                      placeholder="e.g. Chinmay Hudedamani"
                      className="w-full p-2.5 border border-slate-300 rounded-lg text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Mobile Phone Number (+91):</label>
                    <input
                      type="text"
                      value={phoneNumber}
                      onChange={(e) => setPhoneNumber(e.target.value)}
                      placeholder="e.g. 9876543210"
                      className="w-full p-2.5 border border-slate-300 rounded-lg text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Reason for Visit:</label>
                    <select
                      value={visitReason}
                      onChange={(e) => setVisitReason(e.target.value)}
                      className="w-full p-2.5 border border-slate-300 rounded-lg text-xs font-medium focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    >
                      <option value="General Consultation">General Consultation</option>
                      <option value="Toothache / Pain">Toothache / Pain</option>
                      <option value="Root Canal Evaluation">Root Canal Evaluation</option>
                      <option value="Braces / Aligners">Braces / Aligners</option>
                      <option value="Cleaning & Scaling">Cleaning & Scaling</option>
                    </select>
                  </div>

                  <button
                    onClick={() => setBookingStep("CONFIRMATION")}
                    className="w-full py-2.5 bg-emerald-600 text-white font-bold text-xs rounded-lg hover:bg-emerald-700"
                  >
                    Proceed to Confirmation ➡️
                  </button>
                </div>
              </div>
            )}

            {/* Booking Confirmation Step */}
            {bookingStep === "CONFIRMATION" && selectedDoctor && (
              <div>
                <h3 className="text-sm font-bold text-slate-800 mb-3">📄 Step 4: Confirm Your Appointment Summary</h3>
                <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-xs space-y-1.5 mb-4 text-slate-800">
                  <div>👤 <b>Patient</b>: {patientName} (+91 {phoneNumber})</div>
                  <div>👨‍⚕️ <b>Doctor</b>: {selectedDoctor.name} ({selectedDoctor.degree})</div>
                  <div>🕒 <b>Slot</b>: {selectedSlot}</div>
                  <div>🦷 <b>Reason</b>: {visitReason}</div>
                  <div>📍 <b>Location</b>: {location?.branch}</div>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={handleConfirmBooking}
                    disabled={isSubmitting}
                    className="flex-1 py-2.5 bg-emerald-600 text-white font-bold text-xs rounded-lg hover:bg-emerald-700 disabled:opacity-50"
                  >
                    {isSubmitting ? "Locking Slot on Backend..." : "✅ Confirm & Lock Appointment"}
                  </button>
                  <button
                    onClick={() => setBookingStep("IDLE")}
                    className="px-4 py-2.5 border border-slate-300 text-slate-600 font-bold text-xs rounded-lg hover:bg-slate-50"
                  >
                    Restart
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};
