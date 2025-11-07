import React from "react";

export default function Modal({ isOpen, onClose, title, children }) {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center">
            <div className="bg-white rounded-xl shadow-2xl w-full max-w-3xl mx-4 overflow-hidden animate-fadeIn">
                <div className="flex justify-between items-center p-4 border-b border-slate-200">
                    <h2 className="text-xl font-semibold text-slate-800">{title}</h2>
                    <button
                        onClick={onClose}
                        className="text-slate-500 hover:text-slate-800 font-bold text-lg"
                    >
                        ✕
                    </button>
                </div>
                <div className="p-4 overflow-y-auto max-h-[70vh]">{children}</div>
            </div>
        </div>
    );
}
