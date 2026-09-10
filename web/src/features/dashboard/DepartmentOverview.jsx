import React from "react";
import DepartmentDistributionCard from "../../components/ui/DepartmentDistributionCard";

const ARABIC_RE = /[\u0600-\u06FF]/;

const FALLBACK_EN = {
  "طب الأطفال": "Pediatrics",
  "الأمراض الباطنة": "Internal Medicine",
  "التخدير والعناية المركزة": "Anesthesia and Intensive Care",
  "الباثولوجيا الإكلينيكية": "Clinical Pathology",
  "التوليد وأمراض النساء": "Obstetrics and Gynecology",
  "الأمراض الجلدية والتناسلية": "Dermatology and Venereology",
  "الأمراض الجلدية والتناسلية والذكورة": "Dermatology, Venereology and Andrology",
  "طب القلب والأوعية الدموية": "Cardiology and Cardiovascular Medicine",
  "جراحة المخ والأعصاب": "Neurosurgery",
  "الأشعة التشخيصية": "Diagnostic Radiology",
  "الجراحة العامة": "General Surgery",
  "الصحة العامة و طب المجتمع": "Public Health and Community Medicine",
  "الأنف والأذن والحنجرة": "ENT",
  "الانف والاذن والحنجرة": "ENT",
  "الروماتيزم والتأهيل": "Rheumatology and Rehabilitation",
  "الأمراض الصدرية": "Chest Diseases",
  "أمراض كلى": "Nephrology",
  "أمراض دم": "Hematology",
  "طب الأسرة": "Family Medicine"
};

function pick(arText, enText) {
  const en = String(enText || "").trim();
  if (en && !ARABIC_RE.test(en)) return en;

  let value = String(arText || "").trim();
  Object.entries(FALLBACK_EN)
    .sort((a, b) => b[0].length - a[0].length)
    .forEach(([ar, enVal]) => {
      value = value.split(ar).join(enVal);
    });

  return value;
}

export default function DepartmentDistributionPanel({
  departments = [],
  language = "ar",
}) {
  const ar = language === "ar";
  const max = Math.max(...departments.map((item) => Number(item.total) || 0), 1);

  return (
    <section className="panel departmentsPanel">
      <div className="paneltitle">
        <h3>{ar ? "توزيع الطلاب على الأقسام" : "Student Distribution by Department"}</h3>
      </div>

      <div className="departmentsList">
        {departments.map((item, index) => {
          const label = ar
            ? item.department__name_ar
            : pick(item.department__name_ar, item.department__name_en);

          const total = Number(item.total) || 0;
          const width = `${Math.max((total / max) * 100, 8)}%`;

          return (
            <DepartmentDistributionCard
              key={index}
              label={label}
              total={total}
              width={width}
            />
          );
        })}
      </div>
    </section>
  );
}
