// Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
// Toast Notification Event Bus & Utility

export interface ToastMessage {
  id: string;
  type: "success" | "error" | "info";
  title: string;
  description: string;
}

type ToastListener = (toast: ToastMessage) => void;
const listeners: Set<ToastListener> = new Set();

export const subscribeToast = (listener: ToastListener) => {
  listeners.add(listener);
  return () => listeners.delete(listener);
};

export const showToast = (type: "success" | "error" | "info", title: string, description: string) => {
  const toast: ToastMessage = {
    id: Math.random().toString(36).substring(2, 9),
    type,
    title,
    description
  };
  listeners.forEach((listener) => listener(toast));
};
