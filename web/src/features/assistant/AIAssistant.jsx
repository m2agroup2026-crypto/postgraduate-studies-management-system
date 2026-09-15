import React, { useEffect, useRef, useState } from "react";
import { Activity, ArrowUp, Bot, Database, Maximize2, Minimize2, Network, RotateCcw, ShieldCheck, Sparkles, Wifi, X } from "lucide-react";
import { localized } from "../../i18n";

const EXAMPLES = {
  ar: ["كم عدد الطلاب المسجلين؟", "ما الرسائل التي تحتاج قرارًا؟", "اعرض المناقشات القادمة"],
  en: ["How many students are registered?", "Show pending approvals.", "Show upcoming defenses."],
};

const messageId = () => globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random().toString(36).slice(2)}`;

export default function AIAssistant({ api, actions = [], onNavigate, language = "ar" }) {
  const [open, setOpen] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const [question, setQuestion] = useState("");
  const [busy, setBusy] = useState(false);
  const [messages, setMessages] = useState([]);
  const [brief, setBrief] = useState(null);
  const chatRef = useRef(null);
  const inputRef = useRef(null);
  const ar = language === "ar";

  useEffect(() => { if (open) inputRef.current?.focus(); }, [open]);
  useEffect(() => {
    if (!open || brief) return;
    let active = true;
    api("/assistant/")
      .then((payload) => active && setBrief(payload.brief || null))
      .catch(() => active && setBrief(null));
    return () => { active = false; };
  }, [api, brief, open]);
  useEffect(() => { chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight, behavior: "smooth" }); }, [busy, messages]);
  useEffect(() => {
    const closeOnEscape = (event) => { if (event.key === "Escape" && open) setOpen(false); };
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [open]);

  const send = async (value = question) => {
    const current = value.trim();
    if (!current || busy) return;
    setQuestion("");
    setMessages((items) => [...items, { id: messageId(), from: "user", text: current }]);
    setBusy(true);
    try {
      const response = await api("/assistant/", { method: "POST", body: JSON.stringify({ message: current }) });
      setMessages((items) => [...items, {
        id: messageId(), from: "bot",
        text: response.answer || (ar ? "لم تصل إجابة من النظام." : "The system returned no answer."),
        intent: response.intent,
        data: response.data,
      }]);
    } catch (error) {
      setMessages((items) => [...items, {
        id: messageId(), from: "bot", error: true, retry: current,
        text: error.message || (ar ? "تعذر الاتصال بالمساعد." : "The assistant is unavailable."),
      }]);
    } finally { setBusy(false); }
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
    <div className="academicAssistantRoot" dir={ar ? "rtl" : "ltr"}>
      <button className={`intelligenceOrb ${open ? "isOpen" : ""}`} type="button" onClick={() => setOpen((value) => !value)} aria-expanded={open} aria-controls="academic-mission-assistant" aria-label={open ? (ar ? "إغلاق المساعد الأكاديمي" : "Close academic assistant") : (ar ? "فتح المساعد الأكاديمي" : "Open academic assistant")}>
        <span className="orbRadar" aria-hidden="true"><i /><i /><i /></span>
        <span className="orbCore">{open ? <X size={22} /> : <Bot size={23} />}</span>
        <span className="orbIdentity"><small>AI CORE / ONLINE</small><strong>{ar ? "مساعدك الأكاديمي" : "Academic copilot"}</strong></span>
      </button>

      {open && (
        <section id="academic-mission-assistant" className={`intelligenceConsole ${expanded ? "isExpanded" : ""}`} role="dialog" aria-modal="false" aria-labelledby="academic-assistant-title">
          <aside className="intelligenceRail">
            <div className="railCore"><span><Network size={21} /></span><small>ASSIUT MEDICINE</small><b>ACADEMIC<br />INTELLIGENCE</b></div>
            <div className="railTelemetry">
              <span><i className="online" />{ar ? "البيانات متصلة" : "Data connected"}</span>
              <span><ShieldCheck size={13} />{ar ? "النطاق مصرح" : "Permission scoped"}</span>
            </div>
            {brief?.metrics && <div className="railMetrics">
              {Object.entries(brief.metrics).map(([key, value]) => <div key={key}><small>{key}</small><strong>{value}</strong></div>)}
            </div>}
            <small className="railCode">PGMS / AI-01</small>
          </aside>

          <div className="intelligenceWorkspace">
            <header className="intelligenceHeader">
              <span className="intelligenceHeaderIcon"><Sparkles size={19} /></span>
              <span className="intelligenceHeaderCopy"><small><Wifi size={11} /> LIVE ACADEMIC CONTEXT</small><strong id="academic-assistant-title">{ar ? "نواة القرار الأكاديمي" : "Academic Decision Core"}</strong></span>
              <button type="button" onClick={() => setExpanded((value) => !value)} aria-label={expanded ? (ar ? "تصغير النافذة" : "Minimize panel") : (ar ? "توسيع النافذة" : "Expand panel")}>{expanded ? <Minimize2 size={17} /> : <Maximize2 size={17} />}</button>
              <button type="button" onClick={() => setOpen(false)} aria-label={ar ? "إغلاق" : "Close"}><X size={17} /></button>
            </header>

            <div className="intelligenceActions" aria-label={ar ? "إجراءات مقترحة" : "Suggested actions"}>
              {actions.map((action) => <button key={action.id} type="button" onClick={() => runQuickAction(action)} disabled={busy}><Activity size={12} />{localized(action, "label", language)}</button>)}
            </div>

            <div className="intelligenceChat" ref={chatRef} aria-live="polite">
              {!messages.length && <div className="intelligenceWelcome"><span><Database size={19} /></span><div><small>INTELLIGENCE READY</small><h3>{ar ? "اسأل المنصة. خذ إجابة من بياناتها." : "Ask the platform. Get an answer from its data."}</h3><p>{ar ? "ابحث عن طالب برقم جامعي، حلّل مسار الرسائل، أو اكتشف نقطة تراكم في الاعتمادات." : "Find a student by university ID, analyze thesis stages, or identify an approval bottleneck."}</p></div></div>}
              {!messages.length && <div className="intelligenceExamples">{(EXAMPLES[language] || EXAMPLES.en).map((example) => <button key={example} type="button" onClick={() => send(example)}>{example}<ArrowUp size={13} /></button>)}</div>}
              {messages.map((message) => <article className={`intelligenceMessage ${message.from} ${message.error ? "isError" : ""}`} key={message.id}>{message.from === "bot" && <span><Bot size={14} /></span>}<div>{message.intent && <small>{message.intent.toUpperCase()} / LIVE DATA</small>}<p>{message.text}</p>{message.retry && <button type="button" onClick={() => send(message.retry)}><RotateCcw size={13} />{ar ? "إعادة المحاولة" : "Retry"}</button>}</div></article>)}
              {busy && <div className="intelligenceThinking" role="status"><span className="scanLine" /><i /><i /><i /><b>{ar ? "جارٍ قراءة السياق الأكاديمي المصرح…" : "Reading authorized academic context…"}</b></div>}
            </div>

            <form className="intelligenceComposer" onSubmit={(event) => { event.preventDefault(); send(); }}>
              <span><Bot size={17} /></span><input ref={inputRef} value={question} onChange={(event) => setQuestion(event.target.value)} placeholder={ar ? "اسأل عن طالب، رسالة، لجنة أو قرار…" : "Ask about a student, thesis, committee, or decision…"} aria-label={ar ? "سؤال للمساعد الأكاديمي" : "Question for the academic assistant"} />
              <button type="submit" disabled={busy || !question.trim()} aria-label={ar ? "إرسال السؤال" : "Send question"}><ArrowUp size={18} /></button>
            </form>
            <footer className="intelligenceFooter"><span><i />{ar ? "مصدر الإجابة: قاعدة البيانات المباشرة" : "Answer source: live database"}</span><b>ZERO-TRUST CONTEXT</b></footer>
          </div>
        </section>
      )}
    </div>
  );
}
