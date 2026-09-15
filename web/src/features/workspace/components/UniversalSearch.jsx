import React, { useEffect, useMemo, useRef, useState } from "react";
import { BookOpen, CalendarDays, Search, UserRound } from "lucide-react";
import { displayValue, localized } from "../../../i18n";

const MIN_QUERY_LENGTH = 2;

function resultCard(item, type, language, onSelectStudent) {
  const ar = language === "ar";
  const config = {
    student: { icon: UserRound, label: ar ? "طالب" : "Student" },
    thesis: { icon: BookOpen, label: ar ? "رسالة علمية" : "Thesis" },
    committee: { icon: CalendarDays, label: ar ? "مناقشة" : "Defense" },
  }[type];
  const Icon = config.icon;
  const student = type === "student" ? item : item.student;
  const title = type === "student" ? localized(student, "name", language) : localized(item.thesis || item, "title", language);
  const subtitle = type === "student"
    ? `${displayValue(student.university_id)} · ${localized(student.department, "name", language)}`
    : `${localized(student, "name", language)} · ${displayValue(student.university_id)}`;

  return (
    <article key={`${type}-${item.id || item.thesis?.id}`} className="workspaceSearchResult">
      <span className="workspaceResultIcon" aria-hidden="true"><Icon size={18} /></span>
      <span className="workspaceResultCopy">
        <small>{config.label}</small>
        <strong>{title}</strong>
        <em>{subtitle}</em>
      </span>
      <button type="button" onClick={() => onSelectStudent(student.id)}>{ar ? "فتح الملف" : "Open record"}</button>
    </article>
  );
}

export default function UniversalSearch({ api, language = "ar", permissions = [], focusSignal = 0, onSelectStudent }) {
  const ar = language === "ar";
  const inputRef = useRef(null);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState({ students: [], theses: [], committees: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const allowed = useMemo(() => new Set(permissions), [permissions]);

  useEffect(() => { if (focusSignal) inputRef.current?.focus(); }, [focusSignal]);

  useEffect(() => {
    const normalized = query.trim();
    if (normalized.length < MIN_QUERY_LENGTH) {
      setResults({ students: [], theses: [], committees: [] });
      setError("");
      return undefined;
    }

    let active = true;
    const timer = window.setTimeout(async () => {
      setLoading(true);
      setError("");
      const encoded = encodeURIComponent(normalized);
      const requests = [
        allowed.has("students.view") ? api(`/students/?q=${encoded}&page_size=6`) : Promise.resolve({ results: [] }),
        allowed.has("theses.view") ? api(`/theses/?q=${encoded}&page_size=6`) : Promise.resolve({ results: [] }),
        allowed.has("committees.view") ? api(`/committees/?q=${encoded}&page_size=6`) : Promise.resolve({ results: [] }),
      ];
      const settled = await Promise.allSettled(requests);
      if (!active) return;
      const payloads = settled.map((result) => result.status === "fulfilled" ? result.value : { results: [] });
      setResults({ students: payloads[0].results || [], theses: payloads[1].results || [], committees: payloads[2].results || [] });
      if (settled.every((result) => result.status === "rejected")) {
        setError(ar ? "تعذر تنفيذ البحث الآن." : "Search is currently unavailable.");
      }
      setLoading(false);
    }, 350);

    return () => { active = false; window.clearTimeout(timer); };
  }, [allowed, api, ar, query]);

  const total = results.students.length + results.theses.length + results.committees.length;

  return (
    <section className="panel workspaceSearchPanel" aria-labelledby="workspace-search-title">
      <div className="workspaceSectionHeading">
        <div>
          <small>{ar ? "بحث موحد في السجلات المصرح بها" : "Unified authorized-record search"}</small>
          <h3 id="workspace-search-title">{ar ? "الوصول السريع إلى ملف الطالب" : "Quick student record access"}</h3>
        </div>
      </div>

      <label className="workspaceSearchInput">
        <Search size={20} aria-hidden="true" />
        <input
          ref={inputRef}
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder={ar ? "اكتب اسم الطالب أو الرقم الجامعي أو عنوان الرسالة…" : "Type a student name, university ID, or thesis title…"}
          aria-label={ar ? "البحث الموحد" : "Universal search"}
        />
        {loading && <span role="status">{ar ? "جارٍ البحث…" : "Searching…"}</span>}
      </label>

      {error && <p className="workspaceInlineError">{error}</p>}
      {query.trim().length >= MIN_QUERY_LENGTH && !loading && !error && total === 0 && (
        <div className="workspaceEmpty">{ar ? "لا توجد نتائج مطابقة في السجلات المتاحة." : "No matching records were found."}</div>
      )}

      {total > 0 && (
        <div className="workspaceSearchGroups">
          {results.students.length > 0 && <section><h4>{ar ? "الطلاب" : "Students"}<span>{results.students.length}</span></h4><div>{results.students.map((item) => resultCard(item, "student", language, onSelectStudent))}</div></section>}
          {results.theses.length > 0 && <section><h4>{ar ? "الرسائل العلمية" : "Theses"}<span>{results.theses.length}</span></h4><div>{results.theses.map((item) => resultCard(item, "thesis", language, onSelectStudent))}</div></section>}
          {results.committees.length > 0 && <section><h4>{ar ? "المناقشات" : "Defenses"}<span>{results.committees.length}</span></h4><div>{results.committees.map((item) => resultCard(item, "committee", language, onSelectStudent))}</div></section>}
        </div>
      )}
    </section>
  );
}
