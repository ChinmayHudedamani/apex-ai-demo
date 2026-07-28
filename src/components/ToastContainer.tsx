// Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
// Toast Container Component

import React, { useEffect, useState } from "react";
import { subscribeToast, ToastMessage } from "../lib/toast";

export const ToastContainer: React.FC = () => {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  useEffect(() => {
    const unsubscribe = subscribeToast((newToast) => {
      setToasts((prev) => [...prev, newToast]);
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== newToast.id));
      }, 5000);
    });
    return unsubscribe;
  }, []);

  if (toasts.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-md w-full px-4">
      {toasts.map((toast) => {
        let bgClass = "bg-white border-slate-300 text-slate-900";
        let icon = "ℹ️";
        if (toast.type === "success") {
          bgClass = "bg-emerald-50 border-emerald-300 text-emerald-950";
          icon = "✅";
        } else if (toast.type === "error") {
          bgClass = "bg-rose-50 border-rose-300 text-rose-950";
          icon = "⚠️";
        }

        return (
          <div
            key={toast.id}
            className={`p-4 rounded-xl border shadow-lg transition-all duration-300 animate-slide-in flex items-start gap-3 ${bgClass}`}
          >
            <span className="text-xl">{icon}</span>
            <div className="flex-1">
              <h4 className="font-bold text-sm">{toast.title}</h4>
              <p className="text-xs mt-1 opacity-90 leading-relaxed">{toast.description}</p>
            </div>
            <button
              onClick={() => setToasts((prev) => prev.filter((t) => t.id !== toast.id))}
              className="text-xs text-slate-400 hover:text-slate-700 font-bold px-1"
            >
              ✕
            </button>
          </div>
        );
      })}
    </div>
  );
};
