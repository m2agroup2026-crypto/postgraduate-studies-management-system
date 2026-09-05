import React from "react";
import {
  Users,
  BookOpen,
  CalendarDays,
  GraduationCap,
} from "lucide-react";

const cards = [
  {
    key: "students",
    label: "الطلاب النشطون",
    icon: Users,
  },
  {
    key: "theses",
    label: "الرسائل المسجلة",
    icon: BookOpen,
  },
  {
    key: "defenses",
    label: "المناقشات القادمة",
    icon: CalendarDays,
  },
  {
    key: "pending",
    label: "ملفات تحتاج متابعة",
    icon: GraduationCap,
  },
];

export default function MetricsCards({ metrics }) {
  return (
    <div className="metrics">
      {cards.map(({ key, label, icon: Icon }) => (
        <article key={key}>
          <Icon />
          <span>{label}</span>
          <strong>{metrics?.[key] ?? 0}</strong>
          <small>من قاعدة البيانات</small>
        </article>
      ))}
    </div>
  );
}
