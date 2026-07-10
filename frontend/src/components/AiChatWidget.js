"use client";
import { useState } from "react";
import api from "@/lib/api";

export default function AiChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: "assistant", text: "Ask me about your team's reports — e.g. \"What blockers came up this week?\"" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!input.trim()) return;
    const question = input.trim();
    setMessages((m) => [...m, { role: "user", text: question }]);
    setInput("");
    setLoading(true);
    try {
      const { data } = await api.post("/ai/chat/", { message: question });
      setMessages((m) => [...m, { role: "assistant", text: data.answer || data.error }]);
    } catch (err) {
      setMessages((m) => [
        ...m,
        { role: "assistant", text: "Something went wrong reaching the assistant." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 bg-brand-600 text-white rounded-full px-5 py-3 text-sm shadow-lg hover:bg-brand-700"
      >
        💬 Ask AI
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 w-80 bg-white border rounded-xl shadow-xl flex flex-col h-96">
      <div className="flex justify-between items-center px-4 py-3 border-b">
        <span className="text-sm font-medium text-slate-800">Team AI Assistant</span>
        <button onClick={() => setOpen(false)} className="text-slate-400 hover:text-slate-600 text-sm">
          ✕
        </button>
      </div>
      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-2">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`text-sm rounded-lg px-3 py-2 max-w-[85%] ${
              m.role === "user"
                ? "bg-brand-600 text-white ml-auto"
                : "bg-slate-100 text-slate-700"
            }`}
          >
            {m.text}
          </div>
        ))}
        {loading && <div className="text-xs text-slate-400">Thinking…</div>}
      </div>
      <div className="p-3 border-t flex gap-2">
        <input
          className="flex-1 border rounded-lg px-3 py-2 text-sm"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Ask a question…"
        />
        <button
          onClick={send}
          className="text-sm bg-brand-600 text-white rounded-lg px-3 hover:bg-brand-700"
        >
          Send
        </button>
      </div>
    </div>
  );
}
