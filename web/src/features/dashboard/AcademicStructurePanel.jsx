import React from "react";
import {
  GraduationCap,
  BookOpen,
  Users,
  Layers,
} from "lucide-react";

const ARABIC_RE = /[\u0600-\u06FF]/;

const FALLBACK_EN = {
  "الباثولوجيا الإكلينيكية": "Clinical Pathology",
  "طب وجراحة الذكورة والتناسلية والعقم": "Andrology, Reproductive and Infertility Surgery",
  "أمراض تخاطب": "Speech and Language Disorders",
  "طب المسنين وعلوم الأعمار": "Geriatrics and Aging Sciences",
  "الطب المهنى والبيئى": "Occupational and Environmental Medicine",
  "الأمراض الجلدية والتناسلية والذكورة": "Dermatology, Venereology and Andrology",
  "الأمراض الجلدية والتناسلية": "Dermatology and Venereology",
  "الأمراض الباطنة": "Internal Medicine",
  "التخدير والعناية المركزة": "Anesthesia and Intensive Care",
  "التخدير والعناية المركزة الجراحية": "Surgical Anesthesia and Intensive Care",
  "التشريح الآدمي وعلم الأجنة": "Human Anatomy and Embryology",
  "الكيمياء الحيوية الطبية": "Medical Biochemistry",
  "الفسيولوجيا الطبية": "Medical Physiology",
  "الهستولوجيا": "Histology",
  "المكروبيولوجيا الطبية والمناعة": "Medical Microbiology and Immunology",
  "الصحة العامة و طب المجتمع": "Public Health and Community Medicine",
  "الطب الشرعي و السموم الإكلينيكية": "Forensic Medicine and Clinical Toxicology",
  "طب وجراحة العيون": "Ophthalmology",
  "طب الأطفال": "Pediatrics",
  "الأمراض الصدرية": "Chest Diseases",
  "طب القلب والأوعية الدموية": "Cardiology and Cardiovascular Medicine",
  "الأمراض العصبية": "Neurology",
  "الطب النفسي": "Psychiatry",
  "جراحة التجميل والتكميل": "Plastic and Reconstructive Surgery",
  "جراحة التجميل": "Plastic Surgery",
  "جراحة العظام": "Orthopedic Surgery",
  "جراحة المسالك البولية": "Urology",
  "جراحة القلب والصدر": "Cardiothoracic Surgery",
  "جراحة المخ والأعصاب": "Neurosurgery",
  "الأشعة التشخيصية": "Diagnostic Radiology",
  "التوليد وأمراض النساء": "Obstetrics and Gynecology",
  "امراض النساء والتوليد": "Obstetrics and Gynecology",
  "طب الأسرة": "Family Medicine",
  "طب الطوارىء": "Emergency Medicine",
  "طب الطوارئ": "Emergency Medicine",
  "أمراض كلى": "Nephrology",
  "أمراض دم": "Hematology",
  "علاج أورام": "Oncology",
  "طب نووي": "Nuclear Medicine",
  "الروماتيزم والتأهيل": "Rheumatology and Rehabilitation",
  "الطفيليات الطبية": "Medical Parasitology",
  "سمعيات": "Audiology",
  "الباطنة": "Internal Medicine",
  "الجلدية": "Dermatology",
  "الأطفال": "Pediatrics",
  "العيون": "Ophthalmology",
  "التخاطب": "Speech",
  "الصدرية": "Chest Diseases",
  "القلب": "Cardiology",
  "الأعصاب": "Neurology",
  "النساء": "Gynecology",
  "العظام": "Orthopedics",
  "الأنف والأذن والحنجرة": "ENT",
  "الانف والاذن والحنجرة": "ENT",
  "الماجستير": "Master Degree",
  "ماجستير": "Master Degree",
  "دكتوراه": "Doctorate Degree",
  "الدبلومات المهنية": "Professional Diploma"
};

function clean(value) {
  return String(value || "").trim();
}

function translateToEnglish(text) {
  let value = clean(text);
  if (!value) return "";

  const prefixRules = [
    [/^ماجستير\s*-\s*/g, "Master - "],
    [/^دكتوراه\s*-\s*/g, "Doctorate - "],
    [/^دبلوم مهني في\s*/g, "Professional Diploma in "],
    [/^دبلوم\s*-\s*/g, "Diploma - "],
  ];

  prefixRules.forEach(([pattern, replacement]) => {
    value = value.replace(pattern, replacement);
  });

  Object.entries(FALLBACK_EN)
    .sort((a, b) => b[0].length - a[0].length)
    .forEach(([ar, en]) => {
      value = value.split(ar).join(en);
    });

  return value
    .replace(/\s+,/g, ",")
    .replace(/\s{2,}/g, " ")
    .trim();
}

function pickText(arText, enText) {
  const en = clean(enText);
  if (en && !ARABIC_RE.test(en)) return en;
  return translateToEnglish(arText);
}

export default function AcademicStructurePanel({
  structure,
  language = "ar",
}) {
  const ar = language === "ar";

  if (!structure) return null;

  const degrees = structure.degrees || [];
  const programs = structure.programs || [];

  const stats = [
    {
      icon: <Layers />,
      value: degrees.length,
      ar: "درجات أكاديمية",
      en: "Academic Degrees",
    },
    {
      icon: <BookOpen />,
      value: programs.length,
      ar: "برامج أكاديمية",
      en: "Academic Programs",
    },
    {
      icon: <GraduationCap />,
      value: structure.theses || 0,
      ar: "رسائل علمية",
      en: "Theses",
    },
    {
      icon: <Users />,
      value: structure.students || 0,
      ar: "طلاب مسجلين",
      en: "Students",
    },
  ];

  return (
    <section className="panel academicStructure">
      <div className="paneltitle">
        <h3>{ar ? "الهيكل الأكاديمي" : "Academic Structure"}</h3>
      </div>

      <div className="academicStats">
        {stats.map((item, index) => (
          <div className="academicStat" key={index}>
            <div className="academicIcon">{item.icon}</div>
            <strong>{item.value}</strong>
            <span>{ar ? item.ar : item.en}</span>
          </div>
        ))}
      </div>

      <h4>{ar ? "الدرجات العلمية" : "Academic Degrees"}</h4>

      <div className="academicDegrees">
        {degrees.map((degree) => (
          <div className="academicCard" key={degree.code}>
            <strong title={ar ? degree.name_ar : pickText(degree.name_ar, degree.name_en)}>
              {ar ? degree.name_ar : pickText(degree.name_ar, degree.name_en)}
            </strong>

            <span>
              {degree.programs_count || 0} {ar ? "برامج" : "Programs"}
            </span>
          </div>
        ))}
      </div>

      <h4>{ar ? "البرامج الأكاديمية" : "Academic Programs"}</h4>

      <div className="programGrid">
        {programs.map((program) => {
          const programName = ar
            ? program.name_ar
            : pickText(program.name_ar, program.name_en);

          const deptName = ar
            ? program.department__name_ar
            : pickText(program.department__name_ar, program.department__name_en);

          const degreeName = ar
            ? program.degree__name_ar
            : pickText(program.degree__name_ar, program.degree__name_en);

          return (
            <article key={program.code} className="programCard">
              <b title={programName}>{programName}</b>

              <small title={program.code}>{program.code}</small>

              <p title={ar ? `القسم: ${deptName}` : `Department: ${deptName}`}>
                {ar ? `القسم: ${deptName}` : `Department: ${deptName}`}
              </p>

              <p title={ar ? `الدرجة: ${degreeName}` : `Degree: ${degreeName}`}>
                {ar ? `الدرجة: ${degreeName}` : `Degree: ${degreeName}`}
              </p>
            </article>
          );
        })}
      </div>
    </section>
  );
}
