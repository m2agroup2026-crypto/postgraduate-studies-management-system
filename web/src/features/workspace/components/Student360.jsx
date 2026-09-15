import React, { useEffect, useMemo, useState } from "react";
import { BookOpen, CalendarDays, Clock3, GraduationCap, UserRound, X } from "lucide-react";
import StatusBadge from "../../../components/ui/StatusBadge";
import { actionLabel, degreeLabel, displayValue, localized, localizedName, statusLabel, statusTone } from "../../../i18n";

function formatDate(value, language) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat(language === "ar" ? "ar-EG" : "en-GB", { year: "numeric", month: "short", day: "numeric" }).format(date);
}

export default function Student360({ api, studentId, language = "ar", onLoaded, onClose }) {
  const ar = language === "ar";
  const [studentData, setStudentData] = useState(null);
  const [thesisData, setThesisData] = useState(null);
  const [activeTab, setActiveTab] = useState("overview");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    setActiveTab("overview");
    api(`/students/${studentId}/`)
      .then(async (studentPayload) => {
        if (!active) return;
        setStudentData(studentPayload);
        onLoaded?.(studentPayload.student);
        const thesisId = studentPayload.student?.thesis?.id;
        if (thesisId) {
          try {
            const thesisPayload = await api(`/theses/${thesisId}/`);
            if (active) setThesisData(thesisPayload);
          } catch {
            if (active) setThesisData(null);
          }
        } else {
          setThesisData(null);
        }
      })
      .catch((requestError) => active && setError(requestError.message))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [api, onLoaded, studentId]);

  const timeline = useMemo(() => {
    if (!studentData) return [];
    const enrollmentEvents = (studentData.academic_history || []).flatMap((enrollment) =>
      (enrollment.events || []).map((event) => ({
        id: `enrollment-${enrollment.program}-${event.created_at}`,
        date: event.created_at,
        type: ar ? "القيد الأكاديمي" : "Enrollment",
        title: actionLabel(event.event_type, language),
        detail: event.notes || `${statusLabel(event.from_status, language)} → ${statusLabel(event.to_status, language)}`,
      }))
    );
    const workflowEvents = (thesisData?.workflow?.history || []).map((event) => ({
      id: `workflow-${event.id}`,
      date: event.created_at,
      type: ar ? "مسار الرسالة" : "Thesis workflow",
      title: actionLabel(event.action, language),
      detail: event.notes || `${statusLabel(event.from_status, language)} → ${statusLabel(event.to_status, language)}`,
    }));
    const defense = studentData.defense_history;
    const defenseEvents = defense?.defense_date ? [{
      id: "defense-current",
      date: defense.defense_date,
      type: ar ? "المناقشة" : "Defense",
      title: ar ? "موعد المناقشة المسجل" : "Recorded defense date",
      detail: statusLabel(defense.status, language),
    }] : [];
    return [...enrollmentEvents, ...workflowEvents, ...defenseEvents]
      .filter((event) => event.date)
      .sort((a, b) => new Date(b.date) - new Date(a.date));
  }, [ar, language, studentData, thesisData]);

  if (loading) return <section className="panel student360 workspaceLoading">{ar ? "جارٍ تجهيز ملف الطالب…" : "Preparing student record…"}</section>;
  if (error) return <section className="panel student360"><p className="workspaceInlineError">{error}</p><button type="button" onClick={onClose}>{ar ? "إغلاق" : "Close"}</button></section>;

  const student = studentData?.student;
  if (!student) return null;
  const enrollments = studentData.academic_history || [];
  const thesis = thesisData?.thesis || student.thesis;
  const defense = studentData.defense_history;
  const tabs = [
    { key: "overview", ar: "نظرة عامة", en: "Overview", visible: true },
    { key: "enrollment", ar: "القيد", en: "Enrollment", visible: enrollments.length > 0 },
    { key: "thesis", ar: "الرسالة", en: "Thesis", visible: Boolean(thesis) },
    { key: "defense", ar: "المناقشة", en: "Defense", visible: Boolean(defense) },
    { key: "timeline", ar: "السجل الزمني", en: "Timeline", visible: timeline.length > 0 },
  ].filter((tab) => tab.visible);

  return (
    <section className="panel student360" aria-labelledby="student360-title">
      <header className="student360Header">
        <div className="student360Identity">
          <span aria-hidden="true"><UserRound size={22} /></span>
          <div><small>Student 360</small><h3 id="student360-title">{localized(student, "name", language)}</h3><p>{displayValue(student.university_id)}</p></div>
        </div>
        <button className="iconButton" type="button" onClick={onClose} aria-label={ar ? "إغلاق ملف الطالب" : "Close student record"}><X size={18} /></button>
      </header>

      <div className="student360Tabs" role="tablist" aria-label={ar ? "أقسام ملف الطالب" : "Student record sections"}>
        {tabs.map((tab) => <button key={tab.key} type="button" role="tab" aria-selected={activeTab === tab.key} className={activeTab === tab.key ? "active" : ""} onClick={() => setActiveTab(tab.key)}>{ar ? tab.ar : tab.en}</button>)}
      </div>

      <div className="student360Content">
        {activeTab === "overview" && (
          <div className="studentOverviewGrid">
            <article><UserRound size={18} /><span>{ar ? "الاسم" : "Name"}</span><strong>{localized(student, "name", language)}</strong></article>
            <article><GraduationCap size={18} /><span>{ar ? "الرقم الجامعي" : "University ID"}</span><strong>{displayValue(student.university_id)}</strong></article>
            <article><BookOpen size={18} /><span>{ar ? "القسم" : "Department"}</span><strong>{localized(student.department, "name", language)}</strong></article>
            {thesis && <article><Clock3 size={18} /><span>{ar ? "حالة الرسالة" : "Thesis status"}</span><StatusBadge tone={statusTone(thesis.status)}>{statusLabel(thesis.status, language)}</StatusBadge></article>}
          </div>
        )}

        {activeTab === "enrollment" && <div className="studentRecordList">{enrollments.map((enrollment, index) => <article key={`${typeof enrollment.program === "object" ? enrollment.program?.id : enrollment.program}-${index}`}><div><small>{degreeLabel(enrollment.degree, language)}</small><h4>{localizedName(enrollment.program, language)}</h4></div><StatusBadge tone={statusTone(enrollment.status)}>{statusLabel(enrollment.status, language)}</StatusBadge><dl><div><dt>{ar ? "العام الأكاديمي" : "Academic year"}</dt><dd>{displayValue(enrollment.academic_year)}</dd></div><div><dt>{ar ? "تاريخ القيد" : "Enrollment date"}</dt><dd>{formatDate(enrollment.enrollment_date, language)}</dd></div></dl></article>)}</div>}

        {activeTab === "thesis" && thesis && (
          <div className="studentThesisWorkspace">
            <article className="studentThesisSummary"><BookOpen size={20} /><div><small>{ar ? "عنوان الرسالة" : "Thesis title"}</small><h4>{localized(thesis, "title", language)}</h4><StatusBadge tone={statusTone(thesis.status)}>{statusLabel(thesis.status, language)}</StatusBadge></div></article>
            {(thesisData?.workflow?.history || []).length > 0 && <div className="studentWorkflow"><h4>{ar ? "مسار الاعتماد" : "Approval workflow"}</h4>{thesisData.workflow.history.map((event) => <div key={event.id}><span /><p><strong>{actionLabel(event.action, language)}</strong><small>{formatDate(event.created_at, language)} · {displayValue(event.performed_by?.name || event.performed_by?.username)}</small></p></div>)}</div>}
          </div>
        )}

        {activeTab === "defense" && defense && <div className="studentDefenseCard"><CalendarDays size={25} /><div><small>{ar ? "موعد المناقشة" : "Defense date"}</small><strong>{formatDate(defense.defense_date, language)}</strong><StatusBadge tone={statusTone(defense.status)}>{statusLabel(defense.status, language)}</StatusBadge></div></div>}

        {activeTab === "timeline" && <div className="studentAuditTimeline">{timeline.map((event) => <article key={event.id}><span className="studentAuditDot" /><div><small>{event.type} · {formatDate(event.date, language)}</small><strong>{event.title}</strong>{event.detail && <p>{event.detail}</p>}</div></article>)}</div>}
      </div>
    </section>
  );
}
