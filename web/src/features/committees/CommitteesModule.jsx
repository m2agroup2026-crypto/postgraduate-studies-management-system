import React, { useEffect, useMemo, useState } from "react";
import {
  CalendarCheck,
  CalendarDays,
  CalendarX,
  ChevronLeft,
  ChevronRight,
  Clock3,
  Search,
  X,
} from "lucide-react";

const EVENT_LABELS = {
  SCHEDULED: { ar: "تمت الجدولة", en: "Scheduled" },
  RESCHEDULED: { ar: "إعادة جدولة", en: "Rescheduled" },
  DATE_CLEARED: { ar: "إلغاء التاريخ", en: "Date cleared" },
};

function formatDate(value, language) {
  if (!value) return "—";
  const parsed = new Date(`${value}T00:00:00`);
  return new Intl.DateTimeFormat(language === "ar" ? "ar-EG" : "en-GB", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(parsed);
}

function eventLabel(value, language) {
  const labels = EVENT_LABELS[value];
  return labels?.[language] || labels?.ar || value;
}

function CommitteeDetail({ api, thesisId, language, onClose, onChanged }) {
  const [data, setData] = useState(null);
  const [dateValue, setDateValue] = useState("");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const ar = language === "ar";

  const load = async () => {
    setError("");
    const result = await api(`/committees/${thesisId}/`);
    setData(result);
    setDateValue(result.record.defense?.defense_date || "");
  };

  useEffect(() => {
    let active = true;
    setData(null);
    setError("");
    api(`/committees/${thesisId}/`)
      .then((result) => {
        if (!active) return;
        setData(result);
        setDateValue(result.record.defense?.defense_date || "");
      })
      .catch((err) => active && setError(err.message));
    return () => { active = false; };
  }, [api, thesisId]);

  const saveSchedule = async (defenseDate) => {
    setBusy(true);
    setError("");
    try {
      const result = await api(`/committees/${thesisId}/schedule/`, {
        method: "POST",
        body: JSON.stringify({
          defense_date: defenseDate || null,
          notes: notes.trim(),
        }),
      });
      setData(result);
      setDateValue(result.record.defense?.defense_date || "");
      setNotes("");
      onChanged();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  if (!data && !error) {
    return <section className="panel committeeDetail">{ar ? "جارٍ تحميل ملف المناقشة…" : "Loading defense record…"}</section>;
  }

  const record = data?.record;
  const canManage = data?.capabilities?.can_manage;

  return (
    <section className="panel committeeDetail">
      <div className="committeeDetailHeader">
        <div>
          <small>{ar ? "ملف المناقشة" : "Defense record"}</small>
          <h3>{record?.student?.name_ar || "—"}</h3>
          <p>{record?.thesis?.title_ar || ""}</p>
        </div>
        <button className="iconButton" type="button" onClick={onClose} aria-label="close">
          <X size={18} />
        </button>
      </div>

      {error && <div className="settingsNotice error">{error}</div>}

      {record && (
        <>
          <div className="committeeDetailGrid">
            <div><span>{ar ? "الرقم الجامعي" : "University ID"}</span><strong>{record.student.university_id}</strong></div>
            <div><span>{ar ? "القسم" : "Department"}</span><strong>{ar ? record.department.name_ar : record.department.name_en || record.department.name_ar}</strong></div>
            <div><span>{ar ? "حالة الرسالة" : "Thesis status"}</span><strong>{record.thesis.status}</strong></div>
            <div><span>{ar ? "حالة المناقشة" : "Defense status"}</span><strong>{record.defense?.status || (ar ? "غير مجدولة" : "Not scheduled")}</strong></div>
          </div>

          <div className="committeeScheduleCard">
            <div className="committeeSectionTitle">
              <CalendarDays size={18} />
              <strong>{ar ? "جدولة المناقشة" : "Defense scheduling"}</strong>
            </div>
            <div className="committeeCurrentDate">
              <span>{ar ? "الموعد الحالي" : "Current date"}</span>
              <strong>{formatDate(record.defense?.defense_date, language)}</strong>
            </div>

            {canManage ? (
              <div className="committeeScheduleForm">
                <label>
                  {ar ? "تاريخ المناقشة" : "Defense date"}
                  <input type="date" value={dateValue} onChange={(event) => setDateValue(event.target.value)} />
                </label>
                <label>
                  {ar ? "ملاحظات الجدولة" : "Scheduling notes"}
                  <textarea
                    rows="3"
                    value={notes}
                    onChange={(event) => setNotes(event.target.value)}
                    placeholder={ar ? "سبب إعادة الجدولة أو أي ملاحظة إدارية…" : "Reason for rescheduling or an administrative note…"}
                  />
                </label>
                <div className="committeeScheduleActions">
                  <button type="button" disabled={busy || !dateValue} onClick={() => saveSchedule(dateValue)}>
                    <CalendarCheck size={17} />
                    {busy ? (ar ? "جارٍ الحفظ…" : "Saving…") : (ar ? "حفظ الموعد" : "Save date")}
                  </button>
                  {record.defense?.defense_date && (
                    <button className="dangerGhost" type="button" disabled={busy} onClick={() => saveSchedule(null)}>
                      <CalendarX size={17} />
                      {ar ? "إلغاء التاريخ" : "Clear date"}
                    </button>
                  )}
                </div>
              </div>
            ) : (
              <p className="committeeReadOnlyNote">
                {ar ? "لديك صلاحية عرض جدول المناقشات فقط." : "You have read-only access to the defense schedule."}
              </p>
            )}
          </div>

          <div className="committeeHistory">
            <div className="committeeSectionTitle">
              <Clock3 size={18} />
              <strong>{ar ? "سجل تغييرات الجدولة" : "Scheduling history"}</strong>
            </div>
            {(data.schedule_history || []).length ? (
              <div className="committeeTimeline">
                {data.schedule_history.map((event) => (
                  <article key={event.id}>
                    <div className="timelineDot" />
                    <div>
                      <strong>{eventLabel(event.event_type, language)}</strong>
                      <span>
                        {formatDate(event.old_date, language)} → {formatDate(event.new_date, language)}
                      </span>
                      <small>{event.performed_by.name || event.performed_by.username}</small>
                      {event.notes && <p>{event.notes}</p>}
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <p className="committeeReadOnlyNote">{ar ? "لا توجد تغييرات مسجلة حتى الآن." : "No scheduling changes recorded yet."}</p>
            )}
          </div>
        </>
      )}
    </section>
  );
}

export default function CommitteesModule({ api, language }) {
  const [data, setData] = useState(null);
  const [searchInput, setSearchInput] = useState("");
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("");
  const [schedule, setSchedule] = useState("");
  const [page, setPage] = useState(1);
  const [selectedThesis, setSelectedThesis] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [reloadKey, setReloadKey] = useState(0);
  const ar = language === "ar";

  const queryString = useMemo(() => {
    const params = new URLSearchParams({ page: String(page), page_size: "12" });
    if (search) params.set("q", search);
    if (department) params.set("department", department);
    if (schedule) params.set("schedule", schedule);
    return params.toString();
  }, [department, page, schedule, search]);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    api(`/committees/?${queryString}`)
      .then((result) => active && setData(result))
      .catch((err) => active && setError(err.message))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [api, queryString, reloadKey]);

  const submitSearch = (event) => {
    event.preventDefault();
    setPage(1);
    setSearch(searchInput.trim());
  };

  const summary = data?.summary || {};
  const pages = data?.pagination?.pages || 0;

  return (
    <div className="committeesPage" dir={ar ? "rtl" : "ltr"}>
      <section className="committeesHeading">
        <div>
          <small>{ar ? "وحدة تشغيلية للمناقشات" : "Operational defense workspace"}</small>
          <h2>{ar ? "اللجان والمناقشات" : "Committees & Defenses"}</h2>
          <p>{ar ? "إدارة مواعيد المناقشات وربطها بالرسائل والطلاب مع سجل تدقيق لكل تغيير." : "Manage defense dates across theses and students with an audit trail for every scheduling change."}</p>
        </div>
      </section>

      <section className="committeeSummaryGrid">
        <div className="committeeSummaryCard"><CalendarDays size={20} /><span>{ar ? "إجمالي الرسائل" : "Theses"}</span><strong>{summary.total_theses || 0}</strong></div>
        <div className="committeeSummaryCard"><CalendarCheck size={20} /><span>{ar ? "مجدولة" : "Scheduled"}</span><strong>{summary.scheduled || 0}</strong></div>
        <div className="committeeSummaryCard"><Clock3 size={20} /><span>{ar ? "قادمة" : "Upcoming"}</span><strong>{summary.upcoming || 0}</strong></div>
        <div className="committeeSummaryCard"><CalendarX size={20} /><span>{ar ? "غير مجدولة" : "Unscheduled"}</span><strong>{summary.unscheduled || 0}</strong></div>
      </section>

      <section className="panel committeesPanel">
        <form className="committeesToolbar" onSubmit={submitSearch}>
          <label className="committeeSearch">
            <Search size={17} />
            <input
              value={searchInput}
              onChange={(event) => setSearchInput(event.target.value)}
              placeholder={ar ? "ابحث بالطالب أو الرقم الجامعي أو عنوان الرسالة…" : "Search student, university ID, or thesis title…"}
            />
          </label>

          <select value={department} onChange={(event) => { setDepartment(event.target.value); setPage(1); }}>
            <option value="">{ar ? "كل الأقسام" : "All departments"}</option>
            {(data?.filters?.departments || []).map((item) => (
              <option key={item.student__department_id} value={item.student__department_id}>
                {ar ? item.student__department__name_ar : item.student__department__name_en || item.student__department__name_ar}
              </option>
            ))}
          </select>

          <select value={schedule} onChange={(event) => { setSchedule(event.target.value); setPage(1); }}>
            <option value="">{ar ? "كل المواعيد" : "All schedules"}</option>
            <option value="upcoming">{ar ? "المناقشات القادمة" : "Upcoming"}</option>
            <option value="scheduled">{ar ? "المجدولة" : "Scheduled"}</option>
            <option value="unscheduled">{ar ? "غير المجدولة" : "Unscheduled"}</option>
            <option value="past">{ar ? "المناقشات السابقة" : "Past"}</option>
          </select>

          <button type="submit">{ar ? "بحث" : "Search"}</button>
        </form>

        {error && <div className="settingsNotice error">{error}</div>}
        {loading && <div className="committeesLoading">{ar ? "جارٍ تحميل جدول المناقشات…" : "Loading defense schedule…"}</div>}

        {!loading && !error && (
          <div className="committeesTableWrap">
            <table className="committeesTable">
              <thead>
                <tr>
                  <th>{ar ? "الطالب" : "Student"}</th>
                  <th>{ar ? "الرسالة العلمية" : "Thesis"}</th>
                  <th>{ar ? "القسم" : "Department"}</th>
                  <th>{ar ? "موعد المناقشة" : "Defense date"}</th>
                  <th>{ar ? "الحالة" : "Status"}</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {(data?.results || []).map((record) => (
                  <tr key={record.thesis.id}>
                    <td><strong>{record.student.name_ar}</strong><small>{record.student.university_id}</small></td>
                    <td className="committeeThesisCell">{record.thesis.title_ar}</td>
                    <td>{ar ? record.department.name_ar : record.department.name_en || record.department.name_ar}</td>
                    <td>{formatDate(record.defense?.defense_date, language)}</td>
                    <td>
                      <span className={record.defense?.defense_date ? "scheduleBadge scheduled" : "scheduleBadge unscheduled"}>
                        {record.defense?.defense_date ? (ar ? "مجدولة" : "Scheduled") : (ar ? "غير مجدولة" : "Unscheduled")}
                      </span>
                    </td>
                    <td><button className="committeeViewButton" type="button" onClick={() => setSelectedThesis(record.thesis.id)}>{ar ? "فتح" : "Open"}</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
            {(data?.results || []).length === 0 && <div className="committeesEmpty">{ar ? "لا توجد سجلات مطابقة للفلاتر." : "No records match these filters."}</div>}
          </div>
        )}

        {pages > 1 && (
          <div className="committeesPagination">
            <button type="button" disabled={page <= 1} onClick={() => setPage((value) => Math.max(1, value - 1))}>{ar ? <ChevronRight size={17} /> : <ChevronLeft size={17} />}</button>
            <span>{ar ? `صفحة ${page} من ${pages}` : `Page ${page} of ${pages}`}</span>
            <button type="button" disabled={page >= pages} onClick={() => setPage((value) => Math.min(pages, value + 1))}>{ar ? <ChevronLeft size={17} /> : <ChevronRight size={17} />}</button>
          </div>
        )}
      </section>

      {selectedThesis && (
        <CommitteeDetail
          api={api}
          thesisId={selectedThesis}
          language={language}
          onClose={() => setSelectedThesis(null)}
          onChanged={() => setReloadKey((value) => value + 1)}
        />
      )}
    </div>
  );
}
