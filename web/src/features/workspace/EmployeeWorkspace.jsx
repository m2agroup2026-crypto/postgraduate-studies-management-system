import React, { useCallback, useEffect, useMemo, useState } from "react";
import { BookOpenCheck, BriefcaseBusiness, CalendarClock, Clock3, ShieldCheck, UserRoundX } from "lucide-react";
import QuickActions from "./components/QuickActions";
import Student360 from "./components/Student360";
import UniversalSearch from "./components/UniversalSearch";
import WorkQueue from "./components/WorkQueue";
import { displayValue, localized } from "../../i18n";
import "./workspace.css";

const RECENT_LIMIT = 4;

export default function EmployeeWorkspace({ api, user, language = "ar", onNavigate }) {
  const ar = language === "ar";
  const permissions = useMemo(() => user?.permissions || [], [user?.permissions]);
  const firstQueue = permissions.includes("students.view") ? "no_thesis" : permissions.includes("theses.view") ? "pending_review" : "upcoming_defenses";
  const [activeAction, setActiveAction] = useState(firstQueue);
  const [focusSignal, setFocusSignal] = useState(0);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [summary, setSummary] = useState({ noThesis: null, pendingReview: null, upcomingDefenses: null });
  const [recentFiles, setRecentFiles] = useState(() => {
    try {
      return JSON.parse(window.localStorage.getItem(`pgms-recent-students:${user?.username}`)) || [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    let active = true;
    const request = (permission, path) => permissions.includes(permission)
      ? api(path).catch(() => ({ pagination: { total: null } }))
      : Promise.resolve({ pagination: { total: null } });
    Promise.all([
      request("students.view", "/students/?thesis_status=NO_THESIS&page_size=1"),
      request("theses.view", "/theses/?status=SUBMITTED&page_size=1"),
      request("committees.view", "/committees/?schedule=upcoming&page_size=1"),
    ]).then(([students, theses, committees]) => {
      if (!active) return;
      setSummary({
        noThesis: students.pagination?.total ?? null,
        pendingReview: theses.pagination?.total ?? null,
        upcomingDefenses: committees.pagination?.total ?? null,
      });
    });
    return () => { active = false; };
  }, [api, permissions]);

  const actionValues = [summary.noThesis, summary.pendingReview].filter((value) => typeof value === "number");
  const actionCount = actionValues.length ? actionValues.reduce((total, value) => total + value, 0) : null;

  const rememberStudent = useCallback((student) => {
    if (!student?.id) return;
    setRecentFiles((current) => {
      const next = [
        { id: student.id, name: localized(student, "name", language), university_id: student.university_id },
        ...current.filter((item) => item.id !== student.id),
      ].slice(0, RECENT_LIMIT);
      window.localStorage.setItem(`pgms-recent-students:${user?.username}`, JSON.stringify(next));
      return next;
    });
  }, [language, user?.username]);

  const handleAction = (action) => {
    setActiveAction(action);
    if (action === "search_student") setFocusSignal((value) => value + 1);
    if (action === "search_thesis") onNavigate?.("theses");
  };

  const tasks = [
    { key: "pending_review", icon: BookOpenCheck, value: summary.pendingReview, ar: "رسائل تنتظر المراجعة", en: "Theses awaiting review", permission: "theses.view" },
    { key: "no_thesis", icon: UserRoundX, value: summary.noThesis, ar: "طلاب بدون رسالة", en: "Students without thesis", permission: "students.view" },
    { key: "upcoming_defenses", icon: CalendarClock, value: summary.upcomingDefenses, ar: "مناقشات قادمة", en: "Upcoming defenses", permission: "committees.view" },
    { key: "recent", icon: Clock3, value: recentFiles.length, ar: "آخر الملفات المفتوحة", en: "Recently opened files", permission: "students.view" },
  ].filter((task) => permissions.includes(task.permission));

  return (
    <div className="employeeWorkspace" dir={ar ? "rtl" : "ltr"}>
      <section className="workspaceHero">
        <div className="workspaceHeroIcon" aria-hidden="true"><BriefcaseBusiness size={25} /></div>
        <div className="workspaceHeroCopy">
          <span>{ar ? "مركز العمليات الأكاديمية" : "Academic operations center"}</span>
          <h2>{ar ? "مساحة عمل الموظف" : "Employee Workspace"}</h2>
          <p>{localized(user, "name", language, user?.username)} · {localized(user, "title", language, ar ? "موظف الدراسات العليا" : "Postgraduate staff")}</p>
        </div>
        <div className="workspaceHeroStatus"><ShieldCheck size={17} /><span>{ar ? "ملفات تحتاج إجراء" : "Files requiring action"}</span><strong>{actionCount ?? "—"}</strong></div>
      </section>

      <section className="workspaceToday" aria-labelledby="today-tasks-title">
        <div className="workspaceTodayHeading"><div><small>{ar ? "صندوق العمل اليومي" : "Daily work inbox"}</small><h3 id="today-tasks-title">{ar ? "مهام اليوم" : "Today's tasks"}</h3></div></div>
        <div className="workspaceTaskCards">
          {tasks.map((task) => {
            const Icon = task.icon;
            return (
              <button key={task.key} type="button" onClick={() => task.key === "recent" ? recentFiles[0] && setSelectedStudent(recentFiles[0].id) : handleAction(task.key)} disabled={task.key === "recent" && recentFiles.length === 0}>
                <span aria-hidden="true"><Icon size={19} /></span><div><strong>{task.value ?? "—"}</strong><small>{ar ? task.ar : task.en}</small></div>
              </button>
            );
          })}
        </div>
        {recentFiles.length > 0 && <div className="workspaceRecentFiles">{recentFiles.map((file) => <button key={file.id} type="button" onClick={() => setSelectedStudent(file.id)}><strong>{displayValue(file.name || localized(file, "name", language))}</strong><span>{displayValue(file.university_id)}</span></button>)}</div>}
      </section>

      <QuickActions language={language} permissions={permissions} activeAction={activeAction} onAction={handleAction} />

      <div className="workspaceOperationsGrid">
        <UniversalSearch api={api} language={language} permissions={permissions} focusSignal={focusSignal} onSelectStudent={setSelectedStudent} />
        <WorkQueue api={api} language={language} permissions={permissions} queueKey={activeAction.startsWith("search_") ? firstQueue : activeAction} onSelectStudent={setSelectedStudent} />
      </div>

      {selectedStudent && <Student360 api={api} studentId={selectedStudent} language={language} onLoaded={rememberStudent} onClose={() => setSelectedStudent(null)} />}
    </div>
  );
}
