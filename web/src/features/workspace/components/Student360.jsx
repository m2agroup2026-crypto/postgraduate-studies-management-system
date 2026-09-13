import React, { useEffect, useState } from "react";

export default function Student360({
  api,
  studentId,
  language,
}) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  const ar = language === "ar";


  useEffect(() => {
    if (!studentId) return;

    let active = true;

    api(`/students/${studentId}/`)
      .then((result) => {
        if (active) {
          setData(result);
        }
      })
      .catch((err) => {
        if (active) {
          setError(err.message);
        }
      });

    return () => {
      active = false;
    };

  }, [api, studentId]);


  if (!studentId) {
    return null;
  }


  if (error) {
    return (
      <section className="student360">
        {error}
      </section>
    );
  }


  if (!data) {
    return (
      <section className="student360">
        {ar ? "جارٍ تحميل ملف الطالب..." : "Loading student record..."}
      </section>
    );
  }


  const student = data.student;


  return (
    <section className="student360">

      <header>
        <small>
          {ar ? "الملف الأكاديمي الكامل" : "Academic 360 Profile"}
        </small>

        <h2>
          {student.name_ar}
        </h2>

        <p>
          {student.university_id}
        </p>
      </header>


      <div className="student360Grid">

        <article>
          <h4>
            {ar ? "البيانات الأساسية" : "Personal Data"}
          </h4>

          <p>
            {student.name_ar}
          </p>

          <p>
            {ar ? "الرقم الجامعي: " : "University ID: "}
            {student.university_id}
          </p>

          <p>
            {ar ? "القسم: " : "Department: "}
            {student.department?.name_ar}
          </p>
        </article>


        <article>
          <h4>
            {ar ? "القيد الأكاديمي" : "Enrollment"}
          </h4>

          {(data.academic_history || []).length ? (
            data.academic_history.map((item, index) => (
              <div key={index}>
                <strong>
                  {item.program}
                </strong>

                <p>
                  {item.degree}
                </p>

                <small>
                  {item.status}
                </small>
              </div>
            ))
          ) : (
            <p>
              {ar ? "لا يوجد قيد مسجل" : "No enrollment record"}
            </p>
          )}

        </article>


        <article>
          <h4>
            {ar ? "الرسالة العلمية" : "Thesis"}
          </h4>

          {student.thesis ? (
            <>
              <p>
                {student.thesis.title_ar}
              </p>

              <small>
                {student.thesis.status}
              </small>
            </>
          ) : (
            <p>
              {ar ? "لا توجد رسالة" : "No thesis"}
            </p>
          )}

        </article>


        <article>
          <h4>
            {ar ? "المناقشة" : "Defense"}
          </h4>

          {data.defense_history ? (
            <>
              <p>
                {data.defense_history.defense_date}
              </p>

              <small>
                {data.defense_history.status}
              </small>
            </>
          ) : (
            <p>
              {ar ? "غير مجدولة" : "Not scheduled"}
            </p>
          )}

        </article>


        <article className="timelineCard">
          <h4>
            {ar ? "السجل الزمني" : "Audit Timeline"}
          </h4>

          {(data.academic_history || []).map((item,index)=>(
            <div key={index}>
              {item.events?.map((event,eventIndex)=>(
                <p key={eventIndex}>
                  {event.event_type}
                </p>
              ))}
            </div>
          ))}

        </article>

      </div>

    </section>
  );
}
