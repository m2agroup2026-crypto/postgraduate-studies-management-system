import React, { useState } from "react";
import { Bot } from "lucide-react";

export default function AIAssistant({ api }) {
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState("");
  const [busy, setBusy] = useState(false);

  const [messages, setMessages] = useState([
    {
      from: "bot",
      text: "مرحبًا، أنا مساعد الدراسات العليا. كيف أساعدك اليوم؟",
    },
  ]);

  const send = async () => {
    if (!q.trim() || busy) return;

    const current = q;
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

  return (
    <>
      <button
        className="assistantFab"
        onClick={() => setOpen(!open)}
      >
        <Bot />
      </button>

      {open && (
        <div className="assistant">
          <header>
            <Bot />

            <div>
              <b>المساعد الذكي</b>
              <small>
                متصل ببياناتك المصرح بها
              </small>
            </div>
          </header>

          <div className="chat">
            {messages.map((message, index) => (
              <p
                className={message.from}
                key={index}
              >
                {message.text}
              </p>
            ))}
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
              onClick={send}
              disabled={busy}
            >
              {busy ? "..." : "إرسال"}
            </button>
          </footer>
        </div>
      )}
    </>
  );
}
