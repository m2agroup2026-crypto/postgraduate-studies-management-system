import React, { useState } from "react";
import { Bot, Sparkles, Send, X } from "lucide-react";

export default function AIAssistant({ api, actions = [], onNavigate }) {
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState("");
  const [busy, setBusy] = useState(false);

  const [messages, setMessages] = useState([
    {
      from: "bot",
      text: "مرحبًا، أنا مساعد الدراسات العليا الذكي. كيف يمكنني مساعدتك؟",
    },
  ]);

  const send = async (value = q) => {
    if (!value.trim() || busy) return;

    const current = value;
    setQ("");

    setMessages((m) => [
      ...m,
      { from: "user", text: current },
    ]);

    setBusy(true);

    try {
      const response = await api("/assistant/", {
        method: "POST",
        body: JSON.stringify({
          message: current,
        }),
      });

      setMessages((m) => [
        ...m,
        { from: "bot", text: response.answer },
      ]);
    } catch (error) {
      setMessages((m) => [
        ...m,
        { from: "bot", text: error.message },
      ]);
    } finally {
      setBusy(false);
    }
  };

  const runQuickAction = (action) => {
    if (action.type === "navigate") {
      onNavigate?.(action.target);
      setOpen(false);
      return;
    }
    send(action.target);
  };

  return (
    <>
      <button
        className="assistantFab premiumAI"
        onClick={() => setOpen(!open)}
        aria-label="AI Assistant"
      >
        {open ? <X size={24} /> : <Sparkles size={24} />}
      </button>

      {open && (
        <div className="assistant premiumAssistant">
          <header>
            <div className="assistantIcon">
              <Bot size={22} />
            </div>

            <div>
              <b>AI Governance Assistant</b>
              <small>متصل ببياناتك المصرح بها</small>
            </div>
          </header>

          <div className="quickActions">
            {actions.map((action) => (
              <button
                key={action.id}
                type="button"
                onClick={() => runQuickAction(action)}
              >
                {action.label}
              </button>
            ))}
          </div>

          <div className="chat">
            {messages.map((message, index) => (
              <p
                className={message.from}
                key={index}
              >
                {message.text}
              </p>
            ))}

            {busy && (
              <p className="bot">
                جاري التحليل...
              </p>
            )}
          </div>

          <footer>
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              onKeyDown={(e) =>
                e.key === "Enter" && send()
              }
              placeholder="اسأل عن الطلاب أو الرسائل..."
            />

            <button
              onClick={() => send()}
              disabled={busy}
              aria-label="send"
            >
              <Send size={17} />
            </button>
          </footer>
        </div>
      )}
    </>
  );
}
