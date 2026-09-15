import React, { useEffect, useMemo, useState } from "react";
import { BookOpenCheck, CalendarClock, Inbox, UserRoundX } from "lucide-react";
import { displayValue, localized, statusLabel } from "../../../i18n";

const QUEUES = {
  no_thesis: {
    permission: "students.view",
    path: "/students/?thesis_status=NO_THESIS&page_size=8&ordering=-university_id",
    icon: UserRoundX,
    ar: "طلاب بلا رسالة مسجلة",
    en: "Students without a registered thesis",
    taskAr: "استكمال ملف طالب",
    taskEn: "Complete student record",
    statusAr: "لا توجد رسالة مسجلة",
    statusEn: "No thesis registered",
    actionAr: "فتح الملف ومراجعة البيانات",
    actionEn: "Open and review record",
  },
  pending_review: {
    permission: "theses.view",
    path: "/theses/?status=SUBMITTED&page_size=8&ordering=student",
    icon: BookOpenCheck,
    ar: "رسائل تنتظر المراجعة",
    en: "Theses awaiting review",
    taskAr: "مراجعة رسالة علمية",
    taskEn: "Review thesis",
    statusAr: "مرسلة للمراجعة",
    statusEn: "Submitted for review",
    actionAr: "فتح الملف ومراجعة المسار",
    actionEn: "Open and review workflow",
  },
  upcoming_defenses: {
    permission: "committees.view",
    path: "/committees/?schedule=upcoming&page_size=8&ordering=date",
    icon: CalendarClock,
    ar: "المناقشات القادمة",
    en: "Upcoming defenses",
    taskAr: "موعد مناقشة",
    taskEn: "Defense appointment",
    statusAr: "مجدولة",
    statusEn: "Scheduled",
    actionAr: "فتح الملف ومراجعة الموعد",
    actionEn: "Open and review date",
  },
};

export default function WorkQueue({ api, language = "ar", permissions = [], queueKey = "no_thesis", onSelectStudent }) {
  const ar = language === "ar";
  const allowed = useMemo(() => new Set(permissions), [permissions]);
  const queue = QUEUES[queueKey] || QUEUES.no_thesis;
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    if (!allowed.has(queue.permission)) {
      setData({ results: [], pagination: { total: 0 } });
      setLoading(false);
      return () => { active = false; };
    }
    setLoading(true);
    setError("");
    api(queue.path)
      .then((result) => active && setData(result))
      .catch((requestError) => active && setError(requestError.message))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [allowed, api, queue.path, queue.permission]);

  const Icon = queue.icon || Inbox;
  const results = data?.results || [];

  return (
    <section className="panel workspaceQueue" aria-labelledby="workspace-queue-title">
      <div className="workspaceSectionHeading workspaceQueueHeading">
        <div>
          <small>{ar ? "قائمة عمل مباشرة من النظام" : "Live system work queue"}</small>
          <h3 id="workspace-queue-title">{ar ? queue.ar : queue.en}</h3>
        </div>
        <span className="workspaceQueueCount"><Icon size={17} />{data?.pagination?.total ?? 0}</span>
      </div>

      {loading && <div className="workspaceLoading">{ar ? "جارٍ تحميل قائمة العمل…" : "Loading work queue…"}</div>}
      {error && <p className="workspaceInlineError">{error}</p>}
      {!loading && !error && results.length === 0 && <div className="workspaceEmpty">{ar ? "لا توجد سجلات في هذه القائمة حاليًا." : "This queue is currently clear."}</div>}

      {!loading && !error && results.length > 0 && (
        <div className="workspaceQueueList">
          {results.map((item) => {
            const student = queueKey === "no_thesis" ? item : item.student;
            const status = queueKey === "pending_review" ? item.status : queueKey === "upcoming_defenses" ? item.defense?.status : null;
            return (
              <article className="workspaceQueueItem" key={`${queueKey}-${item.id || item.thesis?.id}`}>
                <div className="workspaceQueueIdentity"><strong>{localized(student, "name", language)}</strong><small>{displayValue(student.university_id)}</small></div>
                <dl>
                  <div><dt>{ar ? "نوع المهمة" : "Task"}</dt><dd>{ar ? queue.taskAr : queue.taskEn}</dd></div>
                  <div><dt>{ar ? "الحالة الحالية" : "Current status"}</dt><dd>{status ? statusLabel(status, language) : (ar ? queue.statusAr : queue.statusEn)}</dd></div>
                  {queueKey === "upcoming_defenses" && item.defense?.defense_date && <div><dt>{ar ? "الموعد" : "Date"}</dt><dd>{item.defense.defense_date}</dd></div>}
                  <div><dt>{ar ? "الإجراء المطلوب" : "Required action"}</dt><dd>{ar ? queue.actionAr : queue.actionEn}</dd></div>
                </dl>
                <button type="button" onClick={() => onSelectStudent(student.id)}>{ar ? "فتح الملف" : "Open record"}</button>
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}
