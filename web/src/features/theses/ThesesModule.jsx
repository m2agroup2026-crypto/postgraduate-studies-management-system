import React, { useEffect, useMemo, useState } from "react";
import {
  BookOpenCheck,
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  Clock3,
  Search,
  ShieldCheck,
  UserRound,
  X,
} from "lucide-react";

import "./theses.css";

const STATUS_LABELS = {
  REGISTERED: { ar: "مسجلة", en: "Registered" },
  DRAFT: { ar: "مسودة", en: "Draft" },
  SUBMITTED: { ar: "مقدمة للمراجعة", en: "Submitted" },
  UNDER_REVIEW: { ar: "تحت المراجعة", en: "Under review" },
  DIRECTOR_APPROVED: { ar: "اعتماد مدير الدراسات العليا", en: "Director approved" },
  VICE_DEAN_APPROVED: { ar: "اعتماد الوكيل", en: "Vice Dean approved" },
  DEAN_APPROVED: { ar: "اعتماد العميد", en: "Dean approved" },
  FINAL_APPROVED: { ar: "اعتماد نهائي", en: "Final approved" },
  RETURNED: { ar: "معادة للاستكمال", en: "Returned" },
  REJECTED: { ar: "مرفوضة", en: "Rejected" },
  COMPLETED: { ar: "مكتملة", en: "Completed" },
};

const ACTION_LABELS = {
  SUBMIT: { ar: "تقديم", en: "Submit" },
  REVIEW: { ar: "بدء المراجعة", en: "Start review" },
  DIRECTOR_APPROVE: { ar: "اعتماد مدير الدراسات العليا", en: "Director approve" },
  VICE_DEAN_APPROVE: { ar: "اعتماد وكيل الدراسات العليا", en: "Vice Dean approve" },
  DEAN_APPROVE: { ar: "اعتماد العميد", en: "Dean approve" },
  FINAL_APPROVE: { ar: "الاعتماد النهائي", en: "Final approve" },
  REJECT: { ar: "رفض", en: "Reject" },
  RETURN: { ar: "إعادة للاستكمال", en: "Return" },
};

function textFor(dictionary, key, language) {
  const item = dictionary[key];
  return item?.[language] || item?.ar || key || "—";
}

function formatDateTime(value, language) {
  if (!value) return "—";
  return new Intl.DateTimeFormat(language === "ar" ? "ar-EG" : "en-GB", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function ThesisDetail({ api, thesisId, language, onClose, onChanged }) {
  const [data, setData] = useState(null);
  const [notes, setNotes] = useState("");
  const [error, setError] = useState("");
  const [busyAction, setBusyAction] = useState("");
  const ar = language === "ar";

  const load = () => {
    setError("");
    return api(`/theses/${thesisId}/`)
      .then(setData)
      .catch((err) => setError(err.message));
  };

  useEffect(() => {
    setData(null);
    setNotes("");
    load();
  }, [thesisId]);

  const runAction = async (action) => {
    setBusyAction(action);
    setError("");
    try {
      const next = await api(`/theses/${thesisId}/actions/`, {
        method: "POST",
        body: JSON.stringify({ action, notes }),
      });
      setData(next);
      setNotes("");
      onChanged();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusyAction("");
    }
  };

  const thesis = data?.thesis;
  const availableActions = data?.workflow?.available_actions || [];

  return (
    <section className="thesisDetail panel">
      <div className="thesisDetailHeader">
        <div>
          <small>{ar ? "ملف الرسالة وسير الاعتماد" : "Thesis record and approval workflow"}</small>
          <h3>{thesis?.title_ar || (ar ? "جارٍ تحميل الرسالة…" : "Loading thesis…")}</h3>
        </div>
        <button className="iconButton" type="button" onClick={onClose} aria-label="close">
          <X size={18} />
        </button>
      </div>

      {error && <div className="settingsNotice error">{error}</div>}

      {thesis && (
        <>
          <div className="thesisSummaryGrid">
            <div>
              <UserRound size={17} />
              <span>{ar ? "الطالب" : "Student"}</span>
              <strong>{thesis.student.name_ar}</strong>
              <small>{thesis.student.university_id}</small>
            </div>
            <div>
              <BookOpenCheck size={17} />
              <span>{ar ? "الحالة الحالية" : "Current status"}</span>
              <strong>{textFor(STATUS_LABELS, thesis.status, language)}</strong>
              <small>{thesis.status}</small>
            </div>
            <div>
              <ShieldCheck size={17} />
              <span>{ar ? "القسم" : "Department"}</span>
              <strong>
                {ar ? thesis.department.name_ar : thesis.department.name_en || thesis.department.name_ar}
              </strong>
              <small>{thesis.department.code}</small>
            </div>
            <div>
              <CalendarDays size={17} />
              <span>{ar ? "المناقشة" : "Defense"}</span>
              <strong>
                {thesis.defense?.defense_date || (ar ? "غير مجدولة" : "Not scheduled")}
              </strong>
              <small>{thesis.defense?.status || "—"}</small>
            </div>
          </div>

          <div className="workflowActionPanel">
            <div>
              <small>{ar ? "الإجراء المتاح حسب صلاحيتك والمرحلة الحالية" : "Action available for your role and current stage"}</small>
              <h4>{ar ? "إجراءات سير العمل" : "Workflow actions"}</h4>
            </div>

            {availableActions.length > 0 ? (
              <>
                <textarea
                  value={notes}
                  onChange={(event) => setNotes(event.target.value)}
                  placeholder={ar ? "ملاحظات الإجراء — اختيارية" : "Action notes — optional"}
                  maxLength={5000}
                />
                <div className="workflowActionButtons">
                  {availableActions.map((action) => (
                    <button
                      key={action}
                      type="button"
                      disabled={Boolean(busyAction)}
                      className={action === "REJECT" || action === "RETURN" ? "secondaryAction" : "primaryAction"}
                      onClick={() => runAction(action)}
                    >
                      {busyAction === action
                        ? (ar ? "جارٍ التنفيذ…" : "Processing…")
                        : textFor(ACTION_LABELS, action, language)}
                    </button>
                  ))}
                </div>
              </>
            ) : (
              <p className="workflowNoAction">
                {ar
                  ? "لا يوجد إجراء متاح لهذا الحساب في المرحلة الحالية."
                  : "No workflow action is available to this account at the current stage."}
              </p>
            )}
          </div>

          <div className="workflowTimeline">
            <div className="workflowTimelineHeading">
              <Clock3 size={18} />
              <div>
                <small>{ar ? "سجل تدقيق غير قابل للتجاوز" : "Auditable approval history"}</small>
                <h4>{ar ? "تاريخ الإجراءات" : "Action history"}</h4>
              </div>
            </div>

            {(data.workflow.history || []).length === 0 ? (
              <div className="workflowEmpty">
                {ar ? "لم يتم تسجيل أي إجراء على الرسالة حتى الآن." : "No workflow action has been recorded yet."}
              </div>
            ) : (
              data.workflow.history.map((item) => (
                <article className="workflowEvent" key={item.id}>
                  <div className="workflowEventMarker" />
                  <div>
                    <div className="workflowEventTitle">
                      <strong>{textFor(ACTION_LABELS, item.action, language)}</strong>
                      <span>{formatDateTime(item.created_at, language)}</span>
                    </div>
                    <p>
                      {textFor(STATUS_LABELS, item.from_status, language)}
                      {" → "}
                      {textFor(STATUS_LABELS, item.to_status, language)}
                    </p>
                    <small>
                      {item.performed_by.name} · {item.performed_by.role}
                    </small>
                    {item.notes && <blockquote>{item.notes}</blockquote>}
                  </div>
                </article>
              ))
            )}
          </div>
        </>
      )}
    </section>
  );
}

export default function ThesesModule({ api, language }) {
  const [data, setData] = useState(null);
  const [searchInput, setSearchInput] = useState("");
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("");
  const [status, setStatus] = useState("");
  const [defense, setDefense] = useState("");
  const [page, setPage] = useState(1);
  const [selectedThesis, setSelectedThesis] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const ar = language === "ar";

  const queryString = useMemo(() => {
    const params = new URLSearchParams({ page: String(page), page_size: "12" });
    if (search) params.set("q", search);
    if (department) params.set("department", department);
    if (status) params.set("status", status);
    if (defense) params.set("defense", defense);
    return params.toString();
  }, [defense, department, page, search, status]);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    api(`/theses/?${queryString}`)
      .then((result) => active && setData(result))
      .catch((err) => active && setError(err.message))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [queryString, refreshKey]);

  const submitSearch = (event) => {
    event.preventDefault();
    setPage(1);
    setSearch(searchInput.trim());
  };

  const total = data?.pagination?.total || 0;
  const pages = data?.pagination?.pages || 0;

  return (
    <div className="thesesPage" dir={ar ? "rtl" : "ltr"}>
      <section className="thesesHeading">
        <div>
          <small>{ar ? "وحدة تشغيلية مرتبطة بمحرك الاعتماد" : "Workflow-backed operational module"}</small>
          <h2>{ar ? "الرسائل العلمية وسير الاعتماد" : "Theses and Approval Workflow"}</h2>
          <p>
            {ar
              ? "متابعة موحدة للرسالة والطالب والقسم وحالة الاعتماد وسجل الإجراءات من نقطة واحدة."
              : "Track thesis, student, department, approval status, and audited actions from one workspace."}
          </p>
        </div>
        <div className="thesesCount">
          <BookOpenCheck size={20} />
          <span>{ar ? "إجمالي النتائج" : "Results"}</span>
          <strong>{total}</strong>
        </div>
      </section>

      <section className="panel thesesPanel">
        <form className="thesesToolbar" onSubmit={submitSearch}>
          <label className="thesisSearch">
            <Search size={17} />
            <input
              value={searchInput}
              onChange={(event) => setSearchInput(event.target.value)}
              placeholder={ar ? "ابحث بعنوان الرسالة أو اسم الطالب أو الرقم الجامعي…" : "Search thesis, student, or university ID…"}
            />
          </label>

          <select value={department} onChange={(event) => { setDepartment(event.target.value); setPage(1); }}>
            <option value="">{ar ? "كل الأقسام" : "All departments"}</option>
            {(data?.filters?.departments || []).map((item) => (
              <option key={item.student__department_id} value={item.student__department_id}>
                {ar
                  ? item.student__department__name_ar
                  : item.student__department__name_en || item.student__department__name_ar}
              </option>
            ))}
          </select>

          <select value={status} onChange={(event) => { setStatus(event.target.value); setPage(1); }}>
            <option value="">{ar ? "كل الحالات" : "All statuses"}</option>
            {(data?.filters?.statuses || []).map((item) => (
              <option key={item} value={item}>{textFor(STATUS_LABELS, item, language)}</option>
            ))}
          </select>

          <select value={defense} onChange={(event) => { setDefense(event.target.value); setPage(1); }}>
            <option value="">{ar ? "كل المناقشات" : "All defenses"}</option>
            <option value="scheduled">{ar ? "مناقشة مجدولة" : "Scheduled defense"}</option>
            <option value="unscheduled">{ar ? "بدون موعد مناقشة" : "No defense scheduled"}</option>
          </select>

          <button type="submit">{ar ? "بحث" : "Search"}</button>
        </form>

        {error && <div className="settingsNotice error">{error}</div>}
        {loading && <div className="thesesLoading">{ar ? "جارٍ تحميل الرسائل العلمية…" : "Loading theses…"}</div>}

        {!loading && !error && (
          <div className="thesesTableWrap">
            <table className="thesesTable">
              <thead>
                <tr>
                  <th>{ar ? "الطالب" : "Student"}</th>
                  <th>{ar ? "عنوان الرسالة" : "Thesis title"}</th>
                  <th>{ar ? "القسم" : "Department"}</th>
                  <th>{ar ? "الحالة" : "Status"}</th>
                  <th>{ar ? "المناقشة" : "Defense"}</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {(data?.results || []).map((thesis) => (
                  <tr key={thesis.id}>
                    <td>
                      <strong>{thesis.student.name_ar}</strong>
                      <small>{thesis.student.university_id}</small>
                    </td>
                    <td className="thesisTitleCell">{thesis.title_ar}</td>
                    <td>{ar ? thesis.department.name_ar : thesis.department.name_en || thesis.department.name_ar}</td>
                    <td>
                      <span className={`workflowStatus status-${thesis.status.toLowerCase()}`}>
                        {textFor(STATUS_LABELS, thesis.status, language)}
                      </span>
                    </td>
                    <td>{thesis.defense?.defense_date || "—"}</td>
                    <td>
                      <button className="thesisViewButton" type="button" onClick={() => setSelectedThesis(thesis.id)}>
                        {ar ? "فتح الملف" : "Open"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {(data?.results || []).length === 0 && (
              <div className="thesesEmpty">{ar ? "لا توجد رسائل مطابقة لمعايير البحث." : "No theses match these filters."}</div>
            )}
          </div>
        )}

        {pages > 1 && (
          <div className="thesesPagination">
            <button type="button" disabled={page <= 1} onClick={() => setPage((value) => Math.max(1, value - 1))}>
              {ar ? <ChevronRight size={17} /> : <ChevronLeft size={17} />}
            </button>
            <span>{ar ? `صفحة ${page} من ${pages}` : `Page ${page} of ${pages}`}</span>
            <button type="button" disabled={page >= pages} onClick={() => setPage((value) => Math.min(pages, value + 1))}>
              {ar ? <ChevronLeft size={17} /> : <ChevronRight size={17} />}
            </button>
          </div>
        )}
      </section>

      {selectedThesis && (
        <ThesisDetail
          api={api}
          thesisId={selectedThesis}
          language={language}
          onClose={() => setSelectedThesis(null)}
          onChanged={() => setRefreshKey((value) => value + 1)}
        />
      )}
    </div>
  );
}
