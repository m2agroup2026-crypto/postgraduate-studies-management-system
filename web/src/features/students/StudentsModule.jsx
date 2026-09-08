import React, { useEffect, useMemo, useState } from "react";
import { ChevronLeft, ChevronRight, Search, ShieldCheck, UserRound, X } from "lucide-react";

import "./students.css";

const STATUS_LABELS = {
  REGISTERED: { ar: "مسجلة", en: "Registered" },
  COMPLETED: { ar: "مكتملة", en: "Completed" },
  PENDING: { ar: "قيد المراجعة", en: "Pending" },
  NO_THESIS: { ar: "بدون رسالة", en: "No thesis" },
};

function statusLabel(status, language) {
  const labels = STATUS_LABELS[status];
  return labels?.[language] || labels?.ar || status || "—";
}

function StudentDetail({ api, studentId, language, onClose }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const ar = language === "ar";

  useEffect(() => {
    let active = true;
    setData(null);
    setError("");
    api(`/students/${studentId}/`)
      .then((result) => active && setData(result))
      .catch((err) => active && setError(err.message));
    return () => { active = false; };
  }, [api, studentId]);

  return (
    <section className="studentDetail panel">
      <div className="studentDetailHeader">
        <div>
          <small>{ar ? "الملف الأكاديمي" : "Academic record"}</small>
          <h3>{data?.student?.name_ar || (ar ? "جارٍ تحميل الطالب…" : "Loading student…")}</h3>
        </div>
        <button className="iconButton" type="button" onClick={onClose} aria-label="close">
          <X size={18} />
        </button>
      </div>

      {error && <div className="settingsNotice error">{error}</div>}
      {data && (
        <>
          <div className="studentDetailGrid">
            <div><span>{ar ? "الرقم الجامعي" : "University ID"}</span><strong>{data.student.university_id}</strong></div>
            <div><span>{ar ? "القسم" : "Department"}</span><strong>{ar ? data.student.department.name_ar : data.student.department.name_en || data.student.department.name_ar}</strong></div>
            <div><span>{ar ? "الرقم القومي" : "National ID"}</span><strong>{data.student.national_id || data.student.national_id_masked || "—"}</strong></div>
            <div><span>{ar ? "الكلية" : "Faculty"}</span><strong>{data.student.department.faculty ? (ar ? data.student.department.faculty.name_ar : data.student.department.faculty.name_en || data.student.department.faculty.name_ar) : "—"}</strong></div>
          </div>

          <div className="studentThesisCard">
            <div className="studentThesisTitle">
              <ShieldCheck size={18} />
              <strong>{ar ? "الرسالة العلمية" : "Thesis"}</strong>
            </div>
            {data.student.thesis ? (
              <>
                <p>{data.student.thesis.title_ar}</p>
                <span className={`statusBadge status-${data.student.thesis.status.toLowerCase()}`}>
                  {statusLabel(data.student.thesis.status, language)}
                </span>
              </>
            ) : (
              <p>{ar ? "لا توجد رسالة علمية مرتبطة بالسجل حتى الآن." : "No thesis is linked to this record yet."}</p>
            )}
          </div>

          {data.capabilities.can_manage && (
            <div className="studentPermissionNote">
              {ar
                ? "لديك صلاحية إدارة سجلات الطلاب. سيتم ربط إجراءات التعديل المعتمدة بسجل التدقيق في مرحلة العمليات التالية."
                : "You can manage student records. Approved write actions will be connected to the audit trail in the next operations phase."}
            </div>
          )}
        </>
      )}
    </section>
  );
}

export default function StudentsModule({ api, language }) {
  const [data, setData] = useState(null);
  const [searchInput, setSearchInput] = useState("");
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("");
  const [thesisStatus, setThesisStatus] = useState("");
  const [page, setPage] = useState(1);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const ar = language === "ar";

  const queryString = useMemo(() => {
    const params = new URLSearchParams({ page: String(page), page_size: "12" });
    if (search) params.set("q", search);
    if (department) params.set("department", department);
    if (thesisStatus) params.set("thesis_status", thesisStatus);
    return params.toString();
  }, [department, page, search, thesisStatus]);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    api(`/students/?${queryString}`)
      .then((result) => active && setData(result))
      .catch((err) => active && setError(err.message))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [api, queryString]);

  const submitSearch = (event) => {
    event.preventDefault();
    setPage(1);
    setSearch(searchInput.trim());
  };

  const total = data?.pagination?.total || 0;
  const pages = data?.pagination?.pages || 0;

  return (
    <div className="studentsPage" dir={ar ? "rtl" : "ltr"}>
      <section className="studentsHeading">
        <div>
          <small>{ar ? "وحدة تشغيلية مرتبطة بقاعدة البيانات" : "Database-backed operational module"}</small>
          <h2>{ar ? "سجل طلاب الدراسات العليا" : "Postgraduate Student Registry"}</h2>
          <p>{ar ? "بحث وفلترة واستعراض موحد لبيانات الطالب والقسم وحالة الرسالة العلمية." : "Search, filter, and inspect student, department, and thesis status data from one workspace."}</p>
        </div>
        <div className="studentsCount">
          <UserRound size={20} />
          <span>{ar ? "إجمالي النتائج" : "Results"}</span>
          <strong>{total}</strong>
        </div>
      </section>

      <section className="panel studentsPanel">
        <form className="studentsToolbar" onSubmit={submitSearch}>
          <label className="studentSearch">
            <Search size={17} />
            <input
              value={searchInput}
              onChange={(event) => setSearchInput(event.target.value)}
              placeholder={ar ? "ابحث بالاسم أو الرقم الجامعي أو القسم…" : "Search name, university ID, or department…"}
            />
          </label>

          <select value={department} onChange={(event) => { setDepartment(event.target.value); setPage(1); }}>
            <option value="">{ar ? "كل الأقسام" : "All departments"}</option>
            {(data?.filters?.departments || []).map((item) => (
              <option key={item.department_id} value={item.department_id}>
                {ar ? item.department__name_ar : item.department__name_en || item.department__name_ar}
              </option>
            ))}
          </select>

          <select value={thesisStatus} onChange={(event) => { setThesisStatus(event.target.value); setPage(1); }}>
            <option value="">{ar ? "كل حالات الرسائل" : "All thesis statuses"}</option>
            {(data?.filters?.thesis_statuses || []).map((status) => (
              <option key={status} value={status}>{statusLabel(status, language)}</option>
            ))}
            <option value="NO_THESIS">{statusLabel("NO_THESIS", language)}</option>
          </select>

          <button type="submit">{ar ? "بحث" : "Search"}</button>
        </form>

        {error && <div className="settingsNotice error">{error}</div>}
        {loading && <div className="studentsLoading">{ar ? "جارٍ تحميل سجلات الطلاب…" : "Loading student records…"}</div>}

        {!loading && !error && (
          <div className="studentsTableWrap">
            <table className="studentsTable">
              <thead>
                <tr>
                  <th>{ar ? "الرقم الجامعي" : "University ID"}</th>
                  <th>{ar ? "اسم الطالب" : "Student"}</th>
                  <th>{ar ? "القسم" : "Department"}</th>
                  <th>{ar ? "الرسالة العلمية" : "Thesis"}</th>
                  <th>{ar ? "الحالة" : "Status"}</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {(data?.results || []).map((student) => (
                  <tr key={student.id}>
                    <td><strong>{student.university_id}</strong></td>
                    <td>{student.name_ar}</td>
                    <td>{ar ? student.department.name_ar : student.department.name_en || student.department.name_ar}</td>
                    <td className="thesisCell">{student.thesis?.title_ar || "—"}</td>
                    <td>
                      <span className={`statusBadge status-${(student.thesis?.status || "no-thesis").toLowerCase()}`}>
                        {statusLabel(student.thesis?.status || "NO_THESIS", language)}
                      </span>
                    </td>
                    <td>
                      <button className="studentViewButton" type="button" onClick={() => setSelectedStudent(student.id)}>
                        {ar ? "عرض" : "View"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {(data?.results || []).length === 0 && (
              <div className="studentsEmpty">{ar ? "لا توجد سجلات مطابقة لمعايير البحث." : "No student records match these filters."}</div>
            )}
          </div>
        )}

        {pages > 1 && (
          <div className="studentsPagination">
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

      {selectedStudent && (
        <StudentDetail
          api={api}
          studentId={selectedStudent}
          language={language}
          onClose={() => setSelectedStudent(null)}
        />
      )}
    </div>
  );
}
