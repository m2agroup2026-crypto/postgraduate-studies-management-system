import React from "react";
import Panel from "../../components/ui/Panel";
import {
  GraduationCap,
  BookOpen,
  Users,
  Layers,
} from "lucide-react";
import AcademicStatCard from "../../components/ui/AcademicStatCard";
import AcademicDegreeCard from "../../components/ui/AcademicDegreeCard";
import AcademicProgramCard from "../../components/ui/AcademicProgramCard";
import SectionHeader from "../../components/ui/SectionHeader";
import { localized, localizedFlat } from "../../i18n";

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
      icon: Layers,
      value: degrees.length,
      ar: "درجات أكاديمية",
      en: "Academic Degrees",
    },
    {
      icon: BookOpen,
      value: programs.length,
      ar: "برامج أكاديمية",
      en: "Academic Programs",
    },
    {
      icon: GraduationCap,
      value: structure.theses || 0,
      ar: "رسائل علمية",
      en: "Theses",
    },
    {
      icon: Users,
      value: structure.students || 0,
      ar: "طلاب مسجلين",
      en: "Students",
    },
  ];

  return (
    <Panel className="academicStructure">
      <SectionHeader
        title={ar ? "الهيكل الأكاديمي" : "Academic Structure"}
      />

      <div className="academicStats">
        {stats.map((item, index) => (
          <AcademicStatCard
            key={index}
            icon={item.icon}
            value={item.value}
            label={ar ? item.ar : item.en}
          />
        ))}
      </div>

      <h4>{ar ? "الدرجات العلمية" : "Academic Degrees"}</h4>

      <div className="academicDegrees">
        {degrees.map((degree) => (
          <AcademicDegreeCard
            key={degree.code}
            name={localized(degree, "name", language)}
            programsCount={degree.programs_count || 0}
            programsLabel={ar ? "برامج" : "Programs"}
          />
        ))}
      </div>

      <h4>{ar ? "البرامج الأكاديمية" : "Academic Programs"}</h4>

      <div className="programGrid">
        {programs.map((program) => {
          const programName = localized(program, "name", language);
          const deptName = localizedFlat(program, "department__name", language);
          const degreeName = localizedFlat(program, "degree__name", language);

          return (
            <AcademicProgramCard
              key={program.code}
              name={programName}
              code={program.code}
              department={deptName}
              degree={degreeName}
              labels={{
                department: ar ? "القسم" : "Department",
                degree: ar ? "الدرجة" : "Degree",
              }}
            />
          );
        })}
      </div>
    </Panel>
  );
}
